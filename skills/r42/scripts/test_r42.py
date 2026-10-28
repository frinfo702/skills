#!/usr/bin/env python3
"""Self-check for r42.py: spawn -> event -> ack -> reconcile, a crashed wrapper,
a failed child, dependency ordering and skipping, the per-agent limit, and model
fallback (availability error -> next model; ordinary failure -> no fallback; exhaustion),
and the provider/model/thinking field mapping.
Run: python3 test_r42.py   (uses fake agents, no real model calls)
"""
import importlib.util, json, os, signal, subprocess, sys, tempfile, tomllib, time
from pathlib import Path

R42 = str(Path(__file__).with_name("r42.py"))


def r42(*args, check=True):
    p = subprocess.run([sys.executable, R42, *args], cwd=WD, capture_output=True, text=True)
    assert not check or p.returncode == 0, (args, p.stdout, p.stderr)
    return p.stdout.strip()


def job(jid):
    return json.loads((WD / ".r42" / "jobs" / f"{jid}.json").read_text())


def until(pred, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        if pred():
            return
        time.sleep(0.2)
    raise AssertionError("timed out")


WD = Path(tempfile.mkdtemp())
r42("init")
# field mapping of the shipped providers, and the shipped default config
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill directory
spec = importlib.util.spec_from_file_location("r42", R42)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
cmd = lambda model=None, **e: m.command(e, model, "P", "/p")
assert cmd("claude-opus-5-5", provider="claude-code", thinking="high")[:7] == \
    ["claude", "-p", "P", "--model", "claude-opus-5-5", "--effort", "high"]
assert "--model" not in cmd(provider="claude-code") and "--effort" not in cmd(provider="claude-code")
assert cmd("opencode-go/deepseek-v4.1-flash", provider="opencode", thinking="high") == \
    ["opencode", "run", "--auto", "-m", "opencode-go/deepseek-v4.1-flash#high", "P"]
assert cmd("x", provider="opencode") == ["opencode", "run", "--auto", "-m", "x", "P"]
assert cmd(provider="opencode", thinking="high") == ["opencode", "run", "--auto", "P"]
assert cmd("gpt", provider="codex", thinking="high")[-5:] == ["-m", "gpt", "-c", "model_reasoning_effort=high", "P"]
assert cmd(provider="codex")[-3:] == ["-s", "workspace-write", "P"]
rx = m.rex_cmd(["claude", "-p", "P"], {"cwd": "/w", "name": "q1", "step": "solve"}, "/l", "opus")
assert rx[:2] == ["rex", "run"] and {"--wait", "--keep-open", "--json"} <= set(rx) and rx[-6:] == ["_tab", "/l", "solve: q1 (opus)", "claude", "-p", "P"], rx
assert cmd("m", provider="pi", thinking="max") == ["pi", "-p", "--no-session", "--model", "m", "--thinking", "max", "P"]
# availability errors seen from real runtimes fall back; worker tracebacks and prose do not
unav = lambda text: bool(m.re.search(m.UNAVAILABLE, text, m.re.I))
for text in ["Error: Model unavailable: opencode-go/x", "Variant unavailable for opencode-go/x: bogus",
             "ERROR: workspace routing discovery unauthorized (401)", "refresh token was revoked",
             "API Error: 529 Overloaded", "Invalid API key", "HTTP 402 Payment Required",
             "Connection lost while reading the response: ECONNRESET", "Rate limit exceeded"]:
    assert unav(text), text
for text in ["ModuleNotFoundError: No module named 'numpy'", "NameError: name 'product' is not defined",
             "the model is not determined by the core", "we hit 404 cycles in the graph", "a quota of edges"]:
    assert not unav(text), text
shipped = tomllib.loads(m.DEFAULT_CONFIG)
assert m.default_agent(shipped) == "deepseek"
assert shipped["agents"]["deepseek"]["provider"] == "opencode"
assert shipped["agents"]["deepseek"]["model"][0] == "opencode-go/deepseek-v4.1-flash"
assert shipped["agents"]["opus"]["provider"] == "claude-code" and shipped["agents"]["opus"]["model"][0] == "claude-opus-5-5"
assert shipped["agents"]["opus"]["thinking"]

(WD / ".r42" / "config.toml").write_text('''
max_parallel = 4
judges = ["default", "other"]
[agents.fake]
# the model arrives as $2; without a model "-m {model}" is dropped
cmd = ["sh", "-c", "{prompt}", "sh", "-m", "{model}"]
limit = 1
[agents.other]
when = "solving"
cmd = ["sh", "-c", "{prompt}", "sh", "-m", "{model}"]
model = ["gone", "ok"]
[agents.dead]
when = "never"
cmd = ["sh", "-c", "{prompt}", "sh", "-m", "{model}"]
model = ["x", "y"]
''')

out = r42("agents")
assert "fake: provider=cmd model=default thinking=default when=(default)" in out, out
assert out.splitlines()[-1] == "judges: fake other"

# A then B (B after A); C after failing F is skipped; K is a wrapper we kill.
a = r42("submit", "--step", "pack", "--name", "A", "--prompt", "sleep 1; echo a > a.txt")
b = r42("submit", "--step", "pack", "--name", "B", "--after", a, "--prompt", "cat a.txt")
f = r42("submit", "--step", "solve", "--name", "F", "--agent", "other", "--prompt", "exit 7")
c = r42("submit", "--step", "solve", "--name", "C", "--agent", "other", "--after", f, "--prompt", "echo never")
k = r42("submit", "--step", "solve", "--name", "K", "--agent", "other", "--prompt", "sleep 30")
# fallback: model "gone" is unavailable, "ok" runs; "dead" exhausts both models
UNAV = 'if [ "$2" = gone ]; then echo "Error: Model unavailable: $2" >&2; exit 1; fi; echo "ran $2 $#"'
fb = r42("submit", "--step", "solve", "--name", "FB", "--agent", "other", "--prompt", UNAV)
ex = r42("submit", "--step", "solve", "--name", "EX", "--agent", "dead", "--prompt", 'echo "HTTP 503 Service Unavailable"; exit 1')
nf = r42("submit", "--step", "solve", "--name", "NF", "--agent", "other", "--prompt", 'echo "ModuleNotFoundError: No module named numpy"; exit 1')
dm = r42("submit", "--step", "pack", "--name", "DM", "--after", b, "--prompt", 'echo "args $#"')

# per-agent limit 1: B cannot start while A runs, and must wait for A anyway
assert job(a)["status"] == "running" and job(b)["status"] == "queued"
until(lambda: job(k)["status"] == "running")
os.killpg(job(k)["pid"], signal.SIGKILL)  # wrapper (and its child) die without recording an exit

out = r42("wait", "--timeout", "20")
assert out, "wait returned without events"
ALL = (a, b, f, c, k, fb, ex, dm, nf)
until(lambda: all(job(x)["status"] in ("succeeded", "failed", "unavailable", "crashed", "skipped") for x in ALL))
r42("reconcile")
assert job(k)["status"] == "crashed", job(k)
assert job(a)["status"] == "succeeded" and job(b)["status"] == "succeeded"
assert job(b)["started"] >= job(a)["ended"], "B started before A finished"
assert (WD / ".r42" / "jobs" / f"{b}.log").read_text().splitlines()[-1] == "a"
assert job(f)["status"] == "failed" and job(f)["code"] == 7
assert [x["model"] for x in job(f)["attempts"]] == ["gone"], "ordinary failure must not fall back"
assert job(c)["status"] == "skipped"
assert job(nf)["status"] == "failed" and len(job(nf)["attempts"]) == 1, "a worker traceback is not unavailability"
assert job(fb)["status"] == "succeeded" and job(fb)["model"] == "ok"
assert [x["unavailable"] for x in job(fb)["attempts"]] == [True, False]
assert "ran ok 2" in (WD / ".r42" / "jobs" / f"{fb}.log").read_text()
assert job(ex)["status"] == "unavailable" and [x["model"] for x in job(ex)["attempts"]] == ["x", "y"]
assert "args 0" in (WD / ".r42" / "jobs" / f"{dm}.log").read_text(), "no models: drop -m {model}"

# every job produced exactly one event, numbered 1..n
events = [json.loads(l) for l in (WD / ".r42" / "events.jsonl").read_text().splitlines()]
assert sorted(e["job"] for e in events) == sorted(ALL)
assert [e["seq"] for e in events] == list(range(1, len(ALL) + 1))
assert next(e for e in events if e["job"] == fb)["model"] == "ok"

# unacked events are re-presented until acked
n = len(ALL)
assert len(r42("events").splitlines()) == n
assert len(r42("events").splitlines()) == n
r42("ack", str(n - 2))
assert [l.split()[0] for l in r42("events").splitlines()] == [f"#{n - 1}", f"#{n}"]
r42("ack", str(n))
assert r42("events") == ""
r42("ack", "1")  # ack never moves backwards
assert r42("events") == ""
assert subprocess.run([sys.executable, R42, "wait", "--timeout", "1"], cwd=WD).returncode == 3  # idle
print("r42 self-check passed")
