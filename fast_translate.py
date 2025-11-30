#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Try to use Anthropic
try:
    from anthropic import Anthropic
    client = Anthropic()  # Auto-detects API key from environment
except ImportError:
    print("Error: anthropic package not installed")
    sys.exit(1)
except Exception as e:
    print(f"Error initializing Anthropic: {e}")
    sys.exit(1)

def translate_markdown(content: str) -> str:
    """Translate markdown content to Korean"""
    if not content.strip():
        return content

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Please translate the following markdown content to Korean (한글).

**Important rules:**
1. Keep all markdown formatting (headers, code blocks, links, etc.) exactly as-is
2. Do NOT translate code, variable names, URLs, or technical terms in code blocks
3. Do NOT translate YAML frontmatter (the --- parts)
4. Only translate the human-readable descriptions and text
5. Keep the file structure and formatting perfectly

Content to translate:
{content}"""
            }]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Translation API error: {e}")
        return content

def main():
    src_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/plugins")
    dst_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/pluginsK")

    # Get all markdown files
    md_files = list(src_dir.glob("**/*.md"))
    print(f"Found {len(md_files)} markdown files to translate")

    successful = 0
    failed = 0
    skipped = 0

    for idx, src_file in enumerate(md_files, 1):
        rel_path = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel_path

        try:
            # Read source
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Translate
            print(f"[{idx}/{len(md_files)}] Translating: {rel_path}...", end=" ", flush=True)
            translated = translate_markdown(content)

            # Save
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write(translated)

            print("✓")
            successful += 1

        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
            failed += 1

    print(f"\n=== Translation Complete ===")
    print(f"Successful: {successful}/{len(md_files)}")
    print(f"Failed: {failed}/{len(md_files)}")
    print(f"Output: {dst_dir}")

if __name__ == "__main__":
    main()
