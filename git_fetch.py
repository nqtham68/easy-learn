"""Phase 1 alternative: fetch markdown from a git repo (e.g. GitBook source).

Usage:
  python git_fetch.py <config.yaml>

Config (add `source:` block to site YAML):
  source:
    type: git
    repo: https://github.com/nats-io/nats.docs
    branch: main                # default: main
    docs_path: .                # subfolder containing .md files (default: .)
    url_base: https://docs.nats.io  # used to generate source_url in frontmatter
    exclude:                    # optional glob patterns to skip (default: [])
      - "node_modules/**"
      - ".github/**"
      - "**/SUMMARY.md"
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from posixpath import normpath
from urllib.parse import urlparse

import frontmatter
import yaml


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*```")


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "mailto:", "#", "/"))


def resolve_relative(url: str, file_dir: str) -> tuple[str, str]:
    """Return (resolved_path_no_anchor, anchor_with_hash_or_empty)."""
    anchor = ""
    if "#" in url:
        url, anchor = url.split("#", 1)
        anchor = "#" + anchor
    if not url:
        return "", anchor
    base = file_dir.rstrip("/")
    joined = f"{base}/{url}" if base else url
    return normpath(joined), anchor


def derive_raw_base(repo_url: str, branch: str) -> str:
    p = urlparse(repo_url)
    path = p.path.rstrip("/")
    if path.endswith(".git"):
        path = path[: -len(".git")]
    return f"https://raw.githubusercontent.com{path}/{branch}"


def rewrite_md_links(content: str, file_rel: Path, raw_base: str, url_base: str) -> str:
    """Rewrite relative image and link URLs to absolute. Skip fenced code blocks."""
    file_dir = file_rel.parent.as_posix()
    if file_dir == ".":
        file_dir = ""
    url_base_clean = url_base.rstrip("/")

    def repl_image(m: re.Match[str]) -> str:
        alt, url, title = m.group(1), m.group(2), m.group(3) or ""
        if is_external(url):
            return m.group(0)
        resolved, anchor = resolve_relative(url, file_dir)
        return f"![{alt}]({raw_base}/{resolved}{anchor}{title})"

    def repl_link(m: re.Match[str]) -> str:
        text, url, title = m.group(1), m.group(2), m.group(3) or ""
        if is_external(url):
            return m.group(0)
        resolved, anchor = resolve_relative(url, file_dir)
        if resolved.endswith(".md"):
            resolved = resolved[:-3]
        if resolved.endswith("/README"):
            resolved = resolved[: -len("/README")]
        elif resolved == "README":
            resolved = ""
        target = f"{url_base_clean}/{resolved}".rstrip("/") if resolved else url_base_clean
        return f"[{text}]({target}{anchor}{title})"

    out_lines: list[str] = []
    in_fence = False
    for line in content.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        line = IMAGE_RE.sub(repl_image, line)
        line = LINK_RE.sub(repl_link, line)
        out_lines.append(line)
    return "".join(out_lines)


def is_excluded(rel: Path, patterns: list[str]) -> bool:
    rel_str = rel.as_posix()
    return any(fnmatch.fnmatch(rel_str, p) for p in patterns)


def derive_source_url(url_base: str, rel: Path) -> str:
    base = url_base.rstrip("/")
    path = rel.as_posix()
    if path.endswith("/README.md"):
        path = path[: -len("/README.md")]
    elif path == "README.md":
        path = ""
    elif path.endswith(".md"):
        path = path[: -len(".md")]
    return f"{base}/{path}".rstrip("/")


def derive_title(post: frontmatter.Post, md_path: Path) -> str:
    if "title" in post.metadata:
        return str(post.metadata["title"])
    for line in post.content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return md_path.stem.replace("-", " ").replace("_", " ").title()


def fetch(config_path: Path) -> int:
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    src = cfg.get("source")
    if not src or src.get("type") != "git":
        print(f"config {config_path} has no `source.type: git` block", file=sys.stderr)
        return 2

    name = cfg["name"]
    repo = src["repo"]
    branch = src.get("branch", "main")
    docs_path = src.get("docs_path", ".")
    url_base = src.get("url_base", "")
    exclude = src.get("exclude", [])

    out_root = Path("output") / name / "raw"
    out_root.mkdir(parents=True, exist_ok=True)
    raw_base = derive_raw_base(repo, branch)

    with tempfile.TemporaryDirectory() as tmp:
        clone_dir = Path(tmp) / "repo"
        print(f"cloning {repo} ({branch}) ...")
        subprocess.run(
            ["git", "clone", "--depth=1", "--branch", branch, repo, str(clone_dir)],
            check=True,
        )
        docs_root = clone_dir / docs_path
        if not docs_root.exists():
            print(f"docs_path not found in repo: {docs_path}", file=sys.stderr)
            return 1

        now = datetime.now(timezone.utc).isoformat()
        written = 0
        skipped = 0

        for md in docs_root.rglob("*.md"):
            rel = md.relative_to(docs_root)
            if is_excluded(rel, exclude):
                skipped += 1
                continue

            try:
                post = frontmatter.loads(md.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  skip (parse error) {rel}: {e}", file=sys.stderr)
                skipped += 1
                continue

            if url_base:
                post.content = rewrite_md_links(post.content, rel, raw_base, url_base)

            post.metadata["title"] = derive_title(post, md)
            post.metadata["source_url"] = derive_source_url(url_base, rel) if url_base else ""
            post.metadata["crawled_at"] = now
            post.metadata["translated"] = False

            dest = out_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(frontmatter.dumps(post), encoding="utf-8", newline="\n")
            written += 1

    print(f"fetched: {written} written, {skipped} skipped → {out_root}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"config not found: {config_path}", file=sys.stderr)
        return 1
    return fetch(config_path)


if __name__ == "__main__":
    sys.exit(main())
