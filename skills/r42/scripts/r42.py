#!/usr/bin/env python3
"""r42 background jobs: queue, spawn wrapper, numbered events, ack, wait, reconcile.

State lives in .r42/ of the research repo (found by walking up from cwd, or $R42_ROOT):
  config.toml            agent entries, judges, limits
  jobs/<id>.json         one durable record per job
  jobs/<id>.prompt       prompt given to the agent
  jobs/<id>.log          agent stdout+stderr
  events.jsonl           append-only, one line per finished job, numbered by seq
  events.ack             highest seq the primary has handled

An agent entry is a provider (claude-code, opencode, codex, pi), an ordered model list,
a thinking level, and a natural-language `when`. When a model fails for an availability
reason (model not found, auth/quota, HTTP 4xx/5xx, provider unreachable), the wrapper
tries the next model; an ordinary failure of a working model does not fall back.

Every job ends in exactly one event: succeeded, failed (nonzero exit of a working model),
unavailable (every model failed for availability), crashed (wrapper vanished), or
skipped (a dependency did not succeed). Events and job records name the model that ran.
Python 3.11+, stdlib only.
"""
import argparse, base64, fcntl, json, os, re, shutil, subprocess, sys, time, tomllib
from contextlib import contextmanager
from pathlib import Path

DEFAULT_CONFIG = '''\
max_parallel = 4
notify = false          # OS notification per finished job (for harnesses that cannot be woken)
rex = false             # run each job in its own Rex tab (rex run) to watch agents live; needs `rex`
# Judges for revision votes and rankings: entry names ("default" = the entry without when).
# Mix model families.
judges = ["default", "codex"]

# Agent entries. The entry without `when` is the default for every step. /r42 reads each
# `when` and uses that entry where it applies; an explicit request ("solve on pi") wins.
#   provider  claude-code | opencode | codex | pi
#   model     ordered list; on an availability error (model not found, 401/402/403/404/429/5xx,
#             quota, auth, unreachable) the next model runs. Omit for the provider's default.
#   thinking  claude-code: --effort low|medium|high|xhigh|max
#             opencode: model variant, e.g. deepseek-v4.1-flash low|high|max (needs a model)
#             codex: model_reasoning_effort, e.g. low|medium|high
#             pi: --thinking off|minimal|low|medium|high|xhigh|max
#   limit     max jobs of this entry at once
#   cmd       optional: replace the provider's command template ({prompt}, {prompt_file},
#             {model}, {thinking}, {model#thinking}); fallback = "<regex>" replaces the
#             built-in availability-error pattern.
[agents.deepseek]
provider = "opencode"
model = ["opencode-go/deepseek-v4.1-flash", "opencode-go/glm-5.3", "opencode-go/kimi-k3"]
thinking = "high"
limit = 2

[agents.opus]
when = "checking questions for prior answers and validity (a fresh agent from another model family)"
provider = "claude-code"
model = ["claude-opus-5-5", "claude-sonnet-5-5"]
thinking = "high"
limit = 2

[agents.codex]
when = "judging, and whenever the user asks for codex"
provider = "codex"
limit = 2

[agents.pi]
when = "only when the user asks for pi"
provider = "pi"
limit = 2
'''

# Provider command templates. An argument whose placeholder has no value (no model, no
# thinking) is dropped together with the flag right before it.
PROVIDERS = {
    # keep {prompt} right after -p: --allowedTools takes several values and would swallow it
    "claude-code": ["claude", "-p", "{prompt}", "--model", "{model}", "--effort", "{thinking}",
                    "--permission-mode", "acceptEdits",
                    "--allowedTools", "WebSearch,WebFetch,Read,Grep,Glob,Write,Edit,Bash(python3:*)"],
    "opencode": ["opencode", "run", "--auto", "-m", "{model#thinking}", "{prompt}"],
    "codex": ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write", "-m", "{model}",
              "-c", "model_reasoning_effort={thinking}", "{prompt}"],
    "pi": ["pi", "-p", "--no-session", "--model", "{model}", "--thinking", "{thinking}", "{prompt}"],
}

