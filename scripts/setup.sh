#!/usr/bin/env bash
# Install the two interpreters and build the test locales into ./locales.
# Needs Linux with glibc (localedef) and uv.
set -euo pipefail
cd "$(dirname "$0")/.."

PY314="${PY314:-3.14.8}"
PY315="${PY315:-3.15.0}"
uv python install "$PY314" "$PY315"

mkdir -p locales
# name in LANG          source   charmap
while read -r name src charmap; do
  [ -d "locales/$name" ] || localedef -i "$src" -f "$charmap" "locales/$name"
done <<'LIST'
C.UTF-8 C UTF-8
en_US.UTF-8 en_US UTF-8
en_US en_US ISO-8859-1
ja_JP.eucJP ja_JP EUC-JP
LIST

echo "locales: $(ls locales | tr '\n' ' ')"
