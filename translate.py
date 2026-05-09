"""Translate raw markdown to Vietnamese using Gemini API.

Standalone CLI alternative to the Claude Code skill. Same protect/restore guarantees
(deterministic code-block preservation), same bilingual output format, same resume
semantics (skip files where VN target has translated:true).

Usage:
  python translate.py <raw-folder> [--max-files N] [--concurrency C] [--model M]

Env:
  GEMINI_API_KEY  required
  WEBEZ_GEMINI_MODEL  override default model (gemini-2.5-pro)
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import frontmatter
import typer
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from rich.logging import RichHandler

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 5
BASE_BACKOFF = 4.0  # seconds; doubled each attempt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "translate-kb" / "helpers"))
from protect_code import has_sentinels, protect, restore  # noqa: E402

log = logging.getLogger("translate")

DEFAULT_MODEL = os.getenv("WEBEZ_GEMINI_MODEL", "gemini-2.5-flash")
TRANSLATOR_AGENT_PATH = ROOT / ".claude" / "agents" / "translator.md"


def _load_system_prompt() -> str:
    """Reuse the translator agent's instructions as Gemini system prompt (DRY)."""
    raw = TRANSLATOR_AGENT_PATH.read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    return parts[2].strip() if len(parts) >= 3 else raw


SYSTEM_PROMPT = _load_system_prompt() + (
    "\n\n## Output expectations for direct API call\n\n"
    "Return ONLY the translated markdown file content, starting with the "
    "`---` frontmatter line. No code fences, no preamble, no explanation. "
    "The output will be written to disk as-is."
)

FRONTMATTER_FENCE_RE = re.compile(
    r"^```(?:markdown|md|yaml)?\s*\n(.*)\n```\s*$", re.DOTALL
)


def _strip_outer_fence(text: str) -> str:
    """Some models wrap full output in ```markdown ... ``` — strip if so."""
    m = FRONTMATTER_FENCE_RE.match(text.strip())
    return m.group(1) if m else text


def _vi_target(raw: Path, raw_root: Path, vi_root: Path) -> Path:
    return vi_root / raw.relative_to(raw_root)


def _is_pending(vi_path: Path) -> bool:
    if not vi_path.exists():
        return True
    try:
        post = frontmatter.load(vi_path)
        return not bool(post.metadata.get("translated", False))
    except Exception:
        return True


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)


def _validate(restored: str, original_body_len: int) -> str | None:
    """Return None if ok, else error message."""
    if has_sentinels(restored):
        return "leftover sentinels"
    fences = restored.count("```")
    if fences % 2 != 0:
        return f"unbalanced fences ({fences})"
    try:
        post = frontmatter.loads(restored)
    except Exception as e:
        return f"frontmatter parse: {e}"
    if post.metadata.get("translated") is not True:
        return "frontmatter translated != true"
    if len(post.content) < 0.3 * original_body_len:
        return f"body truncated ({len(post.content)} < 30% of {original_body_len})"
    return None


async def _generate_with_retry(
    client: genai.Client, model: str, user_prompt: str, file_label: str
) -> str:
    """Call Gemini with exponential backoff on transient errors (503/429/500/...)."""
    last_err: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = await client.aio.models.generate_content(
                model=model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                ),
            )
            return resp.text or ""
        except genai_errors.ServerError as e:
            status = getattr(e, "code", None) or getattr(e, "status_code", None)
            if status in RETRYABLE_STATUS and attempt < MAX_ATTEMPTS:
                wait = BASE_BACKOFF * (2 ** (attempt - 1))
                log.info("[%s] %d (attempt %d/%d) — retry in %.0fs", file_label, status, attempt, MAX_ATTEMPTS, wait)
                await asyncio.sleep(wait)
                last_err = e
                continue
            raise
        except genai_errors.ClientError as e:
            status = getattr(e, "code", None) or getattr(e, "status_code", None)
            if status == 429 and attempt < MAX_ATTEMPTS:
                wait = BASE_BACKOFF * (2 ** (attempt - 1))
                log.info("[%s] 429 rate-limited (attempt %d/%d) — wait %.0fs", file_label, attempt, MAX_ATTEMPTS, wait)
                await asyncio.sleep(wait)
                last_err = e
                continue
            raise
    if last_err:
        raise last_err
    return ""


