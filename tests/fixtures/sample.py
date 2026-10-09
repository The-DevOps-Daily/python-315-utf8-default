# Fixture for tests/test_checker.py. A line ending in "# expect" must be
# reported; every other line must not be. Never imported or run.
import codecs
import gzip
import io
import locale
import logging
import logging.handlers
import os
import pathlib
import subprocess
import subprocess as sp
import tempfile
from logging.handlers import RotatingFileHandler
from pathlib import Path
from subprocess import check_output

open("a.txt")  # expect
open("a.txt", "w")  # expect
open("a.txt", mode="r+")  # expect
open("a.txt", "rb")
open("a.txt", mode="wb")
open("a.txt", encoding="utf-8")
open("a.txt", "r", -1, "utf-8")
open("a.txt", encoding="locale")
open("a.txt", **{"encoding": "utf-8"})
open("a.txt", MODE)  # expect
io.open("a.txt")  # expect
codecs.open("a.txt", "r")  # expect
codecs.open("a.txt", "r", "utf-8")
os.fdopen(3, "w")  # expect
os.fdopen(3, "wb")
io.TextIOWrapper(buf)  # expect
io.TextIOWrapper(buf, "utf-8")
gzip.open("a.gz", "rt")  # expect
gzip.open("a.gz")
gzip.open("a.gz", "rt", encoding="utf-8")
os.popen("ls")  # expect
locale.getpreferredencoding()  # expect
locale.getencoding()

Path("a.txt").read_text()  # expect
Path("a.txt").read_text("utf-8")
pathlib.Path("a.txt").write_text("x")  # expect
Path("a.txt").write_text("x", encoding="utf-8")
Path("a.txt").open()  # expect
Path("a.txt").open("rb")
Path("a.txt").open("w", -1, "utf-8")
cfg_path.read_text()  # expect
archive.open("member")

subprocess.run(["ls"], text=True)  # expect
subprocess.run(["ls"], universal_newlines=True)  # expect
subprocess.run(["ls"], text=True, encoding="utf-8")
subprocess.run(["ls"])
subprocess.run(["ls"], text=False)
sp.Popen(["ls"], text=True)  # expect
check_output(["ls"], text=True)  # expect
subprocess.getoutput("ls")  # expect

logging.FileHandler("app.log")  # expect
logging.FileHandler("app.log", "a", "utf-8")
logging.handlers.RotatingFileHandler("app.log", maxBytes=1)  # expect
RotatingFileHandler("app.log", encoding="utf-8")
logging.basicConfig(filename="app.log")  # expect
logging.basicConfig(filename="app.log", encoding="utf-8")
logging.basicConfig(level=10)

tempfile.NamedTemporaryFile("w")  # expect
tempfile.NamedTemporaryFile()
tempfile.TemporaryFile(mode="w+", encoding="utf-8")
