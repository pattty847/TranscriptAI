#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Subtext"
echo ""

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed."
  echo "Install it from: https://docs.astral.sh/uv/getting-started/installation/"
  read -r -n 1 -p "Press any key to close..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Setting up environment with uv sync..."
  if ! uv sync; then
    echo "Setup failed."
    read -r -n 1 -p "Press any key to close..."
    exit 1
  fi
fi

echo "  [1] Desktop   - full app on this computer"
echo "  [2] Web       - browser UI (this PC + same Wi-Fi devices)"
echo ""
read -r -p "Choose 1 or 2: " pick
echo ""

case "${pick:-1}" in
  2)
    echo "Starting Web UI... Open http://127.0.0.1:8765 in your browser."
    echo "From phone/tablet on same Wi-Fi: http://YOUR_PC_IP:8765"
    echo ""
    uv run python run_web.py
    ;;
  *)
    echo "Launching Subtext (Desktop)..."
    uv run python run.py
    ;;
esac

if [ $? -ne 0 ]; then
  echo ""
  echo "Application exited with an error."
  read -r -n 1 -p "Press any key to close..."
  exit 1
fi
