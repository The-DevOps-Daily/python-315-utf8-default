# Write "café 25€" with no encoding, then report the bytes on disk.
import sys

from _result import attempt, record

path = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2] + "/written.txt"


def write():
    with open(path, "w") as f:
        f.write("café 25€\n")
    with open(path, "rb") as f:
        return f.read()


record(outcome=attempt(write))
