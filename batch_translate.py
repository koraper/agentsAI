#!/usr/bin/env python3
"""
Batch translate markdown files using Claude API via subprocess
"""
import os
import subprocess
import json
from pathlib import Path

def translate_with_claude(text: str) -> str:
    """Translate text using claude CLI"""
    if not text.strip():
        return text

    try:
        # Use claude CLI directly
        result = subprocess.run(
            ['claude', 'ask'],
            input=f"""Translate to Korean (한글). Keep markdown formatting, code blocks, and links exactly as-is. Only translate human text:

{text}""",
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Translation error: {result.stderr}")
            return text
    except FileNotFoundError:
        print("Error: 'claude' CLI not found. Using python import instead.")
        # Fallback to python
        try:
            from anthropic import Anthropic
            client = Anthropic()
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": f"""Translate to Korean (한글). Keep markdown formatting, code blocks, and links exactly as-is. Only translate human text:

{text}"""
                }]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Python fallback error: {e}")
            return text

def main():
    src_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/plugins")
    dst_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/pluginsK")

    # Find all markdown files
    md_files = sorted(src_dir.glob("**/*.md"))
    print(f"Found {len(md_files)} markdown files")

    translated = 0
    failed = 0

    for i, src_file in enumerate(md_files, 1):
        rel_path = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel_path

        # Skip if already translated (has Korean characters)
        if dst_file.exists():
            with open(dst_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if any('\uac00' <= c <= '\ud7af' for c in content):  # Korean Unicode range
                    print(f"[{i}/{len(md_files)}] SKIP (already translated): {rel_path}")
                    continue

        print(f"[{i}/{len(md_files)}] Translating: {rel_path}")

        try:
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()

            translated_content = translate_with_claude(content)

            # Ensure destination directory exists
            dst_file.parent.mkdir(parents=True, exist_ok=True)

            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)

            print(f"  ✓ Saved to: {rel_path}")
            translated += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1

    print(f"\n✓ Complete!")
    print(f"  Translated: {translated}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(md_files)}")

if __name__ == "__main__":
    main()
