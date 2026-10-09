# The claim, written before the matrix ran

Python 3.15 turns on UTF-8 mode by default (PEP 686). On Linux, that is a
smaller change for `open()` than it sounds, and a bigger one for stdin and
stdout than most notes on the release say.

1. **Containers with no locale, `LANG=C` or `LC_ALL=C`:** nothing changes.
   Python 3.7 and later already turn UTF-8 mode on in the C and POSIX
   locales, so 3.14 and 3.15 give the same result in every case.
2. **UTF-8 locales (`C.UTF-8`, which the official python images set, and
   `en_US.UTF-8`):** `open()` with no `encoding` gives the same result, because
   the locale encoding was UTF-8 already. What changes is the error handler on
   stdin and stdout: 3.14 uses `strict`, 3.15 uses `surrogateescape`. Bytes
   that are not valid UTF-8 crash a 3.14 script on stdin or stdout and pass
   through on 3.15.
3. **Legacy locales (`LANG=en_US` is ISO-8859-1 on glibc, `ja_JP.eucJP`):**
   everything that uses the default encoding changes: reading and writing
   files, `subprocess` with `text=True`, environment variables, argv and file
   names.
4. `PYTHONUTF8=0` on 3.15 gives the 3.14 result back in every case.
5. `-X warn_default_encoding` finds the same calls on 3.14 and 3.15, so you can
   run it before you upgrade.

What would prove it wrong:

- Any case where 3.14 and 3.15 differ in a C, POSIX or no-locale run.
- Any `open()`, `subprocess` or environment case where 3.14 and 3.15 differ in
  a UTF-8 locale.
- A stdin or stdout case with bytes that are not valid UTF-8 where 3.14 and
  3.15 agree in a UTF-8 locale.
- A case where `PYTHONUTF8=0` on 3.15 does not match 3.14.

Windows is not tested here. The PEP says the change "mostly affects Windows
users", because there the locale encoding is the ANSI code page (for example
cp1252), so `open()` with no `encoding` changes for almost everyone.

## What the runs said

Recorded in `results/` on Linux aarch64, glibc 2.36, Python 3.14.8 and 3.15.0.
`results/claim-check.txt` is the machine check of each line below.

1. **Held.** With no locale, `LANG=C` and `LC_ALL=C`, 3.14 and 3.15 agree in
   all 13 cases.
2. **Half held.** In `en_US.UTF-8`, `open()`, `subprocess` and the environment
   cases agree, and the three cases with invalid UTF-8 on stdin or stdout
   differ. **Wrong for `C.UTF-8`:** 3.14 already uses `surrogateescape` on
   stdin and stdout there, because `C.UTF-8` is the locale Python coerces `C`
   to, so nothing differs in that locale either.
3. **Held.** In `LANG=en_US` (ISO-8859-1), 11 of 13 cases differ: five get
   better (UTF-8 data), five get worse (ISO-8859-1 data), and one prints the
   same bytes by a different route. In `ja_JP.eucJP`, 10 of 13 differ.
4. **Wrong.** With `LC_ALL=C`, 3.15 with `PYTHONUTF8=0` falls back to ASCII.
   3.14 never did that: it turns UTF-8 mode on by itself in the C locale. 7 of
   13 cases differ from 3.14, and 4 that worked on 3.14 raise. `PYTHONUTF8=0`
   means "off", not "what 3.14 did".
5. **Held.** `-X warn_default_encoding` reported the same 4 calls on 3.14 and
   3.15.
