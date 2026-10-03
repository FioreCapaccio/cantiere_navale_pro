#!/bin/bash
# Build del pacchetto standalone per Windows (64 bit), senza installare nulla:
# Python "embeddable" + pacchetti precompilati per Windows.
# Uso: ./build_windows.sh   (output: build/dist/CantiereNavalePro-Windows)
set -e
cd "$(dirname "$0")"

ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="${BUILD_DIR:-/tmp/cnav_build}"
OUT="$BUILD_DIR/win_dist/CantiereNavalePro-Windows"
PYVER="3.13.15"

echo "==> Scarico Python embeddable $PYVER per Windows"
mkdir -p "$BUILD_DIR/win_dist"
cd "$BUILD_DIR/win_dist"
if [ ! -f "python-embed.zip" ]; then
  curl -sL -o python-embed.zip "https://www.python.org/ftp/python/${PYVER}/python-${PYVER}-embed-amd64.zip"
fi

echo "==> Scarico i pacchetti precompilati per Windows (wheel)"
mkdir -p wheels
python3 -m pip download -q \
  --platform win_amd64 --only-binary=:all: --python-version 3.13 \
  -d wheels \
  fastapi uvicorn sqlalchemy "python-jose" python-multipart python-dotenv

echo "==> Assemblo la cartella portabile"
rm -rf "$OUT"
mkdir -p "$OUT/python/Lib/site-packages"
cd "$OUT"
unzip -q "$BUILD_DIR/win_dist/python-embed.zip" -d python

# attiva Lib/site-packages nel python embeddable
sed -i.bak 's/^#import site/import site/' python/python313._pth
printf '.\nLib/site-packages\nimport site\n' > python/python313._pth
rm -f python/python313._pth.bak

for w in "$BUILD_DIR/win_dist"/wheels/*.whl; do
  python3 -m zipfile -e "$w" python/Lib/site-packages/
done

# sorgenti applicativi
cp "$ROOT/main.py" .
cp -R "$ROOT/static" .

cat > "Avvia Cantiere Navale Pro.bat" <<'EOF'
@echo off
title Cantiere Navale Pro
cd /d "%~dp0"
set OPEN_BROWSER=1
echo.
echo   Cantiere Navale Pro - avvio in corso...
echo   Il browser si apre su http://127.0.0.1:8765
echo   Lascia aperta questa finestra mentre usi l'app.
echo   Per chiudere: chiudi questa finestra o premi Ctrl+C.
echo.
"python\python.exe" main.py
pause
EOF

cat > "LEGGIMI.txt" <<'EOF'
CANTIERE NAVALE PRO - VERSIONE WINDOWS (portabile, nessuna installazione)

AVVIO
  1. Fai doppio clic su "Avvia Cantiene Navale Pro.bat"
     (se Windows mostra un avviso SmartScreen: "Ulteriori informazioni" -> "Esegui comunque")
  2. Il browser si apre da solo su http://127.0.0.1:8765
  3. Accedi con:  utente admin   password admin123
     (cambia la password da Impostazioni dopo il primo accesso)

DOVE SONO I DATI
  Tutti i dati (database, allegati) sono nella cartella "data" accanto a questo
  file: per fare un backup basta copiare quella cartella.

PORTA E RETE
  Di default l'app è raggiungibile solo da questo PC (127.0.0.1).
  Per accedere da altri dispositivi in rete crea un file ".env" accanto a questo
  file con dentro:  HOST=0.0.0.0
  (e apri la porta 8765 nel firewall di Windows)

PROBLEMI
  Se la finestra si chiude all'istante, apri cmd dentro questa cartella e lancia:
    python\python.exe main.py
  Il messaggio di errore ti dirà cosa non va.
EOF

echo "==> Pacchetto pronto: $OUT"
du -sh "$OUT"