async def _translate_one(
    client: genai.Client,
    model: str,
    raw_path: Path,
    vi_path: Path,
    sem: asyncio.Semaphore,
) -> tuple[Path, str]:
    """Translate one file. Return (path, status) where status ∈ {DONE, FAIL:<reason>}."""
    async with sem:
        try:
            raw_post = frontmatter.load(raw_path)
            original_body = raw_post.content
            protected_body, blocks = protect(original_body)
            input_post = frontmatter.Post(protected_body, **raw_post.metadata)
            input_md = frontmatter.dumps(input_post)

            user_prompt = (
                f"Translate this file to Vietnamese bilingual format.\n\n"
                f"INPUT (do not modify <<<__WEBEZ_*__>>> tokens):\n\n"
                f"```\n{input_md}\n```\n\n"
                f"Set translated_at to: {datetime.now(timezone.utc).isoformat()}"
            )

            resp_text = await _generate_with_retry(client, model, user_prompt, raw_path.name)
            output = _strip_outer_fence(resp_text)

            try:
                restored_body_post = frontmatter.loads(output)
            except Exception as e:
                return raw_path, f"FAIL: response parse: {e}"

            try:
                restored_body = restore(restored_body_post.content, blocks)
            except ValueError as e:
                return raw_path, f"FAIL: {e}"

            final_post = frontmatter.Post(restored_body, **restored_body_post.metadata)
            final_md = frontmatter.dumps(final_post)

            err = _validate(final_md, len(original_body))
            if err:
                return raw_path, f"FAIL: {err}"

            _atomic_write(vi_path, final_md)
            return raw_path, "DONE"
        except Exception as e:
            return raw_path, f"FAIL: {type(e).__name__}: {e}"


async def _run(
    raw_root: Path, max_files: int | None, concurrency: int, model: str
) -> int:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log.error("GEMINI_API_KEY env var not set")
        return 2

    if raw_root.name != "raw":
        log.error("raw folder must end in 'raw': %s", raw_root)
        return 2
    vi_root = raw_root.parent / "vi"

    pending: list[tuple[Path, Path]] = []
    for raw in sorted(raw_root.rglob("*.md")):
        vi = _vi_target(raw, raw_root, vi_root)
        if _is_pending(vi):
            pending.append((raw, vi))
            if max_files and len(pending) >= max_files:
                break

    if not pending:
        log.info("Nothing to translate")
        return 0

    log.info(
        "translating %d files (model=%s, concurrency=%d)",
        len(pending),
        model,
        concurrency,
    )

    client = genai.Client(api_key=api_key)
    sem = asyncio.Semaphore(concurrency)

    tasks = [_translate_one(client, model, raw, vi, sem) for raw, vi in pending]
    done = 0
    failed = 0
    for coro in asyncio.as_completed(tasks):
        path, status = await coro
        if status == "DONE":
            done += 1
            log.info("[%d/%d] DONE %s", done + failed, len(pending), path.name)
        else:
            failed += 1
            log.warning(
                "[%d/%d] %s — %s", done + failed, len(pending), path.name, status
            )

    print(f"\ntranslate done: {done} done, {failed} failed, {len(pending)} total")
    return 0 if failed == 0 else 1


app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def main(
    raw_folder: Path = typer.Argument(
        ..., help="Raw folder, e.g. output/nats-docs/raw"
    ),
    max_files: int = typer.Option(None, "--max-files", help="Cap files per run"),
    concurrency: int = typer.Option(2, "--concurrency", help="Parallel API calls"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", help="Gemini model id"),
) -> None:
    """Translate raw markdown folder to Vietnamese bilingual via Gemini API."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(show_time=False)],
        format="%(message)s",
    )
    rc = asyncio.run(_run(raw_folder, max_files, concurrency, model))
    raise typer.Exit(rc)


if __name__ == "__main__":
    app()
