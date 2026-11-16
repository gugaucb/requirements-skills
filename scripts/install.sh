#!/usr/bin/env bash
# Install every skill into a harness skills directory, flattened to <dest>/<skill>/SKILL.md.
# Usage: scripts/install.sh <dest> [--copy]
# Examples:
#   scripts/install.sh .agents/skills          # open Agent Skills location (Codex, Gemini CLI, others)
#   scripts/install.sh .claude/skills          # Claude Code
#   scripts/install.sh ~/.agents/skills --copy # user-wide, copies instead of symlinking
set -euo pipefail
dest="${1:?usage: install.sh <dest> [--copy]}"
mode="${2:-}"
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$dest"
count=0
for skill in "$root"/skills/*/*/SKILL.md; do
  dir="$(dirname "$skill")"
  bucket="$(basename "$(dirname "$dir")")"
  [ "$bucket" = "deprecated" ] && continue
  name="$(basename "$dir")"
  rm -rf "${dest:?}/$name"
  if [ "$mode" = "--copy" ]; then cp -R "$dir" "$dest/$name"; else ln -s "$dir" "$dest/$name"; fi
  count=$((count + 1))
done
echo "Installed $count skills into $dest"
echo "Next: start your agent in the target repo and ask for /setup-requirements-repo (or: use the setup-requirements-repo skill)."
