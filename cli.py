"""Unified CLI entrypoint for web-easy-learn.

Run any pipeline step through this single command:
  python cli.py crawl          sites/<name>.yaml          # Phase 1A: HTML
  python cli.py fetch          sites/<name>.yaml          # Phase 1B: git
  python cli.py discover       output/<name>/raw          # list pending files
  python cli.py linkify        output/<name>/vi           # wrap bare URLs
  python cli.py rewrite-links  output/<name>/raw output/<name>/vi
  python cli.py sync                                      # vi/ -> docs-site/docs/
  python cli.py serve                                     # mkdocs dev server
  python cli.py build                                     # mkdocs static build

Translation runs inside Claude Code as `/translate-kb` and is not exposed here.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

import typer
from rich.logging import RichHandler

REPO_ROOT = Path(__file__).resolve().parent
HELPERS = REPO_ROOT / ".claude" / "skills" / "translate-kb" / "helpers"
DOCS_SITE = REPO_ROOT / "docs-site"

app = typer.Typer(add_completion=False, no_args_is_help=True, help=__doc__)


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(show_time=False)],
        format="%(message)s",
    )


def _run_helper(script: Path, args: list[str]) -> int:
    return subprocess.call([sys.executable, str(script), *args])


@app.command()
def crawl(
    config_path: Path = typer.Argument(..., help="Path to site YAML config"),
    output: Path = typer.Option(Path("output"), help="Output root directory"),
    ignore_robots: bool = typer.Option(
        False, "--ignore-robots", help="DO NOT use unless target site is yours"
    ),
) -> None:
    """Phase 1A — Crawl HTML pages per YAML config."""
    from crawler import crawl as do_crawl, load_config

    _setup_logging()
    config = load_config(config_path)
    report = do_crawl(config, output_root=output, ignore_robots=ignore_robots)
    typer.echo(
        f"\nDone: {report.written} written, {report.skipped} skipped, "
        f"{report.failed} failed, {report.fetched} fetched"
    )


@app.command()
def fetch(
    config_path: Path = typer.Argument(..., help="Path to site YAML config with source.type=git"),
) -> None:
    """Phase 1B — Fetch markdown from a git repository."""
    from git_fetch import fetch as do_fetch

    if not config_path.exists():
        typer.echo(f"config not found: {config_path}", err=True)
        raise typer.Exit(1)
    raise typer.Exit(do_fetch(config_path))


@app.command()
def discover(
    raw_folder: Path = typer.Argument(..., help="output/<name>/raw"),
    max_files: int = typer.Option(0, "--max-files", help="Cap (0 = unlimited)"),
    no_filter: bool = typer.Option(False, "--no-filter", help="Skip content filter"),
) -> None:
    """List pending raw files (and auto-stub low-content pages)."""
    args = [str(raw_folder)]
    if max_files:
        args += ["--max-files", str(max_files)]
    if no_filter:
        args.append("--no-filter")
    raise typer.Exit(_run_helper(HELPERS / "discover.py", args))


@app.command()
def linkify(
    vi_root: Path = typer.Argument(..., help="output/<name>/vi"),
    files: list[Path] = typer.Argument(None, help="Specific files (default: all *.md)"),
) -> None:
    """Wrap bare URLs in <a href> (auto-skips frontmatter and code blocks)."""
    args = [str(vi_root)] + [str(f) for f in (files or [])]
    raise typer.Exit(_run_helper(HELPERS / "linkify_urls.py", args))


@app.command(name="rewrite-links")
def rewrite_links(
    raw_root: Path = typer.Argument(..., help="output/<name>/raw"),
    vi_root: Path = typer.Argument(..., help="output/<name>/vi"),
    files: list[Path] = typer.Argument(None, help="Specific files (default: all)"),
) -> None:
    """Rewrite upstream doc URLs to local relative paths."""
    args = [str(raw_root), str(vi_root)] + [str(f) for f in (files or [])]
    raise typer.Exit(_run_helper(HELPERS / "rewrite_all_links.py", args))


@app.command()
def sync(
    source: Path = typer.Option(REPO_ROOT / "output", help="Source root with <project>/vi/ folders"),
    dest: Path = typer.Option(DOCS_SITE / "docs", help="docs-site/docs target"),
) -> None:
    """Sync all output/<project>/vi/ into docs-site/docs/<project>/."""
    raise typer.Exit(
        _run_helper(
            DOCS_SITE / "scripts" / "sync_projects.py",
            ["--source", str(source), "--dest", str(dest)],
        )
    )


def _mkdocs(*extra: str) -> int:
    return subprocess.call([sys.executable, "-m", "mkdocs", *extra], cwd=DOCS_SITE)


@app.command()
def serve(
    addr: str = typer.Option("0.0.0.0:8001", "--addr", help="Bind address"),
) -> None:
    """Run mkdocs dev server (auto-reload on docs-site/docs/ changes)."""
    raise typer.Exit(_mkdocs("serve", "--dev-addr", addr))


@app.command()
def build() -> None:
    """Build static MkDocs site to docs-site/site/."""
    raise typer.Exit(_mkdocs("build"))


if __name__ == "__main__":
    app()
