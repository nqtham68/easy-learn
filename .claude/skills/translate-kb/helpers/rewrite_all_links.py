"""Rewrite upstream doc URLs to local relative paths across a vi/ tree.

Usage:
  python rewrite_all_links.py <raw-root> <vi-root> [<file>...]

If no files specified, processes all *.md under <vi-root>.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rewrite_links import rewrite_file


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    raw_root = Path(argv[0]).resolve()
    vi_root = Path(argv[1]).resolve()
    if argv[2:]:
        files = [Path(p).resolve() for p in argv[2:]]
    else:
        files = sorted(vi_root.rglob("*.md"))
    total_rewritten = 0
    total_links = 0
    changed_files = 0
    for f in files:
        rewritten, links = rewrite_file(f, raw_root, vi_root)
        total_rewritten += rewritten
        total_links += links
        if rewritten:
            changed_files += 1
            print(f"{f.relative_to(vi_root)}: {rewritten}/{links} links rewritten")
    print(
        f"\ntotal: {total_rewritten}/{total_links} links rewritten across "
        f"{changed_files}/{len(files)} files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