# Availability failures: try the next model. Only the log tail of a nonzero exit is checked.
# ponytail: regex on output text; worker output near the end that quotes a provider error
# (e.g. "HTTP 503") still falls back once too often. Set fallback = "..." on the entry to tighten it.
UNAVAILABLE = (r"\b(model|variant) (is )?(unavailable|not found|does not exist|not supported)\b"
               r"|\b(unknown|invalid|no such) model\b|\bnot_found_error\b"
               r"|\b(http|status|error|code)\W{0,3}(40[1-4]|408|429|5\d\d)\b"
               r"|\b(unauthorized|forbidden|not found|overloaded|unavailable)\W{0,3}\(?(40[1-4]|429|5\d\d)\b"
               r"|\b(quota|rate limit|usage limit)\b[^\n]{0,30}\b(exceeded|reached|hit)\b"
               r"|\btoo many requests\b|\bpayment required\b|\bcredit balance\b|\binsufficient (credits?|balance|funds|quota)\b"
               r"|\b(invalid|missing) api key\b|\btoken (was )?(revoked|expired)\b|\bnot logged in\b|\bplease (log|sign) ?in\b"
               r"|\b(?-i:ECONNREFUSED|ENOTFOUND|ETIMEDOUT|ECONNRESET|EAI_AGAIN)\b|\bconnection (refused|reset|lost)\b"
               r"|\bcould not resolve host\b")

TERMINAL = {"succeeded", "failed", "unavailable", "crashed", "skipped"}


def root():
    if os.environ.get("R42_ROOT"):
        return Path(os.environ["R42_ROOT"])
    for d in [Path.cwd(), *Path.cwd().parents]:
        if (d / ".r42").is_dir():
            return d / ".r42"
    sys.exit("no .r42/ found here or above; run: r42.py init")


def config(r):
    return tomllib.loads((r / "config.toml").read_text())


def default_agent(c):
    names = [n for n, e in c.get("agents", {}).items() if not e.get("when")]
    if len(names) != 1:
        sys.exit(f"config.toml needs exactly one agent entry without `when` (the default); found {names}")
    return names[0]


def resolve(c, name):
    return default_agent(c) if name in (None, "default") else name


@contextmanager
def lock(r):
    with open(r / "lock", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def load(r, jid):
    return json.loads((r / "jobs" / f"{jid}.json").read_text())


def save(r, j):
    p = r / "jobs" / f"{j['id']}.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(j, indent=1))
    tmp.replace(p)


def jobs(r):
    return sorted((json.loads(p.read_text()) for p in (r / "jobs").glob("*.json")), key=lambda j: j["id"])


def events(r):
    p = r / "events.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def acked(r):
    p = r / "events.ack"
    return int(p.read_text() or 0) if p.exists() else 0


def finish(r, j, status, code=None):
    """Record a terminal state and its event. Caller holds the lock."""
    j.update(status=status, code=code, ended=time.time())
    j.setdefault("model", None)
    save(r, j)
    es = events(r)
    seq = (es[-1]["seq"] if es else 0) + 1
    e = {"seq": seq, "job": j["id"], "name": j["name"], "step": j["step"], "agent": j["agent"],
         "model": j["model"], "status": status, "code": code, "log": f"jobs/{j['id']}.log", "at": time.time()}
    with open(r / "events.jsonl", "a") as f:
        f.write(json.dumps(e) + "\n")
    if config(r).get("notify"):
        notify(f"r42: {j['name']} {status}")


def notify(msg):
    if shutil.which("osascript"):
        subprocess.run(["osascript", "-e", f"display notification {json.dumps(msg)} with title \"r42\""])
    elif shutil.which("notify-send"):
        subprocess.run(["notify-send", "r42", msg])


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def reconcile(r):
    """Jobs marked running whose wrapper process is gone crashed. Caller holds the lock."""
    # ponytail: pid liveness only; a reused pid hides a crash until that process exits
    for j in jobs(r):
        if j["status"] == "running" and not alive(j["pid"]):
            finish(r, j, "crashed")


def schedule(r):
    """Start every queued job whose deps succeeded, within limits. Caller holds the lock."""
    c = config(r)
    reconcile(r)
    all_ = {j["id"]: j for j in jobs(r)}
    running = [j for j in all_.values() if j["status"] == "running"]
    for j in all_.values():
        if j["status"] != "queued":
            continue
        deps = [all_[d]["status"] if d in all_ else "missing" for d in j["after"]]
        if any(s in TERMINAL - {"succeeded"} or s == "missing" for s in deps):
            finish(r, j, "skipped")
            continue
        if any(s != "succeeded" for s in deps):
            continue
        limit = c.get("agents", {}).get(j["agent"], {}).get("limit", c.get("max_parallel", 4))
        if len(running) >= c.get("max_parallel", 4) or sum(x["agent"] == j["agent"] for x in running) >= limit:
            continue
        p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "_run", j["id"]],
                             cwd=j["cwd"], env={**os.environ, "R42_ROOT": str(r)},
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        j.update(status="running", pid=p.pid, started=time.time())
        save(r, j)
        running.append(j)


