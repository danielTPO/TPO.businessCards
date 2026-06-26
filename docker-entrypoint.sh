#!/bin/sh
set -e

if [ "$#" -eq 0 ] || [ "$1" = "serve" ] || [ "$1" = "web" ]; then
  exec uvicorn api.orders:app --host 0.0.0.0 --port 8000
fi

exec python -m bizcard "$@"
