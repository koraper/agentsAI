#!/usr/bin/env python3
"""
Translate all markdown files from plugins folder to Korean and save to pluginsK folder
"""

import os
import shutil
import json
import re
from pathlib import Path
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

def translate_text(text: str) -> str:
    """Translate text to Korean using Claude API"""
    if not text.strip():
        return text

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"""Translate the following markdown content to Korean (한글).
Keep all markdown formatting, code blocks, links, and structure exactly as is.
Only translate the text content, not the code or filenames.
Keep technical terms that are commonly used in English in the Korean context if they are more commonly understood in English.

Content to translate:
{text}"""
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def copy_folder_structure(src: str, dst: str):
    """Create destination folder structure"""
    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)

def translate_file(src_file: str, dst_file: str):
    """Translate a single markdown file"""
    try:
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Translating: {src_file}...")
        translated_content = translate_text(content)

        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)

        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"✓ Saved to: {dst_file}")
        return True
    except Exception as e:
        print(f"Error translating {src_file}: {e}")
        return False

def main():
    src_plugins = "/Users/kevinjang0301/workprivate/agentsAI/plugins"
    dst_plugins = "/Users/kevinjang0301/workprivate/agentsAI/pluginsK"

    # Create destination root directory
    os.makedirs(dst_plugins, exist_ok=True)

    # Copy folder structure first
    print("Creating folder structure...")
    copy_folder_structure(src_plugins, dst_plugins)

    # Walk through all files and translate markdown files
    translated_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(src_plugins):
        for file in files:
            src_file = os.path.join(root, file)

            # Calculate relative path
            rel_path = os.path.relpath(src_file, src_plugins)
            dst_file = os.path.join(dst_plugins, rel_path)

            if file.endswith('.md'):
                # Translate markdown files
                if translate_file(src_file, dst_file):
                    translated_count += 1
            elif file in ['PLUGIN.md', 'SKILL.md', 'README.md']:
                # Also translate these special files if they don't have .md extension (unlikely)
                if translate_file(src_file, dst_file):
                    translated_count += 1
            else:
                # Copy non-markdown files as is
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                try:
                    shutil.copy2(src_file, dst_file)
                    skipped_count += 1
                except Exception as e:
                    print(f"Error copying {src_file}: {e}")

    print(f"\n✓ Translation complete!")
    print(f"  Translated files: {translated_count}")
    print(f"  Copied files: {skipped_count}")
    print(f"  Destination: {dst_plugins}")

if __name__ == "__main__":
    main()
