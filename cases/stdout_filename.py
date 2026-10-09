# A file name that is not valid UTF-8 (b"report-\xe9.csv", as a Latin-1 system
# would write it), listed and printed. The runner reads stdout and the exit code.
import os
import sys

from _result import record

folder = sys.argv[2] + "/names"
os.makedirs(folder, exist_ok=True)
fd = os.open(os.fsencode(folder) + b"/report-\xe9.csv", os.O_CREAT | os.O_WRONLY, 0o644)
os.close(fd)
names = os.listdir(folder)
record(listdir=ascii(names))
for name in names:
    print(name)
