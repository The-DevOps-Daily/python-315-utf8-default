# The runner pipes "café 25€\n" as UTF-8 into stdin.
import sys

from _result import attempt, record

record(outcome=attempt(lambda: sys.stdin.read()))