def command(entry, model, prompt, prompt_file):
    t = entry.get("thinking")
    vals = {"{model#thinking}": model and (f"{model}#{t}" if t else model), "{model}": model, "{thinking}": t}
    out = []
    for a in entry.get("cmd") or PROVIDERS[entry["provider"]]:
        if any(k in a and v is None for k, v in vals.items()):
            if out and out[-1].startswith("-"):
                out.pop()
            continue
        for k, v in vals.items():
            a = a.replace(k, v or "")
        out.append(a.replace("{prompt_file}", prompt_file).replace("{prompt}", prompt))
    return out


def rex_sess(j):
    return ["-s", j["rex_session"]] if j.get("rex_session") else []


def rex_cmd(cmd, j, logp, model):
    """The `rex run` command that runs cmd through `_tab` in a new tab that stays open after
    it exits, so the user can read the result; `r42.py close` closes it. The login shell's
    environment gives the agent CLIs their PATH."""
    return ["rex", "run", *rex_sess(j), "--json", "--wait", "--keep-open", "--focus=false",
            "-c", j["cwd"], "--label", j["name"], "--", sys.executable, os.path.abspath(__file__), "_tab",
            str(logp), f"{j['step']}: {j['name']} ({model or 'default'})", *cmd]


def in_rex(r, j, cmd, logp, model, log):
    """Run cmd in a Rex tab named after the job, recording the tab on the job. Returns cmd's
    exit code, or None when Rex opened no tab (the caller then runs cmd directly)."""
    p = subprocess.Popen(rex_cmd(cmd, j, logp, model), cwd=j["cwd"], stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=log, text=True)
    out, w = "", None
    for line in p.stdout:  # --json prints the new tab before --wait blocks
        out += line
        try:
            w = json.JSONDecoder().raw_decode(out.lstrip())[0].get("window_id")
            break
        except ValueError:
            continue
    if w:
        subprocess.run(["rex", "window", "rename", *rex_sess(j), w, f"r42 {j['name']}"], capture_output=True)
        with lock(r):
            jj = load(r, j["id"])
            jj.setdefault("tabs", []).append(w)
            save(r, jj)
    p.stdout.read()
    code = p.wait()
    return code if w else None


