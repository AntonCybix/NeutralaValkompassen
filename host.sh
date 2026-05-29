#!/usr/bin/env bash
# Hostar valkompassen lokalt. Användning: ./host.sh [port]
set -euo pipefail

PORT="${1:-8000}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
URL="http://localhost:${PORT}/index.html"

cd "$DIR"

if [ ! -f index.html ]; then
  echo "✗ index.html saknas i $DIR" >&2
  exit 1
fi

# Hitta en python
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python  >/dev/null 2>&1; then PY=python
else
  echo "✗ python3 hittades inte – kan inte starta servern." >&2
  exit 1
fi

echo "▸ Valkompass 2026"
echo "  Serverar $DIR"
echo "  Öppna:  $URL"
echo "  Stoppa: Ctrl+C"
echo

# Försök öppna webbläsaren (tyst, valfritt) en kort stund efter start
( sleep 1
  if   command -v xdg-open >/dev/null 2>&1; then xdg-open  "$URL"
  elif command -v open     >/dev/null 2>&1; then open      "$URL"
  fi ) >/dev/null 2>&1 &

exec "$PY" -m http.server "$PORT" --bind 127.0.0.1
