#!/bin/bash
# Build dell'app standalone macOS (Apple Silicon) con PyInstaller.
# Uso: ./build_mac.sh   (l'output finisce in build/dist/CantiereNavalePro.app)
set -e
cd "$(dirname "$0")"

BUILD_DIR="${BUILD_DIR:-/tmp/cnav_build}"
APP_NAME="CantiereNavalePro"
SRC="$BUILD_DIR/src"
PY="$BUILD_DIR/venv/bin/python"

echo "==> Preparo ambiente di build in $BUILD_DIR"
mkdir -p "$SRC"
if [ ! -x "$PY" ]; then
  uv venv "$BUILD_DIR/venv" --python 3.13
fi
uv pip install --python "$PY" -q fastapi uvicorn sqlalchemy python-jose python-multipart python-dotenv pyinstaller pillow

echo "==> Copio i sorgenti"
cp main.py "$SRC/"
cp make_icon.py "$SRC/" 2>/dev/null || true
rm -rf "$SRC/static" && cp -R static "$SRC/"

echo "==> Genero icona"
(cd "$SRC" && "$PY" make_icon.py)

echo "==> PyInstaller"
cd "$SRC"
rm -rf build dist "$APP_NAME.app"

"$PY" -m PyInstaller \
  --name "$APP_NAME" \
  --windowed \
  --clean \
  --noconfirm \
  --icon icon.icns \
  --osx-bundle-identifier "it.cantierenavale.pro" \
  --add-data "static:static" \
  --hidden-import "uvicorn.logging" \
  --hidden-import "uvicorn.loops" \
  --hidden-import "uvicorn.loops.auto" \
  --hidden-import "uvicorn.protocols" \
  --hidden-import "uvicorn.protocols.http" \
  --hidden-import "uvicorn.protocols.http.auto" \
  --hidden-import "uvicorn.protocols.http.h11_impl" \
  --hidden-import "uvicorn.protocols.websockets" \
  --hidden-import "uvicorn.protocols.websockets.auto" \
  --hidden-import "uvicorn.lifespan" \
  --hidden-import "uvicorn.lifespan.on" \
  --hidden-import "jose.jwt" \
  --hidden-import "jose.jws" \
  --hidden-import "jose.backends" \
  main.py

echo "==> Build completata: $SRC/dist/$APP_NAME.app"
