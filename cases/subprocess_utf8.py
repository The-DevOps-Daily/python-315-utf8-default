# A child process that prints UTF-8 bytes, read with text=True.
import subprocess

from _result import attempt, record

record(outcome=attempt(lambda: subprocess.run(
    ["printf", "caf\\303\\251 25\\342\\202\\254\\n"], capture_output=True, text=True, check=True).stdout))
