#!/bin/bash
# fixture-single-agent — Launch with Codex (macOS)
# Double-click this file to start your agent.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  fixture-single-agent — Starting Codex"
echo "========================================="
echo ""
echo "  Project: $SCRIPT_DIR"
echo "  Codex will read CODEX.md automatically."
echo ""

if ! command -v codex &>/dev/null; then
    echo "[ERROR] 'codex' command not found."
    echo "  Install Codex: https://github.com/openai/codex"
    echo ""
    echo "Press any key to close..."
    read -n 1
    exit 1
fi

codex

echo ""
echo "Session ended. Press any key to close..."
read -n 1
