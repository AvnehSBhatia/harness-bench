#!/bin/sh
# After run-sections.sh: Large fleet jobs again, Heliod only, with --private-checks, so the checks Heliod normally
# sends to its free hosted checker run on the task's own model and are metered and billed like everything else.
#   export OPENROUTER_API_KEY=...; sh run-private-checks.sh
set -eu
cd "$(dirname "$0")"
[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "export OPENROUTER_API_KEY first" >&2; exit 1; }
node run.mjs --suite sections/fleet --all --arms heliod-private --port 8799 --section-budget 1
