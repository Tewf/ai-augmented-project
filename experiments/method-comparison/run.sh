#!/bin/bash
# Usage: run.sh SCRATCH [--harness] [--limit N]
# The key is taken from the maintainer's shell file into this process's environment only, as ANTHROPIC_API_KEY.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
eval "$(grep '^export ANTHROPIC_API_KEY_ODOPHONE=' "$HOME/.bashrc")"
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY_ODOPHONE"
unset ANTHROPIC_API_KEY_ODOPHONE
cd "$HERE"
exec python3 run.py "$@"
