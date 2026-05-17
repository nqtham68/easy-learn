"""Sync each `output/<project>/vi/` into `docs-site/docs/<project>/`.

Auto-discovers all sibling projects with a `vi/` subfolder. Each project gets
copied as its own top-level tab in the unified docs site.

Usage:
  python scripts/sync_projects.py [--source <path>] [--dest <path>]

Defaults assume this script lives at <repo>/docs-site/scripts/sync_projects.py
and source projects at <repo>/output/*/vi/.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", "raw"}
PROJECT_TITLES = {
    "nats-docs-git": "NATS",
}


def discover_projects(source_root: Path) -> list[Path]:
    found = []
    for p in sorted(source_root.iterdir()):
        if not p.is_dir() or p.name in EXCLUDE_DIRS:
            continue
        vi = p / "vi"
        if vi.is_dir() and any(vi.rglob("*.md")):
            found.append(vi)
    return found


def sync_one(src_vi: Path, dest: Path) -> int:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in src_vi.rglob("*.md"):
        rel = src.relative_to(src_vi)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        count += 1
    return count


def write_landing(dest_root: Path, projects: list[tuple[str, Path]]) -> None:
    lines = [
        "---",
        "title: Trang chủ",
        "---",
        "",
        "# Tài liệu kỹ thuật — Bản dịch tiếng Việt",
        "",
        "Tổng hợp các bản dịch tiếng Việt của tài liệu kỹ thuật mã nguồn mở.",
        "Định dạng song ngữ: mỗi đoạn văn xuôi đi kèm bản gốc tiếng Anh.",
        "",
        "## Các bộ tài liệu",
        "",
    ]
    for slug, _ in projects:
        title = PROJECT_TITLES.get(slug, slug.replace("-", " ").title())
        lines.append(f"- [{title}]({slug}/)")
    (dest_root / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    here = Path(__file__).resolve().parent
    docs_site = here.parent
    repo_root = docs_site.parent

    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=repo_root / "output")
    ap.add_argument("--dest", type=Path, default=docs_site / "docs")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"source not found: {args.source}", file=sys.stderr)
        return 2

    args.dest.mkdir(parents=True, exist_ok=True)

    # Clear old project folders (keep index.md if user customised it manually,
    # but it will be regenerated below).
    for child in args.dest.iterdir():
        if child.is_dir():
            shutil.rmtree(child)

    vi_dirs = discover_projects(args.source)
    if not vi_dirs:
        print(f"no projects with vi/ found under {args.source}", file=sys.stderr)
        return 1

    projects: list[tuple[str, Path]] = []
    for vi in vi_dirs:
        slug = vi.parent.name
        target = args.dest / slug
        n = sync_one(vi, target)
        title = PROJECT_TITLES.get(slug, slug.replace("-", " ").title())
        (target / ".nav.yml").write_text(f"title: {title}\n", encoding="utf-8")
        projects.append((slug, target))
        print(f"synced {slug}: {n} files (title: {title})")

    write_landing(args.dest, projects)
    print(f"\nlanding page written: {args.dest / 'index.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
