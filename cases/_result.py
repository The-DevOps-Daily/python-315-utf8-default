"""Shared by every case: run a step, describe what happened, write one JSON file.

The runner passes the result path as argv[1]. The JSON is written as ASCII
bytes, so the result never depends on the encoding under test.
"""
import json
import sys


def attempt(fn):
    try:
        return "ok " + ascii(fn())
    except Exception as exc:  # the error is the measurement
        return f"{type(exc).__name__}: {exc}"


def record(**fields):
    with open(sys.argv[1], "wb") as out:
        out.write(json.dumps(fields, ensure_ascii=True, sort_keys=True).encode("ascii"))
