# Results

Recorded by `scripts/run_matrix.py`:

```text
date_utc=2026-10-09
machine=aarch64
system=Linux
libc=glibc 2.36
python_3.14=3.14.8
python_3.15=3.15.0
runs=308
```

## probe

What each interpreter picks (UTF-8 mode, locale encoding, stdout).

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=0, locale UTF-8, stdout utf-8/surrogateescape` |
| LANG=C | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=0, locale UTF-8, stdout utf-8/surrogateescape` |
| LC_ALL=C | `utf8_mode=1, locale ANSI_X3.4-1968, stdout utf-8/surrogateescape` | `utf8_mode=1, locale ANSI_X3.4-1968, stdout utf-8/surrogateescape` | `utf8_mode=0, locale ANSI_X3.4-1968, stdout ascii/surrogateescape` |
| LANG=C.UTF-8 | `utf8_mode=0, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=0, locale UTF-8, stdout utf-8/surrogateescape` |
| LANG=en_US.UTF-8 | `utf8_mode=0, locale UTF-8, stdout utf-8/strict` | `utf8_mode=1, locale UTF-8, stdout utf-8/surrogateescape` | `utf8_mode=0, locale UTF-8, stdout utf-8/strict` |
| LANG=en_US | `utf8_mode=0, locale ISO-8859-1, stdout iso8859-1/strict` | `utf8_mode=1, locale ISO-8859-1, stdout utf-8/surrogateescape` | `utf8_mode=0, locale ISO-8859-1, stdout iso8859-1/strict` |
| LANG=ja_JP.eucJP | `utf8_mode=0, locale EUC-JP, stdout euc_jp/strict` | `utf8_mode=1, locale EUC-JP, stdout utf-8/surrogateescape` | `utf8_mode=0, locale EUC-JP, stdout euc_jp/strict` |

## read_latin1

open() with no encoding on an ISO-8859-1 file.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=C | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LC_ALL=C | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US | `ok 'caf\xe9 na\xefve r\xe9sum\xe9\n'` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `ok 'caf\xe9 na\xefve r\xe9sum\xe9\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` |

## read_latin1_locale

open(encoding="locale") on the same file.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=C | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LC_ALL=C | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US | `ok 'caf\xe9 na\xefve r\xe9sum\xe9\n'` | `ok 'caf\xe9 na\xefve r\xe9sum\xe9\n'` | `ok 'caf\xe9 na\xefve r\xe9sum\xe9\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` |

## read_utf8

open() with no encoding on a UTF-8 file.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` |
| LANG=C | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` |
| LC_ALL=C | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` |
| LANG=en_US.UTF-8 | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` |
| LANG=en_US | `ok 'caf\xc3\xa9 25\xe2\x82\xac \xe2\x9c\x93\n'` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `ok 'caf\xc3\xa9 25\xe2\x82\xac \xe2\x9c\x93\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` | `ok 'caf\xe9 25\u20ac \u2713\n'` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` |

## write_text

open("w") with no encoding, writing "café 25€".

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=C | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LC_ALL=C | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=en_US.UTF-8 | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=en_US | `UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 7: ordinal not in range(256)` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 7: ordinal not in range(256)` |
| LANG=ja_JP.eucJP | `UnicodeEncodeError: 'euc_jp' codec can't encode character '\u20ac' in position 7: illegal multibyte sequence` | `ok b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `UnicodeEncodeError: 'euc_jp' codec can't encode character '\u20ac' in position 7: illegal multibyte sequence` |

## subprocess_latin1

subprocess.run(text=True) on a child that prints ISO-8859-1.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=C | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LC_ALL=C | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US | `ok 'caf\xe9\n'` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `ok 'caf\xe9\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` |

## subprocess_utf8

subprocess.run(text=True) on a child that prints UTF-8.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=C | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LC_ALL=C | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US.UTF-8 | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US | `ok 'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` | `ok 'caf\xe9 25\u20ac\n'` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` |

## environ_argv

An ISO-8859-1 value in os.environ and sys.argv, then encoded as UTF-8.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |
| LANG=C | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |
| LC_ALL=C | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |
| LANG=C.UTF-8 | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |
| LANG=en_US.UTF-8 | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |
| LANG=en_US | `environ 'caf\xe9', argv 'caf\xe9'; encode: ok b'{"name": "caf\xc3\xa9"}'` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\xe9', argv 'caf\xe9'; encode: ok b'{"name": "caf\xc3\xa9"}'` |
| LANG=ja_JP.eucJP | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` | `environ 'caf\udce9', argv 'caf\udce9'; encode: UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 13: surrogates not allowed` |

## stdin_latin1

ISO-8859-1 bytes on stdin.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` |
| LANG=C | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` |
| LC_ALL=C | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` |
| LANG=C.UTF-8 | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` | `ok 'caf\udce9\n'` |
| LANG=en_US.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `ok 'caf\udce9\n'` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US | `ok 'caf\xe9\n'` | `ok 'caf\udce9\n'` | `ok 'caf\xe9\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `ok 'caf\udce9\n'` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` |

