# Same file, with the escape hatch PEP 597 added in 3.10: encoding="locale".
import sys

from _result import attempt, record

path = sys.argv[2] + "/latin1.txt"
record(outcome=attempt(lambda: open(path, encoding="locale").read()))
