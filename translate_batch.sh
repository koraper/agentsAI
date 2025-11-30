#!/bin/bash

# Complete Korean translation script
# This script will process all markdown files in batches

SOURCE_DIR="/Users/kevinjang0301/workprivate/agentsAI/plugins"
TARGET_DIR="/Users/kevinjang0301/workprivate/agentsAI/pluginsK"

# Create target directory structure
echo "Creating directory structure..."
find "$SOURCE_DIR" -type d | while read dir; do
    target_dir="${dir/$SOURCE_DIR/$TARGET_DIR}"
    mkdir -p "$target_dir"
done

# Get list of all markdown files
echo "Finding all markdown files..."
find "$SOURCE_DIR" -type f -name "*.md" > /tmp/md_files_list.txt

total=$(wc -l < /tmp/md_files_list.txt)
echo "Found $total markdown files to process"

# Save file list for manual processing
cp /tmp/md_files_list.txt /Users/kevinjang0301/workprivate/agentsAI/files_to_translate.txt

echo "File list saved to: /Users/kevinjang0301/workprivate/agentsAI/files_to_translate.txt"
echo "Ready for translation processing"
