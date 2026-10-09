# The runner sets DEMO_LATIN1=b"caf\xe9" and passes the same bytes as argv[3].
# Reading never fails: undecodable bytes become lone surrogates. The failure,
# if there is one, comes later, when the value is encoded as UTF-8 for a file,
# a JSON body or an HTTP header.
import json
import os
import sys

from _result import attempt, record

value = os.environ["DEMO_LATIN1"]
record(
    environ=ascii(value),
    argv=ascii(sys.argv[3]),
    to_utf8=attempt(lambda: json.dumps({"name": value}, ensure_ascii=False).encode("utf-8")),
)
