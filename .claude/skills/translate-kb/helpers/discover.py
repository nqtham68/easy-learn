"""Discover pending files for translate-kb skill.

Usage:
  python discover.py <raw-folder> [--max-files N] [--no-filter]

Prints one pending raw-file path per line on stdout. By default, runs the
content filter and writes a `translated: skipped` stub for low-content files
so they are excluded from the pending list (and never re-attempted).
"""

from __future__ import annotations

import sys
from pathlib import Path

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_filter import classify, write_stub


def vi_target(raw_path: Path, raw_root: Path, vi_root: Path) -> Path:
    rel = raw_path.relative_to(raw_root)
    return vi_root / rel


def is_pending(vi_path: Path) -> bool:
    if not vi_path.exists():
        return True
    try:
        post = frontmatter.load(vi_path)
        return not bool(post.metadata.get("translated", False))
    except Exception:
        return True


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    raw_root = Path(sys.argv[1]).resolve()
    if not raw_root.exists():
        print(f"raw folder not found: {raw_root}", file=sys.stderr)
        return 2

    max_files = None
    if "--max-files" in sys.argv:
        i = sys.argv.index("--max-files")
        max_files = int(sys.argv[i + 1])
    apply_filter = "--no-filter" not in sys.argv

    # raw_root must end in /raw — derive vi_root
    if raw_root.name != "raw":
        print(f"expected raw folder ending in 'raw', got: {raw_root}", file=sys.stderr)
        return 2
    vi_root = raw_root.parent / "vi"

    pending = []
    skipped = 0
    for raw in sorted(raw_root.rglob("*.md")):
        vi = vi_target(raw, raw_root, vi_root)
        if not is_pending(vi):
            continue
        if apply_filter:
            low, reason = classify(raw)
            if low:
                write_stub(raw, vi, reason)
                skipped += 1
                print(f"# skip {raw.relative_to(raw_root)}: {reason}", file=sys.stderr)
                continue
        pending.append(raw)
        if max_files and len(pending) >= max_files:
            break

    for p in pending:
        print(p)
    print(f"# pending: {len(pending)}  skipped: {skipped}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
