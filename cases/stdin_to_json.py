# The runner pipes b"caf\xe9\n" (ISO-8859-1) into stdin. The script turns it
# into a JSON line with json.dumps defaults and writes it as UTF-8, the way a
# log shipper or an API client would.
import json
import sys

from _result import attempt, record

path = sys.argv[2] + "/out.json"


def convert():
    line = json.dumps({"line": sys.stdin.read()})
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "rb") as f:
        return f.read()


record(outcome=attempt(convert))
