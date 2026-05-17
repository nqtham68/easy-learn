---
name: translate-kb
description: Translate a folder of crawled markdown files (EN) to Vietnamese bilingual format. Spawns parallel translator subagents per batch, preserves code blocks deterministically, file-based resume.
---

# translate-kb

Translate raw markdown crawled by `crawler.py` (Phase 1) to Vietnamese bilingual `vi/` output.

## Usage

```
/translate-kb <raw-folder> [--batch-size N] [--max-files M] [--auto] [--review-first N]
```

- `raw-folder`: e.g. `output/nats-docs/raw`
- `--batch-size`: parallel subagents per batch (default 3, validated by Spike A)
- `--max-files`: cap files per run (default unlimited)
- `--auto`: run end-to-end without pausing between batches; only print final summary
- `--review-first N`: after translating, spawn `translation-reviewer` agent to refine the first N files (default 0). Useful for QA passes on early files before a long run.

Output written to sibling folder `vi/` (e.g. `output/nats-docs/vi`).

## Workflow

### Step 1 — Discover pending files

1. Glob `<raw-folder>/**/*.md`.
2. For each raw file, compute target path: replace `/raw/` with `/vi/` in the path.
3. **Filter pending:** include the file if EITHER:
   - target VN file does not exist, OR
   - target VN file exists but its frontmatter `translated` is not `true` (note:
     `translated: skipped` counts as not-pending — see content filter below).
4. **Content filter (auto):** before adding a pending file to the batch, run
   `content_filter.classify()`. If it returns low-content (under 20 prose words
   OR >80% link-only lines), write a stub VN file with `translated: skipped`
   and `skip_reason: <why>`, then exclude it from the pending list. Pass
   `--no-filter` to bypass.
5. Apply `--max-files` cap.
6. If pending list empty: report "Nothing to translate" and stop.

### Step 2 — Per-file preparation (deterministic, no LLM)

For each pending file (sequential, fast):

1. Read raw file content.
2. Split frontmatter (YAML between leading `---`) from body.
3. Run `protect_code.protect(body)` → `(protected_body, blocks_dict)`.
4. Save the `blocks_dict` to a temp file `<vi-target>.blocks.json` next to where the VN file will land. (Skill needs to restore after subagent returns.)
5. Write a temp input file `<vi-target>.tmp-input.md` containing:
   - Original frontmatter (unchanged at this stage)
   - Plus `protected_body`

This temp file is what the subagent will read.

### Step 3 — Spawn translator subagents in parallel batches

Loop over pending files in chunks of `batch_size`:

For the chunk, spawn N `translator` subagents IN ONE MESSAGE (multiple Task tool calls in a single response). Each subagent prompt includes:

```
Translate the markdown file at:
  INPUT: <absolute path to .tmp-input.md>

Write the Vietnamese bilingual translation to:
  OUTPUT: <absolute path to .tmp-output.md>

FEEDBACK: <absolute path to <vi-root>/_review-feedback.md>

Preserve all <<<__WEBEZ_*__>>> tokens exactly. Translate prose only. Update
frontmatter: title → Vietnamese, translated: true, translated_at: <ISO now>.

Return DONE on success.
```

The FEEDBACK path points at `<vi-root>/_review-feedback.md`. The translator
reads it (if it exists) and applies glossary overrides + style rules from
prior review passes. The file is created lazily by reviewers — pass the path
unconditionally, even if the file does not yet exist.

Wait for all subagents in the batch to return. Per Spike A, expect ~1.86× speedup vs sequential.

**Stall handling:** Occasionally a translator subagent stalls and is killed by
the harness watchdog (typically after ~600s of no output). The notification
arrives with `status: failed` and a summary like "Agent stalled: no progress
for 600s". When this happens:

1. Do NOT re-run protect — the `.tmp-input.md` and `.blocks.json` are still
   valid on disk.
2. Re-spawn a fresh `translator` subagent with the same INPUT/OUTPUT/FEEDBACK
   paths. The next attempt usually succeeds (the stall is usually a network
   blip, not a bad input).
3. Continue restore + validation as normal once the retry returns DONE.

A single retry counts as "completed", not "failed", in the Step 5 summary.

### Step 3.5 — Review pass (optional, --review-first N)

If `--review-first N > 0`, after a translator subagent's tmp-output is produced (and before code restore), for the first N files of the run:

1. Spawn `translation-reviewer` subagent with prompt:
   ```
   Review and refine the Vietnamese bilingual translation at:
     INPUT/OUTPUT: <absolute path to .tmp-output.md>

   FEEDBACK: <absolute path to <vi-root>/_review-feedback.md>

   Read the file, apply refinements per your spec (naturalness, glossary
   consistency, inline gloss selection), and overwrite the same path.

   After refining, append generalizable findings (glossary overrides, style
   rules, common pitfalls) to the FEEDBACK file per the criteria in your
   agent spec. Create the file with the documented section structure if it
   does not exist.

   Preserve all <<<__WEBEZ_*__>>> tokens, `> 🇬🇧 *...*` blockquote lines,
   and frontmatter fields exactly. Return DONE on success.
   ```
2. Wait for reviewer to return.
3. Reviewers can be batched in parallel up to `batch_size`, same as translators.
4. After review, proceed to Step 4 (restore + validate + atomic write).

