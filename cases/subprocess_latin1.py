# A child process that prints ISO-8859-1 bytes, read with text=True.
import subprocess

from _result import attempt, record

record(outcome=attempt(lambda: subprocess.run(
    ["printf", "caf\\351\\n"], capture_output=True, text=True, check=True).stdout))
