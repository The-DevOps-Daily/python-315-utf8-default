#!/usr/bin/env bash
# The fixes the post recommends, run on 3.15 in the locales where they matter.
# Writes results/fixes.txt.
set -uo pipefail
cd "$(dirname "$0")/.."
PY315="${PY315:-$(uv python find "${PY315_VERSION:-3.15.0}")}"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
printf 'caf\303\251 25\342\202\254\n' > "$work/utf8.txt"

py() {  # py <locale assignments...> -- <python args...>
  local envs=()
  while [ "$1" != "--" ]; do envs+=("$1"); shift; done
  shift
  env -i PATH=/usr/bin:/bin LOCPATH="$PWD/locales" "${envs[@]}" "$PY315" "$@" 2>&1 | tail -1
}

{
  echo "## en_US.UTF-8, ISO-8859-1 byte on stdin: getting the 3.14 error back"
  echo "default:                      $(printf 'caf\351\n' | py LANG=en_US.UTF-8 -- -c 'import sys; print(ascii(sys.stdin.read()))')"
  echo "stdin.reconfigure(strict):    $(printf 'caf\351\n' | py LANG=en_US.UTF-8 -- -c 'import sys; sys.stdin.reconfigure(errors="strict"); print(ascii(sys.stdin.read()))')"
  echo "PYTHONIOENCODING=utf-8:strict $(printf 'caf\351\n' | py LANG=en_US.UTF-8 PYTHONIOENCODING=utf-8:strict -- -c 'import sys; print(ascii(sys.stdin.read()))')"
  echo "sys.stdin.buffer (bytes):     $(printf 'caf\351\n' | py LANG=en_US.UTF-8 -- -c 'import sys; print(sys.stdin.buffer.read())')"
  echo
  echo "## LC_ALL=C with PYTHONUTF8=0: reading a UTF-8 file"
  echo "no encoding:                  $(py LC_ALL=C PYTHONUTF8=0 -- -c "print(ascii(open('$work/utf8.txt').read()))")"
  echo "encoding=\"utf-8\":             $(py LC_ALL=C PYTHONUTF8=0 -- -c "print(ascii(open('$work/utf8.txt', encoding='utf-8').read()))")"
  echo
  echo "## LANG=en_US (ISO-8859-1): reading a legacy file on 3.15"
  printf 'caf\351\n' > "$work/latin1.txt"
  echo "no encoding:                  $(py LANG=en_US -- -c "print(ascii(open('$work/latin1.txt').read()))")"
  echo "encoding=\"latin-1\":           $(py LANG=en_US -- -c "print(ascii(open('$work/latin1.txt', encoding='latin-1').read()))")"
} | sed "s#$work#<workdir>#g" | tee results/fixes.txt
