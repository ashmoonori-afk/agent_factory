#!/bin/bash
# uiux-design-helper — Launch with Claude Code (Linux)
# Run: chmod +x launch-claude.sh && ./launch-claude.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  uiux-design-helper — Starting Claude Code"
echo "========================================="
echo ""
echo "  Project: $SCRIPT_DIR"
echo "  Claude Code will read CLAUDE.md automatically."
echo ""

if ! command -v claude &>/dev/null; then
    echo "[ERROR] 'claude' command not found."
    echo "  Install Claude Code: https://docs.anthropic.com/en/docs/claude-code"
    exit 1
fi

claude
