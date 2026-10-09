#!/usr/bin/env python3
"""Run every case in cases/ on Python 3.14 and 3.15, each with its default and
with PYTHONUTF8=0, in seven locales, and write results/matrix.json.

Each run starts from an empty environment (only PATH, LOCPATH and the locale
variables), so nothing from your shell leaks in.
"""
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "cases"
RESULTS = ROOT / "results"
LOCPATH = ROOT / "locales"

VERSIONS = {"3.14": os.environ.get("PY314_VERSION", "3.14.8"),
            "3.15": os.environ.get("PY315_VERSION", "3.15.0")}

# label, locale variables, the locale encoding the probe must report (None: not checked)
LOCALES = [
    ("no locale", {}, None),
    ("LANG=C", {"LANG": "C"}, None),
    ("LC_ALL=C", {"LC_ALL": "C"}, None),
    ("LANG=C.UTF-8", {"LANG": "C.UTF-8"}, "UTF-8"),
    ("LANG=en_US.UTF-8", {"LANG": "en_US.UTF-8"}, "UTF-8"),
    ("LANG=en_US", {"LANG": "en_US"}, "ISO-8859-1"),
    ("LANG=ja_JP.eucJP", {"LANG": "ja_JP.eucJP"}, "EUC-JP"),
]


LATIN1 = b"caf\xe9"
CASE_SPECS = {
    "probe": {},
    "read_latin1": {},
    "read_latin1_locale": {},
    "read_utf8": {},
    "write_text": {},
    "subprocess_latin1": {},
    "subprocess_utf8": {},
    "environ_argv": {"env": {b"DEMO_LATIN1": LATIN1}, "argv": [LATIN1]},
    "stdin_latin1": {"stdin": LATIN1 + b"\n"},
    "stdin_to_json": {"stdin": LATIN1 + b"\n"},
    "stdin_utf8": {"stdin": "café 25€\n".encode("utf-8")},
    "stdout_filename": {"stdout": True},
    "stdout_utf8": {"stdout": True},
    "encoding_warning": {"flags": ["-X", "warn_default_encoding"]},
}

FIXTURES = {
    "latin1.txt": "café naïve résumé\n".encode("latin-1"),
    "utf8.txt": "café 25€ ✓\n".encode("utf-8"),
    "ascii.txt": b"plain ascii\n",
}


def find_python(minor):
    override = os.environ.get("PY" + minor.replace(".", ""))
    if override:
        return override
    out = subprocess.run(["uv", "python", "find", VERSIONS[minor]],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return out.stdout.strip()


def columns():
    py314, py315 = find_python("3.14"), find_python("3.15")
    off = {b"PYTHONUTF8": b"0"}
    return [("3.14", py314, {}), ("3.15", py315, {}),
            ("3.15 + PYTHONUTF8=0", py315, off), ("3.14 + PYTHONUTF8=0", py314, off)]


def base_env(locale_vars):
    env = {b"PATH": b"/usr/bin:/bin", b"LOCPATH": os.fsencode(LOCPATH),
           b"PYTHONDONTWRITEBYTECODE": b"1"}
    for key, value in locale_vars.items():
        env[key.encode()] = value.encode()
    return env


LAUNCHES = 0


def run_case(case, python, extra_env, locale_vars, workdir, argv_tail=()):
    global LAUNCHES
    LAUNCHES += 1
    spec = CASE_SPECS.get(case, {})
    result_path = Path(workdir) / f"{case}.json"
    env = base_env(locale_vars)
    env.update(extra_env)
    env.update(spec.get("env", {}))
    cmd = [python, "-s", "-B", *spec.get("flags", []), str(CASES / f"{case}.py"),
           str(result_path), str(workdir), *spec.get("argv", []), *argv_tail]
    proc = subprocess.run(cmd, env=env, input=spec.get("stdin"),
                          stdin=None if spec.get("stdin") else subprocess.DEVNULL,
                          capture_output=True, timeout=60)
    row = {"exit": proc.returncode,
           "result": json.loads(result_path.read_bytes()) if result_path.exists() else None}
    if spec.get("stdout"):
        row["stdout"] = ascii(proc.stdout)
    if proc.returncode != 0:
        lines = proc.stderr.decode("utf-8", "backslashreplace").strip().splitlines()
        # keep local paths out of the committed results
        row["stderr_tail"] = (lines[-1] if lines else "").replace(str(workdir), "<workdir>")
    return row


def fresh_workdir():
    work = Path(tempfile.mkdtemp(prefix="run-", dir=ROOT / "work"))
    for name, data in FIXTURES.items():
        (work / name).write_bytes(data)
    return work


def main():
    (ROOT / "work").mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    cols = columns()
    rows = []
    for label, locale_vars, expected in LOCALES:
        for col_label, python, extra in cols:
            for case in CASE_SPECS:
                work = fresh_workdir()
                try:
                    row = run_case(case, python, extra, locale_vars, work)
                finally:
                    shutil.rmtree(work)
                if case == "probe" and expected:
                    got = (row["result"] or {}).get("locale_encoding")
                    if got != expected:
                        sys.exit(f"{label} on {col_label}: locale encoding is {got}, "
                                 f"expected {expected}. Run scripts/setup.sh first.")
                rows.append({"case": case, "locale": label, "column": col_label, **row})

        # One host, two versions: a file written by one is read by the other.
        for writer, reader in ((cols[1], cols[0]), (cols[0], cols[1])):
            work = fresh_workdir()
            try:
                target = str(work / "handoff.txt")
                w = run_case("write_text", writer[1], writer[2], locale_vars, work, [target])
                r = run_case("read_utf8", reader[1], reader[2], locale_vars, work, [target])
            finally:
                shutil.rmtree(work)
            rows.append({"case": "handoff", "locale": label,
                         "column": f"{writer[0]} writes, {reader[0]} reads",
                         "exit": max(w["exit"], r["exit"]),
                         "result": {"written": (w["result"] or {}).get("outcome"),
                                    "read": (r["result"] or {}).get("outcome")}})

    (RESULTS / "matrix.json").write_text(json.dumps(rows, indent=1, ensure_ascii=True) + "\n",
                                         encoding="utf-8")
    probe = {r["column"]: r["result"]["version"] for r in rows if r["case"] == "probe"}
    env_lines = [
        f"date_utc={datetime.now(timezone.utc).date().isoformat()}",
        f"machine={platform.machine()}",
        f"system={platform.system()}",
        f"libc={os.confstr('CS_GNU_LIBC_VERSION')}",
        f"python_3.14={probe['3.14']}",
        f"python_3.15={probe['3.15']}",
        f"results={len(rows)}",
        f"interpreter_runs={LAUNCHES}",
    ]
    (RESULTS / "environment.txt").write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} results from {LAUNCHES} interpreter runs written to results/matrix.json")


if __name__ == "__main__":
    main()
