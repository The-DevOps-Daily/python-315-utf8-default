#!/usr/bin/env python3
"""Turn results/matrix.json into results/summary.md: one table per case,
locales down the side, interpreters across the top."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

TITLES = {
    "probe": "What each interpreter picks (UTF-8 mode, locale encoding, stdout)",
    "read_latin1": "open() with no encoding on an ISO-8859-1 file",
    "read_latin1_locale": "open(encoding=\"locale\") on the same file",
    "read_utf8": "open() with no encoding on a UTF-8 file",
    "write_text": "open(\"w\") with no encoding, writing \"café 25€\"",
    "handoff": "One host, two versions: one writes the file, the other reads it",
    "subprocess_latin1": "subprocess.run(text=True) on a child that prints ISO-8859-1",
    "subprocess_utf8": "subprocess.run(text=True) on a child that prints UTF-8",
    "environ_argv": "An ISO-8859-1 value in os.environ and sys.argv, then encoded as UTF-8",
    "stdin_latin1": "ISO-8859-1 bytes on stdin",
    "stdin_to_json": "ISO-8859-1 bytes on stdin, turned into JSON with json.dumps defaults",
    "stdin_utf8": "UTF-8 bytes on stdin",
    "stdout_filename": "Printing a file name that is not valid UTF-8",
    "stdout_utf8": "Printing \"café 25€\"",
    "encoding_warning": "-X warn_default_encoding: calls that raised EncodingWarning",
}


def cell(row):
    res = row["result"]
    case = row["case"]
    if not res:
        return f"exit {row['exit']}; {row.get('stderr_tail', '')}"
    if case == "probe":
        return (f"utf8_mode={res['utf8_mode']}, locale {res['locale_encoding']}, "
                f"stdout {res['stdout']}")
    if "stdout" in row:
        text = f"exit {row['exit']}, wrote {row['stdout']}"
        if "listdir" in res:
            text = f"listdir {res['listdir']}; " + text
        if row["exit"]:
            text += f"; {row.get('stderr_tail', '')}"
        return text
    if case == "environ_argv":
        return f"environ {res['environ']}, argv {res['argv']}; encode: {res['to_utf8']}"
    if case == "encoding_warning":
        return f"{len(res['warnings'])} of 4"
    if case == "handoff":
        return f"wrote {res['written']}; read {res['read']}"
    if res.get("outcome"):
        return res["outcome"]
    return f"exit {row['exit']}; {row.get('stderr_tail', '')}"


def md(text):
    return "`" + text.replace("|", "\\|").replace("`", "'") + "`"


def main():
    rows = json.loads((RESULTS / "matrix.json").read_text(encoding="utf-8"))
    env = (RESULTS / "environment.txt").read_text(encoding="utf-8").strip()
    out = ["# Results", "", "Recorded by `scripts/run_matrix.py`:", "", "```text", env,
           "```", ""]
    cases = list(dict.fromkeys(r["case"] for r in rows))
    for case in cases:
        sub = [r for r in rows if r["case"] == case]
        cols = list(dict.fromkeys(r["column"] for r in sub))
        locales = list(dict.fromkeys(r["locale"] for r in sub))
        out += [f"## {case}", "", TITLES.get(case, case) + ".", "",
                "| Locale | " + " | ".join(cols) + " |",
                "| --- |" + " --- |" * len(cols)]
        for loc in locales:
            by_col = {r["column"]: r for r in sub if r["locale"] == loc}
            out.append(f"| {loc} | " + " | ".join(md(cell(by_col[c])) for c in cols) + " |")
        out.append("")
    (RESULTS / "summary.md").write_text("\n".join(out), encoding="utf-8")
    print(f"results/summary.md: {len(cases)} tables")


if __name__ == "__main__":
    main()
