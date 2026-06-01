#!/usr/bin/env bash
cd "$(dirname "$0")"
PORT="${1:-8000}"
URL="http://localhost:${PORT}/rapman.html"
mkdir -p recordings
echo "Serving on ${URL}"
open "${URL}"
exec python3 server.py "${PORT}"