### Step 4 — Restore code blocks + validate + atomic write

For each completed subagent:

1. Read the subagent's `.tmp-output.md`.
2. Run `protect_code.restore(content, blocks_dict)`.
3. Validate the restored content:
   - `not protect_code.has_sentinels(restored)` (no leftover tokens)
   - Triple-backtick fence count is even
   - Frontmatter parses (use `python-frontmatter`)
   - Frontmatter has `translated: true`
   - Body length > 30% of original input length (reject obvious truncation)
4. If all checks pass: atomic write to final `<vi-target>.md` (write `.tmp` then `os.replace`).
5. Delete `.tmp-input.md`, `.tmp-output.md`, `.blocks.json` **only on success**.
6. If checks fail: log `FAIL <file>: <reason>` and leave VN target absent. **Keep tmp files for debugging.** The next skill run will see the missing target and re-attempt.

**CRITICAL — cleanup ordering in shell loops:**

When restoring multiple files in a bash loop, cleanup must be conditional on restore success. WRONG pattern (deletes tmp even on FAIL, losing debug evidence):

```bash
for f in ...; do
  cli_protect.py restore ... || echo FAIL
  rm -f tmp-input tmp-output blocks  # ❌ runs unconditionally
done
```

CORRECT pattern (cleanup only when restore succeeds):

```bash
for f in ...; do
  if cli_protect.py restore "$f.tmp-output.md" "$f.blocks.json" "$f.md"; then
    rm -f "$f.tmp-input.md" "$f.tmp-output.md" "$f.blocks.json"
  else
    echo "FAIL: $f (tmp files kept for debug)"
  fi
done
```

### Step 4.4 — Linkify bare URLs

Some raw pages embed bare URLs inside literal HTML blocks (e.g., `<p>https://...</p>`),
where markdown auto-link syntax doesn't work. Run the linkifier to wrap them
in `<a href>`:

```bash
.venv/Scripts/python.exe .claude/skills/translate-kb/helpers/linkify_urls.py <vi-root> [<vi-file>...]
```

Already-formatted markdown links and code blocks are preserved.

### Step 4.5 — Rewrite upstream links to local relative paths

After all files in the run are restored and atomically written, run the link
rewriter once across all newly-written VN files:

```bash
.venv/Scripts/python.exe .claude/skills/translate-kb/helpers/rewrite_all_links.py <raw-root> <vi-root> [<vi-file>...]
```

This converts links like `https://docs.nats.io/<path>` and site-root-relative
`/<path>` to relative paths pointing at the corresponding `vi/<path>.md`,
preserving anchors and query strings. Links to external sites (github.com,
wikipedia, etc.) are left untouched.

To re-run across an existing tree (e.g., after fixing the rewriter), invoke
with no file args to process all `*.md` under `<vi-root>`.

### Step 5 — Report

Print final summary:

```
translate-kb done:
  done    : N files
  skipped : K files (already translated)
  failed  : F files (see logs above)
```

## Requirements / Setup

- Python 3.11+ with `python-frontmatter` and the helper module:
  - `python -c "import sys; sys.path.insert(0, '.claude/skills/translate-kb/helpers'); from protect_code import protect, restore"` should succeed.
- Virtual env activated (typically `.venv/Scripts/python.exe` on Windows).
- Phase 1 raw folder exists with at least one `.md` file having `translated: false`.

## Helper invocation pattern

The skill should NOT inline the regex logic — call `protect_code.py` via subprocess or import it. Recommended: call a small Python wrapper script the skill runs via Bash:

```bash
.venv/Scripts/python.exe .claude/skills/translate-kb/helpers/cli_protect.py protect <raw-md-path> <output-tmp-input> <blocks-json>
.venv/Scripts/python.exe .claude/skills/translate-kb/helpers/cli_protect.py restore <subagent-output> <blocks-json> <final-vn-path>
```

(See `helpers/cli_protect.py` for the wrapper.)

## Auto mode

When `--auto` is passed:
- Skip per-batch progress narration in user-visible text (still log internally).
- Do not pause to ask the user for confirmation between batches.
- Print only the final Step 5 summary.

When NOT in auto mode (default):
- Print 1 short line per batch like `batch 3/53: 3/3 done`.
- Still do not pause for confirmation — the skill always runs end-to-end. Auto mode purely controls verbosity.

## Important Constraints

- **Do NOT translate inside this skill's main agent context.** Always delegate to `translator` subagent. Main agent context must stay clean across batches.
- **Resume-safe:** if interrupted mid-batch, re-running the skill picks up where left off (filter step skips completed files automatically).
- **Code blocks are sacred:** byte-equal preservation is non-negotiable. The protect/restore round-trip is tested in `tests/test_protect_code.py`.
- **One subagent = one file.** Do not batch multiple files into a single subagent prompt.

## Bilingual Format Reference

See `examples/bilingual-format.md`.

## Fallback: VN-only mode (if Spike B fails)

If the user's NotebookLM pilot (Spike B) shows bilingual format pollutes retrieval, the translator agent prompt at `.claude/agents/translator.md` can be edited to skip the `> 🇬🇧 *...*` blockquote wrapping and emit only Vietnamese paragraphs. No skill-level changes needed.
