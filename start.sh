#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
 umask 077
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  python - <<'PY'
from pathlib import Path
import secrets
p=Path('.env');p.write_text(p.read_text().replace('replace-with-random-token-at-least-24-characters',secrets.token_urlsafe(32)))
PY
fi
printf 'Open http://127.0.0.1:8765 in your browser. Private token (do not share):\n'
grep '^JARVIS_TOKEN=' .env | cut -d= -f2-
exec python -m uvicorn app:app --host 127.0.0.1 --port 8765
