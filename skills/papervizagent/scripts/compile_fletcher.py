#!/usr/bin/env python3
"""
Deterministic compiler, preflight verifier, Fletcher/CeTZ debug-overlay renderer,
and vector PDF/SVG/PNG exporter for the papervizagent skill.

Zero third-party dependencies (Python 3 standard library only).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


COMMON_TYPST_PATHS = [
    "/opt/homebrew/bin/typst",
    "/opt/homebrew/opt/typst/bin/typst",
    "/usr/local/bin/typst",
    os.path.expanduser("~/.cargo/bin/typst"),
    os.path.expanduser("~/.local/bin/typst"),
    os.path.expanduser("~/.nix-profile/bin/typst"),
]

PREFERRED_FONTS = [
    "Inter",
    "Helvetica Neue",
    "Helvetica",
    "Arial",
    "Roboto",
    "IBM Plex Sans",
    "Liberation Sans",
    "DejaVu Sans",
    "New Computer Modern",
    "Libertinus Serif",
    "Times New Roman",
]


def find_typst() -> str | None:
    """Locate the typst binary on PATH or common install locations."""
    found = shutil.which("typst")
    if found:
        return found
    for candidate in COMMON_TYPST_PATHS:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def find_cached_package_versions(pkg_name: str) -> list[str]:
    """Return sorted list of locally cached @preview/<pkg_name> versions."""
    cache_dirs: list[Path] = []
    if platform.system() == "Darwin":
        cache_dirs.append(Path.home() / "Library/Caches/typst/packages/preview" / pkg_name)
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        cache_dirs.append(Path(xdg) / "typst/packages/preview" / pkg_name)
    cache_dirs.append(Path.home() / ".cache/typst/packages/preview" / pkg_name)

    versions: set[str] = set()
    for d in cache_dirs:
        if d.is_dir():
            for child in d.iterdir():
                if child.is_dir() and re.match(r"^\d+\.\d+\.\d+$", child.name):
                    versions.add(child.name)

    def ver_key(v: str) -> tuple[int, ...]:
        return tuple(int(x) for x in v.split("."))

    return sorted(versions, key=ver_key, reverse=True)


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def check_env() -> dict[str, Any]:
    """Inspect Typst CLI, cached Fletcher/CeTZ/cetz-plot versions, and available fonts."""
    typst_bin = find_typst()
    fletcher_vers = find_cached_package_versions("fletcher")
    cetz_vers = find_cached_package_versions("cetz")
    cetz_plot_vers = find_cached_package_versions("cetz-plot")

    info: dict[str, Any] = {
        "typst_found": typst_bin is not None,
        "typst_path": typst_bin,
        "typst_version": None,
        "cached_fletcher_versions": fletcher_vers,
        "recommended_fletcher_version": fletcher_vers[0] if fletcher_vers else "0.5.8",
        "cached_cetz_versions": cetz_vers,
        "recommended_cetz_version": cetz_vers[0] if cetz_vers else "0.3.4",
        "cached_cetz_plot_versions": cetz_plot_vers,
        "available_preferred_fonts": [],
    }

    if typst_bin:
        ver = run_cmd([typst_bin, "--version"])
        if ver.returncode == 0:
            info["typst_version"] = ver.stdout.strip()
        fonts_proc = run_cmd([typst_bin, "fonts"])
        if fonts_proc.returncode == 0:
            installed = {line.strip() for line in fonts_proc.stdout.splitlines() if line.strip()}
            info["available_preferred_fonts"] = [f for f in PREFERRED_FONTS if f in installed]

    return info


def read_png_dimensions(png_path: Path) -> dict[str, Any] | None:
    """Parse width and height from a PNG file's IHDR chunk without external libraries."""
    try:
        with png_path.open("rb") as f:
            header = f.read(24)
        if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", header[16:24])
        ratio = round(width / height, 2) if height > 0 else 0.0
        return {"file": str(png_path), "width": width, "height": height, "aspect_ratio": ratio}
    except OSError:
        return None


def parse_typst_stderr(stderr: str, returncode: int = 0) -> tuple[list[str], list[str]]:
    """Split Typst stderr into warnings and errors, ignoring package download progress."""
    warnings: list[str] = []
    errors: list[str] = []
    current_bucket: list[str] | None = None
    buffer: list[str] = []

    progress_re = re.compile(r"^(downloading @|\s*\d+(\.\d+)?\s*[KMGT]?i?B\s*/)")

    def flush() -> None:
        nonlocal buffer, current_bucket
        if buffer and current_bucket is not None:
            current_bucket.append("\n".join(buffer).strip())
        buffer = []

    for line in stderr.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if progress_re.match(stripped):
            flush()
            current_bucket = None
            continue
        if line.startswith("warning:"):
            flush()
            current_bucket = warnings
            buffer = [line]
        elif line.startswith("error:"):
            flush()
            current_bucket = errors
            buffer = [line]
        elif current_bucket is not None:
            buffer.append(line)
        elif returncode != 0:
            errors.append(stripped)

    flush()
    return warnings, errors