def tab(logp, msg, cmd):
    """Inside a Rex tab: run cmd, copy its output to the tab and the job log, and report
    working/done/error through the Program Status Protocol (OSC 7501)."""
    def status(state, text):
        text = "".join(ch for ch in text if ch.isprintable())  # the protocol refuses control chars
        sys.stdout.write(f"\033]7501;state={state}:app=r42:msg={base64.b64encode(text.encode()).decode()}\033\\")
        sys.stdout.flush()
    jid = Path(logp).stem
    print(f"== r42 {msg}  job {jid} ==\n", flush=True)
    status("working", msg)
    with open(logp, "ab") as log:
        try:
            p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for chunk in iter(lambda: p.stdout.read1(4096), b""):
                sys.stdout.buffer.write(chunk)
                sys.stdout.flush()
                log.write(chunk)
                log.flush()
            code = p.wait()
        except OSError as e:
            log.write(f"r42: cannot start {cmd[0]}: {e}\n".encode())
            code = 127
    status("done", msg) if code == 0 else status("error", f"{msg}: exit {code}")
    print(f"\n== r42 {'succeeded' if code == 0 else f'failed (exit {code})'}  log {logp} ==\n"
          f"== close this tab: {sys.executable} {os.path.abspath(__file__)} close {jid} ==", flush=True)
    return code


def run(r, jid):
    """Wrapper: run the entry, falling back through its models on availability errors,
    then record the outcome as an event."""
    j = load(r, jid)
    entry = config(r)["agents"][j["agent"]]
    pattern = re.compile(entry.get("fallback", UNAVAILABLE), re.I)
    pf = r / "jobs" / f"{jid}.prompt"
    logp = r / "jobs" / f"{jid}.log"
    attempts = []
    for model in entry.get("model") or [None]:
        if load(r, jid).get("closed"):  # stopped by `close`: no fallback to the next model
            break
        cmd = command(entry, model, pf.read_text(), str(pf))
        with open(logp, "a") as log:
            log.write(f"== r42: {entry.get('provider', 'cmd')} model={model or 'default'} thinking={entry.get('thinking') or 'default'} ==\n")
            log.flush()
            try:
                code = None
                if config(r).get("rex") and j.get("rex_session") and shutil.which("rex"):
                    code = in_rex(r, j, cmd, logp, model, log)
                if code is None:
                    code = subprocess.run(cmd, cwd=j["cwd"], stdin=subprocess.DEVNULL, stdout=log, stderr=log).returncode
            except OSError as e:
                log.write(f"r42: cannot start {cmd[0]}: {e}\n")
                code = 127
        with open(logp, "rb") as log:
            log.seek(max(0, logp.stat().st_size - 4096))
            tail = log.read().decode(errors="replace")
        unavailable = code != 0 and (code == 127 or bool(pattern.search(tail)))
        attempts.append({"model": model, "code": code, "unavailable": unavailable})
        if not unavailable:
            break
    status = "succeeded" if code == 0 else "unavailable" if unavailable else "failed"
    with lock(r):
        j = load(r, jid)
        j.update(model=model, attempts=attempts)
        finish(r, j, status, code)
        schedule(r)


def unread(r):
    a = acked(r)
    return [e for e in events(r) if e["seq"] > a]


def show(es):
    for e in es:
        print(f"#{e['seq']} {e['status']:11} {e['name']} (step={e['step']} agent={e['agent']} model={e.get('model')} code={e['code']}) log={e['log']}")


