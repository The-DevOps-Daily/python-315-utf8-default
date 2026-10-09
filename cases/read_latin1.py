# A file written by a legacy tool in ISO-8859-1: b"caf\xe9 na\xefve r\xe9sum\xe9\n"
import sys

from _result import attempt, record

path = sys.argv[2] + "/latin1.txt"
record(outcome=attempt(lambda: open(path).read()))
