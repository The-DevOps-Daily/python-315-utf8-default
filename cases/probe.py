import locale
import os
import sys

from _result import record

record(
    version=sys.version.split()[0],
    utf8_mode=sys.flags.utf8_mode,
    lc_ctype=locale.setlocale(locale.LC_CTYPE),
    lc_ctype_env=os.environ.get("LC_CTYPE"),
    locale_encoding=locale.getencoding(),
    preferred_encoding=locale.getpreferredencoding(False),
    filesystem_encoding=sys.getfilesystemencoding(),
    stdin=f"{sys.stdin.encoding}/{sys.stdin.errors}",
    stdout=f"{sys.stdout.encoding}/{sys.stdout.errors}",
)
