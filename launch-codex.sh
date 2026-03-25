#!/bin/bash
# Agent Factory — Launch with Codex (Linux)
# Run: chmod +x launch-codex.sh && ./launch-codex.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  Agent Factory — Starting Codex"
echo "========================================="
echo ""
echo "  Project: $SCRIPT_DIR"
echo "  Codex will read CODEX.md automatically."
echo ""

if ! command -v codex &>/dev/null; then
    echo "[ERROR] 'codex' command not found."
    echo "  Install Codex: https://github.com/openai/codex"
    exit 1
fi

codex
