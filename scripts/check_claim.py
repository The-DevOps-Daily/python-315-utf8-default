#!/usr/bin/env python3
"""Check CLAIM.md against results/matrix.json and write results/claim-check.txt."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

C_LOCALES = ["no locale", "LANG=C", "LC_ALL=C"]
UTF8_LOCALES = ["LANG=C.UTF-8", "LANG=en_US.UTF-8"]
LEGACY_LOCALES = ["LANG=en_US", "LANG=ja_JP.eucJP"]
STDIO_CASES = {"stdin_latin1", "stdin_to_json", "stdout_filename"}  # invalid UTF-8 on stdin or stdout
# cases that name their encoding or only count warnings, so the locale should not matter
LOCALE_INDEPENDENT = {"read_latin1_locale", "encoding_warning"}


def outcome(row):
    """What a run did, without the parts that differ by design (the version)."""
    res = dict(row["result"] or {})
    res.pop("version", None)
    return json.dumps([row["exit"], res, row.get("stdout"), row.get("stderr_tail")],
                      sort_keys=True)


def main():
    rows = [r for r in json.loads((RESULTS / "matrix.json").read_text(encoding="utf-8"))
            if r["case"] != "handoff"]
    index = {(r["case"], r["locale"], r["column"]): r for r in rows}
    # "probe" reports settings, not behaviour, so it is left out of every check
    cases = [c for c in dict.fromkeys(r["case"] for r in rows) if c != "probe"]

    def differ(locale, a="3.14", b="3.15"):
        return [c for c in cases
                if outcome(index[(c, locale, a)]) != outcome(index[(c, locale, b)])]

    lines = []

    def check(ok, text, detail=""):
        lines.append(f"{'PASS' if ok else 'FAIL'}  {text}" + (f"\n      {detail}" if detail else ""))

    for loc in C_LOCALES:
        d = differ(loc)
        check(not d, f"{loc}: 3.14 and 3.15 agree in every case", ", ".join(d))
    for loc in UTF8_LOCALES:
        d = set(differ(loc))
        check(not (d - STDIO_CASES),
              f"{loc}: open(), subprocess and environment cases agree", ", ".join(sorted(d)))
        check(STDIO_CASES <= d,
              f"{loc}: invalid UTF-8 on stdin/stdout differs between 3.14 and 3.15",
              "differs: " + (", ".join(sorted(d)) or "nothing"))
    for loc in LEGACY_LOCALES:
        d = differ(loc)
        same = [c for c in cases if c not in d]
        check(set(same) <= LOCALE_INDEPENDENT,
              f"{loc}: every case that uses the default encoding differs ({len(d)} of {len(cases)})",
              "agree: " + ", ".join(same))
    everywhere = C_LOCALES + UTF8_LOCALES + LEGACY_LOCALES
    mismatches = [f"{loc}: {c}" for loc in everywhere
                  for c in differ(loc, "3.14", "3.15 + PYTHONUTF8=0")]
    check(not mismatches, "3.15 + PYTHONUTF8=0 gives the 3.14 default result in every case",
          "; ".join(mismatches))
    mismatches = [f"{loc}: {c}" for loc in everywhere
                  for c in differ(loc, "3.14 + PYTHONUTF8=0", "3.15 + PYTHONUTF8=0")]
    check(not mismatches, "PYTHONUTF8=0 gives the same result on 3.14 and 3.15 in every case",
          "; ".join(mismatches))
    warn = {r["column"]: r["result"]["warnings"] for r in rows
            if r["case"] == "encoding_warning" and r["locale"] == "LANG=en_US.UTF-8"}
    check(warn["3.14"] == warn["3.15"] and len(warn["3.14"]) == 4,
          "-X warn_default_encoding reports the same 4 calls on 3.14 and 3.15")

    (RESULTS / "claim-check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
