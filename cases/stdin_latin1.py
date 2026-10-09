# The runner pipes b"caf\xe9\n" (ISO-8859-1) into stdin.
import sys

from _result import attempt, record

record(outcome=attempt(lambda: sys.stdin.read()))
