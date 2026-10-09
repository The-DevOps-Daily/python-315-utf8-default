# python-315-utf8-default

Python 3.15 turns on UTF-8 mode by default (PEP 686). This repo runs the same
13 cases on Python 3.14 and 3.15 in seven Linux locales and records what
changes, then gives you a checker for your own code.

```bash
./scripts/setup.sh                 # uv installs 3.14.8 and 3.15.0; localedef builds ./locales
python3 scripts/run_matrix.py      # 308 runs, about 2 minutes, writes results/matrix.json
python3 scripts/summarize.py       # results/summary.md, one table per case
python3 scripts/check_claim.py     # results/claim-check.txt, CLAIM.md checked against the runs
./scripts/consumers.sh             # what jq and node do with the JSON that 3.15 writes
./scripts/fixes.sh                 # the fixes from the post, run on 3.15
./scripts/checker_vs_runtime.sh    # the checker against -X warn_default_encoding on examples/
```

Needs Linux with glibc (for `localedef`) and [uv](https://docs.astral.sh/uv/).
Set `PY314` and `PY315` to interpreter paths to skip uv. Windows is not
tested; on Windows the locale encoding is the ANSI code page, so `open()` with
no `encoding` changes for almost every user there.

The write-up is on DevOps Daily.

## Check your own code

```bash
python3 check_default_encoding.py src/ scripts/
```

It reports every call that uses the default text encoding: `open()`,
`Path.read_text()` and `write_text()`, `Path.open()`, `subprocess` with
`text=True` and no `encoding`, `os.popen()`, logging file handlers,
`tempfile` in text mode, `gzip.open()` in text mode, `os.fdopen()`,
`io.TextIOWrapper()` and `locale.getpreferredencoding()`. Exit status 1 means
it found something. It is a static check, so also run your tests once with
`python -X warn_default_encoding -W error::EncodingWarning`, which catches
calls made through variables and wrappers. `tests/test_checker.py` holds the
cases it must and must not report (`python3 -m unittest tests/test_checker.py`).
On `examples/release_notes.py`, the checker and the runtime warning report the
same 6 lines (`results/checker-example.txt`).

## What the cases do

| Case | What it does |
| --- | --- |
| `probe` | UTF-8 mode, locale encoding, stdin and stdout encoding and error handler |
| `read_latin1` | `open()` on an ISO-8859-1 file |
| `read_latin1_locale` | the same with `encoding="locale"` |
| `read_utf8` | `open()` on a UTF-8 file |
| `write_text` | `open("w")` writing `café 25€` |
| `subprocess_latin1`, `subprocess_utf8` | `subprocess.run(text=True)` on a child that prints ISO-8859-1 or UTF-8 |
| `environ_argv` | an ISO-8859-1 value in `os.environ` and `sys.argv`, then encoded as UTF-8 |
| `stdin_latin1`, `stdin_utf8` | `sys.stdin.read()` on ISO-8859-1 or UTF-8 bytes |
| `stdin_to_json` | ISO-8859-1 bytes on stdin turned into a JSON line |
| `stdout_filename` | printing a file name that is not valid UTF-8 |
| `stdout_utf8` | printing `café 25€` |
| `encoding_warning` | which calls `-X warn_default_encoding` reports |
| `handoff` | 3.15 writes a file and 3.14 reads it on the same host, and the other way round |

Every run starts from an empty environment with only `PATH`, `LOCPATH` and the
locale variables, so your shell settings do not leak in. The runner stops if a
locale does not report the encoding it should, so a missing locale cannot pass
as a result. `CLAIM.md` is the claim as written before the runs, with what the
runs said.

## Results

See [`results/summary.md`](results/summary.md) for every table and
[`CLAIM.md`](CLAIM.md) for which parts of the claim held.