## stdin_to_json

ISO-8859-1 bytes on stdin, turned into JSON with json.dumps defaults.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` |
| LANG=C | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` |
| LC_ALL=C | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` |
| LANG=C.UTF-8 | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` |
| LANG=en_US.UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` | `ok b'{"line": "caf\\udce9\\n"}'` | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte` |
| LANG=en_US | `ok b'{"line": "caf\\u00e9\\n"}'` | `ok b'{"line": "caf\\udce9\\n"}'` | `ok b'{"line": "caf\\u00e9\\n"}'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` | `ok b'{"line": "caf\\udce9\\n"}'` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe9 in position 3: illegal multibyte sequence` |

## stdin_utf8

UTF-8 bytes on stdin.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=C | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LC_ALL=C | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\udcc3\udca9 25\udce2\udc82\udcac\n'` |
| LANG=C.UTF-8 | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US.UTF-8 | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US | `ok 'caf\xc3\xa9 25\xe2\x82\xac\n'` | `ok 'caf\xe9 25\u20ac\n'` | `ok 'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=ja_JP.eucJP | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` | `ok 'caf\xe9 25\u20ac\n'` | `UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` |

## stdout_filename

Printing a file name that is not valid UTF-8.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` |
| LANG=C | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` |
| LC_ALL=C | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` |
| LANG=C.UTF-8 | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` |
| LANG=en_US.UTF-8 | `exit 1, wrote b''; UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 7: surrogates not allowed` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 1, wrote b''; UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 7: surrogates not allowed` |
| LANG=en_US | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 0, wrote b'report-\xe9.csv\n'` |
| LANG=ja_JP.eucJP | `exit 1, wrote b''; UnicodeEncodeError: 'euc_jp' codec can't encode character '\udce9' in position 7: illegal multibyte sequence` | `exit 0, wrote b'report-\xe9.csv\n'` | `exit 1, wrote b''; UnicodeEncodeError: 'euc_jp' codec can't encode character '\udce9' in position 7: illegal multibyte sequence` |

## stdout_utf8

Printing "café 25€".

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=C | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LC_ALL=C | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 1, wrote b''; UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)` |
| LANG=C.UTF-8 | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=en_US.UTF-8 | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` |
| LANG=en_US | `exit 1, wrote b''; UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 7: ordinal not in range(256)` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 1, wrote b''; UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 7: ordinal not in range(256)` |
| LANG=ja_JP.eucJP | `exit 1, wrote b''; UnicodeEncodeError: 'euc_jp' codec can't encode character '\u20ac' in position 7: illegal multibyte sequence` | `exit 0, wrote b'caf\xc3\xa9 25\xe2\x82\xac\n'` | `exit 1, wrote b''; UnicodeEncodeError: 'euc_jp' codec can't encode character '\u20ac' in position 7: illegal multibyte sequence` |

## encoding_warning

-X warn_default_encoding: calls that raised EncodingWarning.

| Locale | 3.14 | 3.15 | 3.15 + PYTHONUTF8=0 |
| --- | --- | --- | --- |
| no locale | `4 of 4` | `4 of 4` | `4 of 4` |
| LANG=C | `4 of 4` | `4 of 4` | `4 of 4` |
| LC_ALL=C | `4 of 4` | `4 of 4` | `4 of 4` |
| LANG=C.UTF-8 | `4 of 4` | `4 of 4` | `4 of 4` |
| LANG=en_US.UTF-8 | `4 of 4` | `4 of 4` | `4 of 4` |
| LANG=en_US | `4 of 4` | `4 of 4` | `4 of 4` |
| LANG=ja_JP.eucJP | `4 of 4` | `4 of 4` | `4 of 4` |

## handoff

One host, two versions: one writes the file, the other reads it.

| Locale | 3.15 writes, 3.14 reads | 3.14 writes, 3.15 reads |
| --- | --- | --- |
| no locale | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` |
| LANG=C | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` |
| LC_ALL=C | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` |
| LANG=C.UTF-8 | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US.UTF-8 | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xe9 25\u20ac\n'` |
| LANG=en_US | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read ok 'caf\xc3\xa9 25\xe2\x82\xac\n'` | `wrote UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 7: ordinal not in range(256); read ok ''` |
| LANG=ja_JP.eucJP | `wrote ok b'caf\xc3\xa9 25\xe2\x82\xac\n'; read UnicodeDecodeError: 'euc_jp' codec can't decode byte 0xe2 in position 8: illegal multibyte sequence` | `wrote UnicodeEncodeError: 'euc_jp' codec can't encode character '\u20ac' in position 7: illegal multibyte sequence; read ok ''` |
