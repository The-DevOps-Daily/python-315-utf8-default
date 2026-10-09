# A UTF-8 file ("café 25€ ✓\n"), or the file named in argv[3].
import sys

from _result import attempt, record

path = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2] + "/utf8.txt"
record(outcome=attempt(lambda: open(path).read()))
