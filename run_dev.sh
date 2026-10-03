#!/bin/bash
# Avvio in sviluppo: crea il venv se manca e lancia il server su http://127.0.0.1:8765
set -e
cd "$(dirname "$0")"
if [ ! -x ".venv/bin/python" ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi
exec .venv/bin/python main.py
