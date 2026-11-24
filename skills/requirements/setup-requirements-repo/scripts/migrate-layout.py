#!/usr/bin/env python3
"""Move a flat v2 artifact root into the numbered phase layout (stdlib only).

Usage: migrate-layout.py <artifact-root> [--apply]
Dry run by default: prints the moves and changes nothing. Never overwrites, never runs git.
Relative Markdown links between moved files are not rewritten; the report lists files that contain links.
"""
import re
import shutil
import sys
from pathlib import Path

MOVES = [
    ("PRODUCT-VISION.md", "01-vision/PRODUCT-VISION.md"),
    ("BACKLOG.md", "02-backlog/BACKLOG.md"),
    ("specs", "03-specs"),
    ("stories", "04-stories"),
    ("changes", "05-changes"),
    ("requests", "inputs/requests"),
    ("research", "inputs/research"),
    ("GLOSSARY.md", "shared/GLOSSARY.md"),
    ("GLOSSARY-MAP.md", "shared/GLOSSARY-MAP.md"),
    ("DECISIONS.md", "shared/DECISIONS.md"),
    ("OUT-OF-SCOPE.md", "shared/OUT-OF-SCOPE.md"),
]


def plan(root):
    out, skipped = [], []
    for src, dst in MOVES:
        s, d = root / src, root / dst
        if not s.exists():
            continue
        if d.exists():
            skipped.append(f"{src}: destination {dst} already exists")
        else:
            out.append((s, d))
    return out, skipped


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 64
    root = Path(args[0])
    moves, skipped = plan(root)
    for s, d in moves:
        print(f"{'move' if '--apply' in argv else 'would move'}: {s.relative_to(root)} -> {d.relative_to(root)}")
        if "--apply" in argv:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(s), str(d))
    for x in skipped:
        print("skip:", x)
    if "--apply" in argv:
        linked = [f for f in root.rglob("*.md") if re.search(r"\]\((?!https?:)[^)]*\.md", f.read_text(encoding="utf-8", errors="replace"))]
        for f in linked:
            print("check relative links in:", f.relative_to(root))
    elif moves:
        print("dry run: re-run with --apply to move")
    if not moves and not skipped:
        print("nothing to migrate")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
