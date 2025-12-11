#!/usr/bin/env python3
"""
Batch Image Organizer

A Python script that reorganizes images from nested subfolders into batched folders
of a configurable size (default: 1000 images per batch).

This tool is useful for organizing large collections of images that are scattered
across multiple directories into a flat, manageable batch structure.

Author: Generated with Claude
License: MIT
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple, Set

# ============================================================================
# CONFIGURATION
# ============================================================================

# Supported image file extensions (case-insensitive)
SUPPORTED_EXTENSIONS: Set[str] = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif'
}

# Default batch size (number of images per folder)
DEFAULT_BATCH_SIZE: int = 1000

# Default output folder name
DEFAULT_OUTPUT_FOLDER: str = "batched_output"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_image_file(file_path: Path) -> bool:
    """
    Check if a file is a supported image type based on its extension.

    Args:
        file_path: Path object pointing to the file to check.

    Returns:
        True if the file has a supported image extension, False otherwise.
    """
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def scan_for_images(source_dir: Path) -> List[Path]:
    """
    Recursively scan a directory and all its subdirectories for image files.

    This function walks through the entire directory tree starting from
    source_dir and collects all files that have supported image extensions.

    Args:
        source_dir: Path object pointing to the root directory to scan.

    Returns:
        A sorted list of Path objects for all found image files.
        The list is sorted to ensure consistent ordering across runs.
    """
    image_files: List[Path] = []

    # Walk through all directories recursively
    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)

        # Check each file in the current directory
        for filename in files:
            file_path = root_path / filename

            # Add to list if it's a supported image type
            if is_image_file(file_path):
                image_files.append(file_path)

    # Sort for consistent ordering (by full path)
    return sorted(image_files)


def generate_unique_filename(dest_dir: Path, original_name: str,
                              used_names: Set[str]) -> str:
    """
    Generate a unique filename to handle duplicates.

    If the original filename already exists in the destination or has been
    used in this batch, append a number to make it unique.

    Args:
        dest_dir: Path object for the destination directory.
        original_name: The original filename to use if possible.
        used_names: Set of filenames already used in this session.

    Returns:
        A unique filename string that won't conflict with existing files.

    Example:
        If "photo.jpg" exists, returns "photo_1.jpg"
        If "photo_1.jpg" also exists, returns "photo_2.jpg"
    """
    # Check if the original name is available
    if original_name not in used_names and not (dest_dir / original_name).exists():
        return original_name

    # Split filename into name and extension
    name_path = Path(original_name)
    base_name = name_path.stem  # filename without extension
    extension = name_path.suffix  # extension including the dot

    # Try incrementing numbers until we find a unique name
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{extension}"

        # Check both the used_names set and the actual filesystem
        if new_name not in used_names and not (dest_dir / new_name).exists():
            return new_name

        counter += 1

        # Safety limit to prevent infinite loops
        if counter > 100000:
            raise RuntimeError(f"Could not generate unique filename for {original_name}")


def format_batch_name(batch_number: int) -> str:
    """
    Format a batch number into a zero-padded folder name.

    Args:
        batch_number: The batch number (1-indexed).

    Returns:
        Formatted batch folder name like "batch_001", "batch_002", etc.
    """
    return f"batch_{batch_number:03d}"


def create_batch_folders(
    image_files: List[Path],
    output_dir: Path,
    batch_size: int,
    dry_run: bool = False
) -> List[Tuple[Path, Path, str]]:
    """
    Organize images into batch folders.

    This is the main processing function that:
    1. Creates batch directories as needed
    2. Assigns each image to a batch
    3. Handles duplicate filenames
    4. Copies files (unless in dry-run mode)

    Args:
        image_files: List of Path objects for source images.
        output_dir: Path object for the output directory.
        batch_size: Number of images per batch folder.
        dry_run: If True, don't actually copy files, just report what would happen.

    Returns:
        List of tuples containing (source_path, dest_path, dest_filename)
        for each processed image.
    """
    operations: List[Tuple[Path, Path, str]] = []

    # Track total number of images to process
    total_images = len(image_files)

    if total_images == 0:
        print("No images found to process.")
        return operations

    # Calculate total number of batches needed
    total_batches = (total_images + batch_size - 1) // batch_size

    print(f"\nFound {total_images} images to organize into {total_batches} batch(es)")
    print(f"Batch size: {batch_size} images per folder")
    print(f"Output directory: {output_dir}")
    print("-" * 60)

    # Create the main output directory if not in dry-run mode
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Process images in batches
    current_batch = 1
    current_batch_count = 0
    current_batch_dir: Path = output_dir / format_batch_name(current_batch)
    used_names_in_batch: Set[str] = set()

    for index, source_path in enumerate(image_files, start=1):
        # Check if we need to start a new batch
        if current_batch_count >= batch_size:
            current_batch += 1
            current_batch_count = 0
            current_batch_dir = output_dir / format_batch_name(current_batch)
            used_names_in_batch.clear()  # Reset used names for new batch

        # Create batch directory if this is the first image in the batch
        if current_batch_count == 0 and not dry_run:
            current_batch_dir.mkdir(parents=True, exist_ok=True)

        # Generate a unique filename for this image in the current batch
        original_filename = source_path.name
        unique_filename = generate_unique_filename(
            current_batch_dir,
            original_filename,
            used_names_in_batch
        )

        # Mark this filename as used
        used_names_in_batch.add(unique_filename)

        # Full destination path
        dest_path = current_batch_dir / unique_filename

        # Record this operation
        operations.append((source_path, current_batch_dir, unique_filename))

        # Copy the file if not in dry-run mode
        if not dry_run:
            shutil.copy2(source_path, dest_path)  # copy2 preserves metadata

        # Update batch counter
        current_batch_count += 1

        # Print progress every 100 images or at significant milestones
        if index % 100 == 0 or index == total_images:
            percentage = (index / total_images) * 100
            mode_str = "[DRY RUN] " if dry_run else ""
            print(f"{mode_str}Progress: {index}/{total_images} images ({percentage:.1f}%) - Batch {current_batch}")

    return operations


def print_summary(
    operations: List[Tuple[Path, Path, str]],
    output_dir: Path,
    batch_size: int,
    dry_run: bool
) -> None:
    """
    Print a summary of the batch operation.

    Args:
        operations: List of (source, dest_dir, filename) tuples.
        output_dir: Path to the output directory.
        batch_size: Number of images per batch.
        dry_run: Whether this was a dry run.
    """
    total_images = len(operations)

    if total_images == 0:
        print("\n" + "=" * 60)
        print("SUMMARY: No images were processed.")
        print("=" * 60)
        return

    # Count batches created
    batches_used = set()
    for _, dest_dir, _ in operations:
        batches_used.add(dest_dir.name)

    # Count renamed files (duplicates that needed unique names)
    renamed_count = sum(
        1 for source, _, dest_name in operations
        if source.name != dest_name
    )

    # Print summary
    print("\n" + "=" * 60)
    mode_str = "DRY RUN " if dry_run else ""
    print(f"{mode_str}SUMMARY")
    print("=" * 60)
    print(f"Total images processed: {total_images}")
    print(f"Batch folders created:  {len(batches_used)}")
    print(f"Files renamed (duplicates): {renamed_count}")
    print(f"Output location: {output_dir}")

    if dry_run:
        print("\n*** This was a DRY RUN - no files were actually copied ***")
        print("Run without --dry-run to perform the actual copy.")
    else:
        print("\nAll images have been successfully copied to batch folders!")

    print("=" * 60)


def print_detailed_preview(
    operations: List[Tuple[Path, Path, str]],
    max_items: int = 20
) -> None:
    """
    Print a detailed preview of operations (useful for dry-run mode).

    Args:
        operations: List of (source, dest_dir, filename) tuples.
        max_items: Maximum number of items to show in preview.
    """
    if not operations:
        return

    print("\nPreview of operations:")
    print("-" * 60)

    # Group by batch
    batches = {}
    for source, dest_dir, filename in operations:
        batch_name = dest_dir.name
        if batch_name not in batches:
            batches[batch_name] = []
        batches[batch_name].append((source, filename))

    # Print each batch
    items_shown = 0
    for batch_name in sorted(batches.keys()):
        if items_shown >= max_items:
            remaining = len(operations) - items_shown
            print(f"\n... and {remaining} more files")
            break

        print(f"\n{batch_name}/")
        for source, filename in batches[batch_name][:5]:
            renamed = " (renamed)" if source.name != filename else ""
            print(f"  {filename}{renamed} <- {source}")
            items_shown += 1

            if items_shown >= max_items:
                break

        if len(batches[batch_name]) > 5:
            print(f"  ... and {len(batches[batch_name]) - 5} more in this batch")


# ============================================================================
# MAIN FUNCTION AND CLI
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse and validate command-line arguments.

    Returns:
        Parsed arguments as a Namespace object.
    """
    parser = argparse.ArgumentParser(
        prog='batch_images',
        description='Reorganize images from nested subfolders into batched folders.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/photos
      Scan /path/to/photos and create batched_output/ in current directory

  %(prog)s /path/to/photos --output /path/to/output
      Create batch folders in specified output directory

  %(prog)s /path/to/photos --dry-run
      Preview what would happen without copying files

  %(prog)s /path/to/photos --batch-size 500
      Create batches of 500 images instead of 1000

Supported image formats: jpg, jpeg, png, gif, webp, bmp, tiff
        """
    )

    # Required argument: source folder
    parser.add_argument(
        'source',
        type=str,
        help='Source folder containing images (will scan recursively)'
    )

    # Optional: output directory
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help=f'Output directory for batch folders (default: ./{DEFAULT_OUTPUT_FOLDER})'
    )

    # Optional: batch size
    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f'Number of images per batch folder (default: {DEFAULT_BATCH_SIZE})'
    )

    # Optional: dry run mode
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview operations without actually copying files'
    )

    # Optional: verbose mode
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed preview of file operations'
    )

    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Tuple[Path, Path]:
    """
    Validate the parsed arguments and convert to Path objects.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Tuple of (source_path, output_path) as Path objects.

    Raises:
        SystemExit: If validation fails.
    """
    # Validate source directory
    source_path = Path(args.source).resolve()

    if not source_path.exists():
        print(f"Error: Source directory does not exist: {source_path}")
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Error: Source path is not a directory: {source_path}")
        sys.exit(1)

    # Set up output directory
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = Path.cwd() / DEFAULT_OUTPUT_FOLDER

    # Check that output is not inside source (would cause issues)
    try:
        output_path.relative_to(source_path)
        print("Error: Output directory cannot be inside the source directory")
        sys.exit(1)
    except ValueError:
        # This is expected - output is not inside source
        pass

    # Validate batch size
    if args.batch_size < 1:
        print(f"Error: Batch size must be at least 1, got: {args.batch_size}")
        sys.exit(1)

    if args.batch_size > 100000:
        print(f"Warning: Very large batch size ({args.batch_size}). Are you sure?")

    return source_path, output_path


def main() -> None:
    """
    Main entry point for the batch image organizer script.

    This function orchestrates the entire process:
    1. Parse command-line arguments
    2. Validate inputs
    3. Scan for images
    4. Create batch folders and copy files
    5. Print summary
    """
    # Parse and validate arguments
    args = parse_arguments()
    source_path, output_path = validate_arguments(args)

    # Print header
    print("=" * 60)
    print("BATCH IMAGE ORGANIZER")
    print("=" * 60)
    print(f"Source: {source_path}")
    print(f"Output: {output_path}")
    print(f"Batch size: {args.batch_size}")
    print(f"Mode: {'DRY RUN (no files will be copied)' if args.dry_run else 'LIVE'}")

    # Scan for images
    print("\nScanning for images...")
    image_files = scan_for_images(source_path)

    if not image_files:
        print("\nNo image files found in the source directory.")
        print(f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        sys.exit(0)

    # Process images into batches
    operations = create_batch_folders(
        image_files,
        output_path,
        args.batch_size,
        args.dry_run
    )

    # Show detailed preview if verbose mode
    if args.verbose or args.dry_run:
        print_detailed_preview(operations)

    # Print summary
    print_summary(operations, output_path, args.batch_size, args.dry_run)


if __name__ == '__main__':
    main()
