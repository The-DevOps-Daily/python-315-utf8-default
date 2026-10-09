#!/usr/bin/env bash
# Compare the static checker with what -X warn_default_encoding reports when
# examples/release_notes.py actually runs on 3.15. Writes results/checker-example.txt.
set -euo pipefail
cd "$(dirname "$0")/.."
PY315="${PY315:-$(uv python find "${PY315_VERSION:-3.15.0}")}"
repo=$PWD
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cd "$work"
git init -q . && git config user.email demo@example.com && git config user.name demo
printf '[service]\nname = billing\n' > service.ini
mkdir templates && printf '# {service}\n\n{changes}\n' > templates/notes.md.tmpl
git add . && git commit -qm "initial" && git tag v0
git commit -q --allow-empty -m "Fix the café menu price in €"

{
  echo "## static: check_default_encoding.py examples/"
  (cd "$repo" && python3 check_default_encoding.py examples/ 2>&1) || true
  echo
  echo "## runtime: python3.15 -X warn_default_encoding examples/release_notes.py v0"
  env -i PATH=/usr/bin:/bin HOME="$work" LANG=C.UTF-8 "$PY315" -X warn_default_encoding \
    -W always::EncodingWarning "$repo/examples/release_notes.py" v0 2>&1 \
    | grep EncodingWarning | sed "s#$repo/##" | sort -t: -k2 -n
  echo
  echo "## RELEASE_NOTES.md"
  cat RELEASE_NOTES.md
} | tee "$repo/results/checker-example.txt"