def inject_debug_overlay(source: str, level: int) -> tuple[str, bool, str]:
    """
    Non-destructively inject debug visualization:
    - For Fletcher (`diagram(`): inject `debug: <level>,`
    - For standalone CeTZ (`cetz.canvas(`): inject a light 1-unit coordinate grid overlay
    Returns (patched_source, injected_bool, mode_name).
    """
    # Priority 1: Fletcher diagram()
    if re.search(r"#?(?:fletcher\.)?diagram\s*\(", source):
        existing_debug = re.search(r"(\bdebug\s*:\s*)\d+", source)
        if existing_debug:
            patched = re.sub(r"(\bdebug\s*:\s*)\d+", rf"\g<1>{level}", source, count=1)
            return patched, True, "fletcher"
        match = re.search(r"(#?(?:fletcher\.)?diagram\s*\()", source)
        if match:
            insert_pos = match.end()
            patched = source[:insert_pos] + f"\n  debug: {level}," + source[insert_pos:]
            return patched, True, "fletcher"

    # Priority 2: Standalone CeTZ canvas({ ... })
    canvas_match = re.search(r"(#?(?:cetz\.)?canvas\s*\([^{]*\{)", source)
    if canvas_match:
        insert_pos = canvas_match.end()
        step = "0.5" if level >= 3 else "1"
        overlay = (
            "\n  cetz.draw.on-layer(-99, {\n"
            f"    cetz.draw.grid((-1, -1), (18, 10), step: {step}, "
            "stroke: 0.25pt + rgb(\"#FCA5A5\"))\n"
            "    for x in range(0, 18) {\n"
            "      cetz.draw.content((x, -0.35), text(size: 5pt, fill: rgb(\"#EF4444\"))[#x])\n"
            "    }\n"
            "    for y in range(0, 10) {\n"
            "      cetz.draw.content((-0.35, y), text(size: 5pt, fill: rgb(\"#EF4444\"))[#y])\n"
            "    }\n"
            "  })\n"
        )
        patched = source[:insert_pos] + overlay + source[insert_pos:]
        return patched, True, "cetz"

    return source, False, "none"


def compile_pages_png(
    typst_bin: str,
    src_path: Path,
    out_dir: Path,
    prefix: str,
    ppi: int,
    root: str | None,
) -> tuple[bool, list[Path], list[str], list[str]]:
    """Compile a .typ file to numbered PNG pages (`<prefix>-{p}.png`) to detect overflow."""
    for old in out_dir.glob(f"{prefix}-*.png"):
        if re.match(rf"^{re.escape(prefix)}-\d+\.png$", old.name):
            old.unlink(missing_ok=True)

    template = str(out_dir / f"{prefix}-{{p}}.png")
    cmd = [typst_bin, "compile", str(src_path), template, "--ppi", str(ppi)]
    if root:
        cmd.extend(["--root", root])

    proc = run_cmd(cmd)
    warnings, errors = parse_typst_stderr(proc.stderr, proc.returncode)
    if proc.returncode != 0:
        if not errors and proc.stderr.strip():
            errors.append(proc.stderr.strip())
        return False, [], warnings, errors

    pages = sorted(
        (
            p
            for p in out_dir.glob(f"{prefix}-*.png")
            if re.match(rf"^{re.escape(prefix)}-\d+\.png$", p.name)
        ),
        key=lambda p: int(p.stem.rsplit("-", 1)[1]),
    )
    return True, pages, warnings, errors


