#!/usr/bin/env bash
# What a downstream consumer does with the JSON line that 3.15 writes for an
# ISO-8859-1 byte on stdin. Writes results/consumers.txt. jq and node are
# optional; whichever is installed is tested.
set -euo pipefail
cd "$(dirname "$0")/.."
PY315="${PY315:-$(uv python find "${PY315_VERSION:-3.15.0}")}"
out=results/consumers.txt
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

printf 'caf\351\n' | env -i PATH=/usr/bin:/bin LOCPATH="$PWD/locales" LANG=en_US.UTF-8 \
  "$PY315" -c 'import json, sys; print(json.dumps({"line": sys.stdin.read().strip()}))' \
  > "$work/line.json"

{
  echo "input bytes on stdin:   63 61 66 e9"
  echo "3.15 wrote:             $(cat "$work/line.json")"
  if command -v jq >/dev/null; then
    echo "$(jq --version) -r .line: $(jq -r .line "$work/line.json" | od -An -tx1 | xargs)"
  fi
  if command -v node >/dev/null; then
    echo "node $(node --version) JSON.parse, written as UTF-8: $(node -e '
      const s = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8")).line;
      process.stdout.write(Buffer.from(s + "\n", "utf8"));' "$work/line.json" | od -An -tx1 | xargs)"
  fi
  echo "ef bf bd is U+FFFD, the replacement character: the original byte e9 is gone."
} | tee "$out"
