# Run with -X warn_default_encoding. Each call in the block uses the default
# encoding; the result lists which ones raised EncodingWarning.
import linecache
import locale
import pathlib
import subprocess
import sys
import warnings

from _result import record

path = sys.argv[2] + "/ascii.txt"
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    open(path).close()
    pathlib.Path(path).read_text()
    subprocess.run(["true"], capture_output=True, text=True)
    locale.getpreferredencoding()
record(
    flag=sys.flags.warn_default_encoding,
    warnings=[f"{linecache.getline(w.filename, w.lineno).strip()} [{w.category.__name__}]"
              for w in caught],
)