def compile_single_format(
    typst_bin: str,
    src_path: Path,
    out_path: Path,
    fmt: str,
    ppi: int,
    root: str | None,
) -> tuple[bool, list[str], list[str]]:
    """Compile a .typ file to a single target format (pdf, svg, or png)."""
    cmd = [typst_bin, "compile", str(src_path), str(out_path)]
    if fmt == "png":
        cmd.extend(["--ppi", str(ppi)])
    elif fmt == "svg":
        cmd.extend(["--format", "svg"])
    elif fmt == "pdf":
        cmd.extend(["--format", "pdf"])
    if root:
        cmd.extend(["--root", root])

    proc = run_cmd(cmd)
    warnings, errors = parse_typst_stderr(proc.stderr, proc.returncode)
    if proc.returncode != 0:
        if not errors and proc.stderr.strip():
            errors.append(proc.stderr.strip())
        return False, warnings, errors
    return True, warnings, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile, preflight-check, debug-render, and export Typst (Fletcher / CeTZ) figures."
    )
    parser.add_argument("input", nargs="?", help="Path to the .typ figure file")
    parser.add_argument("--check-env", action="store_true", help="Check Typst binary, cached Fletcher/CeTZ, and fonts")
    parser.add_argument("--out-dir", type=str, default=None, help="Output directory (defaults to input parent)")
    parser.add_argument("--prefix", type=str, default=None, help="Output filename prefix (defaults to input stem)")
    parser.add_argument("--ppi", type=int, default=180, help="PNG render resolution in PPI (default: 180)")
    parser.add_argument(
        "--export",
        type=str,
        default="png",
        help="Comma-separated formats to compile: png,pdf,svg (default: png preview check)",
    )
    parser.add_argument(
        "--debug",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="Non-destructively inject Fletcher `debug: <level>` or CeTZ coordinate grid overlay into a temporary copy",
    )
    parser.add_argument("--root", type=str, default=None, help="Optional Typst --root directory")
    args = parser.parse_args()

    if args.check_env:
        info = check_env()
        print(json.dumps(info, indent=2))
        return 0 if info["typst_found"] else 1

    if not args.input:
        parser.error("Provide an input .typ file or pass --check-env")

    src_path = Path(args.input).resolve()
    if not src_path.is_file():
        print(json.dumps({"ok": False, "compile_ok": False, "errors": [f"Input file not found: {src_path}"]}, indent=2))
        return 1

    typst_bin = find_typst()
    if not typst_bin:
        print(
            json.dumps(
                {
                    "ok": False,
                    "compile_ok": False,
                    "errors": ["Typst CLI (`typst`) not found on PATH or standard install locations."],
                },
                indent=2,
            )
        )
        return 1

    out_dir = Path(args.out_dir).resolve() if args.out_dir else src_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or src_path.stem
    formats = [f.strip().lower() for f in args.export.split(",") if f.strip()]
    for fmt in formats:
        if fmt not in {"png", "pdf", "svg"}:
            print(json.dumps({"ok": False, "compile_ok": False, "errors": [f"Unsupported format: {fmt}"]}, indent=2))
            return 1

    all_warnings: list[str] = []
    all_errors: list[str] = []

    compile_ok, preview_pages, w, e = compile_pages_png(
        typst_bin=typst_bin,
        src_path=src_path,
        out_dir=out_dir,
        prefix=prefix,
        ppi=args.ppi,
        root=args.root,
    )
    all_warnings.extend(w)
    all_errors.extend(e)

    page_count = len(preview_pages)
    overflow = page_count > 1
    dimensions = [d for p in preview_pages if (d := read_png_dimensions(p)) is not None]

    exports: dict[str, str] = {}
    if compile_ok and page_count == 1:
        if "png" in formats:
            clean_png = out_dir / f"{prefix}.png"
            shutil.copy2(preview_pages[0], clean_png)
            exports["png"] = str(clean_png)

        for fmt in ("pdf", "svg"):
            if fmt in formats:
                target = out_dir / f"{prefix}.{fmt}"
                fmt_ok, fw, fe = compile_single_format(
                    typst_bin=typst_bin,
                    src_path=src_path,
                    out_path=target,
                    fmt=fmt,
                    ppi=args.ppi,
                    root=args.root,
                )
                all_warnings.extend(fw)
                all_errors.extend(fe)
                if fmt_ok:
                    exports[fmt] = str(target)
                else:
                    compile_ok = False

    debug_images: list[str] = []
    debug_injected = False
    debug_mode = "none"
    if args.debug > 0 and compile_ok:
        source_text = src_path.read_text(encoding="utf-8")
        patched_text, debug_injected, debug_mode = inject_debug_overlay(source_text, args.debug)
        if debug_injected:
            tmp_fd, tmp_name = tempfile.mkstemp(prefix=f".{prefix}_debug_", suffix=".typ", dir=src_path.parent)
            os.close(tmp_fd)
            tmp_path = Path(tmp_name)
            try:
                tmp_path.write_text(patched_text, encoding="utf-8")
                dbg_ok, dbg_pages, dw, de = compile_pages_png(
                    typst_bin=typst_bin,
                    src_path=tmp_path,
                    out_dir=out_dir,
                    prefix=f"{prefix}_debug",
                    ppi=args.ppi,
                    root=args.root,
                )
                all_warnings.extend(dw)
                if dbg_ok:
                    debug_images = [str(p) for p in dbg_pages]
                else:
                    all_errors.extend(de)
            finally:
                tmp_path.unlink(missing_ok=True)
        else:
            all_warnings.append("debug requested, but no `diagram(` or `cetz.canvas(` call was found in input .typ")

    dedup_warnings = list(dict.fromkeys(all_warnings))
    font_warnings = [w for w in dedup_warnings if "font" in w.lower()]

    ok = compile_ok and page_count == 1
    result: dict[str, Any] = {
        "ok": ok,
        "compile_ok": compile_ok,
        "page_count": page_count,
        "overflow": overflow,
        "preview_images": [str(p) for p in preview_pages],
        "dimensions": dimensions,
        "exports": exports,
        "debug_injected": debug_injected,
        "debug_mode": debug_mode,
        "debug_images": debug_images,
        "warnings": dedup_warnings,
        "font_warnings": font_warnings,
        "errors": all_errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
