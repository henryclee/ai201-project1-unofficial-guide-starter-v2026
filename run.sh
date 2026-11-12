#!/usr/bin/env bash
# The one documented start command for The Unofficial Guide (unit 9, Path B).
#
#   ./run.sh            index (first run only), then serve on http://localhost:5001
#
# Does exactly what RUNNING.md says: activate .venv, check the API key, pin the
# corpus to city_guides, build the index if there isn't one, start serve.py.
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "No .venv found. Create it first (see RUNNING.md → Environment)." >&2
  exit 1
fi

# serve.py loads .env itself, but fail early with a readable message if the key is missing.
if [ -z "${GEMINI_API_KEY:-}" ] && ! grep -qE '^GEMINI_API_KEY=.+' .env 2>/dev/null; then
  echo "GEMINI_API_KEY is not set. Copy .env.example to .env and paste your key in." >&2
  exit 1
fi

# config.CORPUS defaults to campus_life; the service is tuned and tested on city_guides.
export AI201_CORPUS="${AI201_CORPUS:-city_guides}"
export PORT="${PORT:-5001}"

if ! python -c "import store, sys; sys.exit(0 if store.index_exists('$AI201_CORPUS') else 1)"; then
  echo "no index for $AI201_CORPUS — building it now (first run only: downloads the ~80 MB embedder, then takes a few seconds to a minute)"
  python app.py --corpus "$AI201_CORPUS" index
  echo "index built."
fi

exec python serve.py
