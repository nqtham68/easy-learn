"""CLI wrapper around protect_code for the translate-kb skill.

Usage:
  python cli_protect.py protect <raw_md_path> <output_tmp_input> <blocks_json>
  python cli_protect.py restore <subagent_output> <blocks_json> <final_vn_path>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize_gitbook import normalize
from protect_code import has_sentinels, protect, restore


def cmd_protect(raw_path: Path, tmp_input: Path, blocks_json: Path) -> int:
    raw = raw_path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    body = normalize(post.content)
    protected_body, blocks = protect(body)
    blocks_json.parent.mkdir(parents=True, exist_ok=True)
    blocks_json.write_text(json.dumps(blocks, ensure_ascii=False), encoding="utf-8")
    new_post = frontmatter.Post(protected_body, **post.metadata)
    tmp_input.parent.mkdir(parents=True, exist_ok=True)
    tmp_input.write_text(frontmatter.dumps(new_post), encoding="utf-8")
    print(f"protected: {len(blocks)} blocks → {tmp_input}")
    return 0


def cmd_restore(subagent_out: Path, blocks_json: Path, final_path: Path) -> int:
    translated = subagent_out.read_text(encoding="utf-8")
    blocks = json.loads(blocks_json.read_text(encoding="utf-8"))
    post = frontmatter.loads(translated)
    body = post.content

    # Validate before restore
    if blocks and not body:
        print("FAIL: empty body after translation", file=sys.stderr)
        return 1
    if post.metadata.get("translated") is not True:
        print("FAIL: frontmatter translated != true", file=sys.stderr)
        return 1

    try:
        restored_body = restore(body, blocks)
    except ValueError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1

    if has_sentinels(restored_body):
        print("FAIL: leftover sentinels after restore", file=sys.stderr)
        return 1

    fences = restored_body.count("```")
    if fences % 2 != 0:
        print(f"FAIL: unbalanced code fences ({fences})", file=sys.stderr)
        return 1

    new_post = frontmatter.Post(restored_body, **post.metadata)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = final_path.with_suffix(final_path.suffix + ".tmp")
    tmp.write_text(frontmatter.dumps(new_post), encoding="utf-8", newline="\n")
    tmp.replace(final_path)
    print(f"restored: {len(blocks)} blocks → {final_path}")
    return 0


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__, file=sys.stderr)
        return 2
    op = sys.argv[1]
    if op == "protect":
        return cmd_protect(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    if op == "restore":
        return cmd_restore(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    print(f"unknown op: {op}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
