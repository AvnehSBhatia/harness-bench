#!/bin/sh
# Track B: Large fleet jobs, Ambiguous specs and Quick tasks, one section after another; inside a section the two
# harnesses take turns (never at the same time). GPT-6 Luna, at most $1 per harness per section.
#   export OPENROUTER_API_KEY=...; sh run-sections.sh
set -eu
cd "$(dirname "$0")"
[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "export OPENROUTER_API_KEY first" >&2; exit 1; }
echo "== section checks: every reference passes, every starter fails"; python3 sections/validate.py
for s in fleet ambiguous quick; do
	echo "== section: $s"
	node run.mjs --suite "sections/$s" --all --port 8798 --section-budget 1
done
echo "done: results/<time>-<section>/ (REPORT.md, AUDIT.md, SCORECARD.md, calls/ with every request and response)"