def main():
    ap = argparse.ArgumentParser(prog="r42.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("agents", help="print the agent entries (with their when) and the judges")
    s = sub.add_parser("submit")
    s.add_argument("--step", required=True)
    s.add_argument("--name", required=True)
    s.add_argument("--agent", help="an agent entry name chosen by its `when` or the user's request; default: the entry without when")
    s.add_argument("--after", default="", help="comma-separated job ids that must succeed first")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    sub.add_parser("status")
    sub.add_parser("events", help="print unacknowledged events")
    s = sub.add_parser("ack")
    s.add_argument("seq", type=int)
    s = sub.add_parser("wait", help="block until an unacknowledged event exists")
    s.add_argument("--timeout", type=float, default=3600)
    sub.add_parser("reconcile")
    s = sub.add_parser("close", help="close the Rex tabs of these jobs (a running job stops); no ids: every finished job")
    s.add_argument("ids", nargs="*")
    s = sub.add_parser("_run")
    s.add_argument("id")
    s = sub.add_parser("_tab")
    s.add_argument("log")
    s.add_argument("msg")
    s.add_argument("argv", nargs=argparse.REMAINDER)
    a = ap.parse_args()

    if a.cmd == "init":
        r = Path.cwd() / ".r42"
        for d in ("jobs", "pack", "questions", "solves", "rankings", "reports"):
            (r / d).mkdir(parents=True, exist_ok=True)
        if not (r / "config.toml").exists():
            (r / "config.toml").write_text(DEFAULT_CONFIG)
        print(r)
        return
    if a.cmd == "_tab":
        sys.exit(tab(a.log, a.msg, a.argv))
    r = root()
    if a.cmd == "_run":
        return run(r, a.id)
    if a.cmd == "agents":
        c = config(r)
        d = default_agent(c)
        for n, e in c["agents"].items():
            print(f"{n}: provider={e.get('provider', 'cmd')} model={e.get('model') or 'default'} "
                  f"thinking={e.get('thinking') or 'default'} when={'(default)' if n == d else e['when']}")
        return print("judges: " + " ".join(resolve(c, x) for x in c.get("judges", ["default"])))
    if a.cmd == "submit":
        c = config(r)
        agent = resolve(c, a.agent)
        e = c.get("agents", {}).get(agent)
        if e is None:
            sys.exit(f"agent {agent!r} has no [agents.{agent}] entry in config.toml")
        if not e.get("cmd") and e.get("provider") not in PROVIDERS:
            sys.exit(f"agent {agent!r}: provider must be one of {', '.join(PROVIDERS)} (or give cmd)")
        with lock(r):
            jid = f"{time.strftime('%Y%m%d-%H%M%S')}-{len(jobs(r)) + 1:04d}"
            prompt = a.prompt if a.prompt is not None else Path(a.prompt_file).read_text()
            (r / "jobs" / f"{jid}.prompt").write_text(prompt)
            save(r, {"id": jid, "name": a.name, "step": a.step, "agent": agent,
                     "after": [x for x in a.after.split(",") if x], "cwd": str(r.parent),
                     "status": "queued", "pid": None, "code": None, "model": None,
                     "created": time.time(), "started": None, "ended": None,
                     "rex_session": os.environ.get("REX_SESSION")})
            schedule(r)
        return print(jid)
    with lock(r):
        reconcile(r)
        schedule(r)
    if a.cmd == "status":
        for j in jobs(r):
            print(f"{j['id']} {j['status']:11} {j['agent']:8} {j['step']:8} {j['name']} model={j.get('model') or '-'} after={','.join(j['after']) or '-'}"
                  + (f" tabs={len(j['tabs'])}" if j.get("tabs") else ""))
    elif a.cmd == "events":
        show(unread(r))
    elif a.cmd == "close":
        for j in jobs(r):
            if not (j["id"] in a.ids if a.ids else j["status"] in TERMINAL):
                continue
            with lock(r):  # mark first so run() does not fall back into a new tab
                j = load(r, j["id"])
                j["closed"] = True
                save(r, j)
            if j.get("tabs"):
                subprocess.run(["rex", "window", "close", *rex_sess(j), *j["tabs"]], capture_output=True)
                with lock(r):
                    jj = load(r, j["id"])
                    jj["tabs"] = [t for t in jj.get("tabs", []) if t not in j["tabs"]]
                    save(r, jj)
                print(f"closed {j['id']} {j['name']}")
    elif a.cmd == "ack":
        with lock(r):
            (r / "events.ack").write_text(str(max(a.seq, acked(r))))
    elif a.cmd == "wait":
        end = time.time() + a.timeout
        while not unread(r):
            if not any(j["status"] in ("queued", "running") for j in jobs(r)):
                print("idle: no unread events and no queued or running jobs")
                sys.exit(3)
            if time.time() > end:
                sys.exit(2)
            time.sleep(2)
            with lock(r):
                schedule(r)
        show(unread(r))


if __name__ == "__main__":
    main()
