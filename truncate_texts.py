#!/usr/bin/env python3
"""
Text Truncation Script
Extracts the first ~1500 characters from .txt files, ending at the nearest sentence.
"""

import os
import sys
from pathlib import Path


def find_sentence_break(text: str, target_length: int = 1500, lookback: int = 200) -> int:
    """
    Find the nearest sentence ending (. ! ?) at or before target_length.
    If no sentence break found in the last `lookback` characters, return target_length.

    Args:
        text: The text to search
        target_length: Target character count
        lookback: How far back to search for sentence endings

    Returns:
        The position to truncate at
    """
    if len(text) <= target_length:
        return len(text)

    # Search for sentence endings in the range [target_length - lookback, target_length]
    search_start = max(0, target_length - lookback)
    search_region = text[search_start:target_length]

    # Find the last sentence ending in the search region
    last_break = -1
    for i, char in enumerate(search_region):
        if char in '.!?':
            # Make sure this isn't followed by more sentence-ending punctuation
            # and account for potential quotes or parentheses after
            last_break = i

    if last_break != -1:
        # Return position after the sentence ending (include the punctuation)
        return search_start + last_break + 1

    # No sentence break found, fall back to exact target_length
    return target_length


def truncate_text(text: str, target_length: int = 1500) -> str:
    """
    Truncate text to approximately target_length characters, ending at a sentence.

    Args:
        text: The text to truncate
        target_length: Target character count

    Returns:
        Truncated text
    """
    if not text:
        return text

    if len(text) <= target_length:
        return text

    break_pos = find_sentence_break(text, target_length)
    return text[:break_pos].rstrip()


def process_files(source_folder: str) -> tuple[int, str]:
    """
    Process all .txt files in the source folder.

    Args:
        source_folder: Path to folder containing .txt files

    Returns:
        Tuple of (files_processed, output_folder_path)
    """
    source_path = Path(source_folder).resolve()

    # Validate source folder
    if not source_path.exists():
        print(f"Error: Source folder does not exist: {source_path}")
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Error: Source path is not a directory: {source_path}")
        sys.exit(1)

    # Create output folder
    output_folder = Path.home() / "Desktop" / "TruncatedScripts"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Find all .txt files
    txt_files = list(source_path.glob("*.txt"))

    if not txt_files:
        print(f"No .txt files found in: {source_path}")
        return 0, str(output_folder)

    print(f"Found {len(txt_files)} .txt file(s) in: {source_path}")
    print(f"Output folder: {output_folder}")
    print("-" * 50)

    files_processed = 0

    for txt_file in txt_files:
        try:
            # Read file content
            content = txt_file.read_text(encoding='utf-8')

            # Handle empty files
            if not content.strip():
                print(f"[SKIP] {txt_file.name} - empty file")
                continue

            original_length = len(content)

            # Truncate text
            truncated = truncate_text(content)
            truncated_length = len(truncated)

            # Generate output filename
            output_filename = f"{txt_file.stem}_truncated.txt"
            output_path = output_folder / output_filename

            # Write output file
            output_path.write_text(truncated, encoding='utf-8')

            # Report status
            if truncated_length < original_length:
                print(f"[OK] {txt_file.name} ({original_length} → {truncated_length} chars)")
            else:
                print(f"[OK] {txt_file.name} ({original_length} chars, full content copied)")

            files_processed += 1

        except UnicodeDecodeError:
            print(f"[ERROR] {txt_file.name} - could not decode file (not UTF-8)")
        except Exception as e:
            print(f"[ERROR] {txt_file.name} - {e}")

    return files_processed, str(output_folder)


def main():
    if len(sys.argv) != 2:
        print("Usage: python truncate_texts.py <source_folder>")
        print("Example: python truncate_texts.py /path/to/txt/files")
        sys.exit(1)

    source_folder = sys.argv[1]

    print("=" * 50)
    print("Text Truncation Script")
    print("=" * 50)

    files_processed, output_folder = process_files(source_folder)

    print("-" * 50)
    print(f"Summary: {files_processed} file(s) processed, saved to {output_folder}")
    print("=" * 50)


if __name__ == "__main__":
    main()
