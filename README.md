# Batch Image Organizer

A Python command-line tool that reorganizes images scattered across nested subfolders into neatly organized batch folders of configurable size.

## Description

When dealing with large collections of images spread across multiple directories (from camera imports, downloads, etc.), this tool helps you consolidate them into a flat, manageable structure. It scans a source directory recursively, finds all image files, and copies them into sequentially numbered batch folders.

## Features

- **Recursive scanning** - Finds images in all subdirectories, no matter how deeply nested
- **Multiple format support** - Handles JPG, JPEG, PNG, GIF, WebP, BMP, and TIFF images
- **Configurable batch size** - Default 1000 images per folder, but fully customizable
- **Safe copy operation** - Copies files instead of moving them, preserving your originals
- **Duplicate handling** - Automatically renames files with conflicting names (e.g., `photo.jpg` → `photo_1.jpg`)
- **Dry-run mode** - Preview what will happen before committing to any changes
- **Progress reporting** - Real-time progress updates and detailed summary
- **Preserves metadata** - Uses `shutil.copy2` to maintain original file timestamps
- **Cross-platform** - Works on Windows, macOS, and Linux

## Prerequisites

- **Python 3.6 or higher** (uses f-strings and type hints)
- No external dependencies required (uses only Python standard library)

### Checking Your Python Version

```bash
python --version
# or
python3 --version
```

## Installation

1. Download the `batch_images.py` script to your local machine:

```bash
# Clone the repository or download directly
curl -O https://raw.githubusercontent.com/your-repo/batch_images.py

# Or simply copy the script to your desired location
```

2. Make the script executable (Linux/macOS):

```bash
chmod +x batch_images.py
```

3. Verify it works:

```bash
python batch_images.py --help
```

## Usage

### Basic Syntax

```bash
python batch_images.py <source_folder> [options]
```

### CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `source` | | **Required.** Path to folder containing images | - |
| `--output` | `-o` | Output directory for batch folders | `./batched_output` |
| `--batch-size` | `-b` | Number of images per batch folder | `1000` |
| `--dry-run` | `-n` | Preview without copying files | `False` |
| `--verbose` | `-v` | Show detailed file operations | `False` |
| `--help` | `-h` | Show help message | - |

## Usage Examples

### Basic Usage

Scan a folder and create batch folders in the current directory:

```bash
python batch_images.py /path/to/my/photos
```

This creates a `batched_output` folder in your current directory containing `batch_001`, `batch_002`, etc.

### Custom Output Directory

Specify where to create the batch folders:

```bash
python batch_images.py /path/to/source --output /path/to/destination
```

### Dry Run (Preview Mode)

See what would happen without copying any files:

```bash
python batch_images.py /path/to/photos --dry-run
```

This is **highly recommended** before running on large collections!

### Custom Batch Size

Create smaller batches of 500 images each:

```bash
python batch_images.py /path/to/photos --batch-size 500
```

Or larger batches of 2000:

```bash
python batch_images.py /path/to/photos -b 2000
```

### Verbose Output with Dry Run

Get maximum detail about what will happen:

```bash
python batch_images.py /path/to/photos --dry-run --verbose
```

### Full Example

```bash
python batch_images.py ~/Pictures/Vacation2023 \
    --output ~/Pictures/Organized \
    --batch-size 500 \
    --dry-run \
    --verbose
```

## Example Folder Structure

### Before

```
source_folder/
├── Camera/
│   ├── 2023-01/
│   │   ├── IMG_0001.jpg
│   │   ├── IMG_0002.jpg
│   │   └── photo.png
│   └── 2023-02/
│       ├── IMG_0003.jpg
│       └── photo.png          # Duplicate filename!
├── Downloads/
│   ├── wallpaper.jpg
│   └── screenshot.png
└── Misc/
    └── old/
        └── archive/
            ├── pic1.gif
            └── pic2.webp
```

### After (with --batch-size 5)

```
batched_output/
├── batch_001/
│   ├── IMG_0001.jpg
│   ├── IMG_0002.jpg
│   ├── IMG_0003.jpg
│   ├── photo.png
│   └── photo_1.png            # Renamed to avoid conflict
└── batch_002/
    ├── pic1.gif
    ├── pic2.webp
    ├── screenshot.png
    └── wallpaper.jpg
```

Note: The original `source_folder` remains unchanged!

## Supported Image Formats

The following file extensions are recognized (case-insensitive):

- `.jpg`, `.jpeg` - JPEG images
- `.png` - PNG images
- `.gif` - GIF images (including animated)
- `.webp` - WebP images
- `.bmp` - Bitmap images
- `.tiff`, `.tif` - TIFF images

## Troubleshooting

### "No image files found in the source directory"

**Cause:** The script didn't find any files with supported extensions.

**Solutions:**
- Verify the source path is correct
- Check that your images have standard extensions (the tool is case-insensitive, but extensions like `.jpeg2000` aren't supported)
- Ensure you have read permissions for the source directory

### "Source directory does not exist"

**Cause:** The provided path doesn't exist or is misspelled.

**Solutions:**
- Double-check the path for typos
- Use absolute paths instead of relative paths
- On Windows, use forward slashes or escape backslashes: `C:/Users/...` or `C:\\Users\\...`

### "Output directory cannot be inside the source directory"

**Cause:** You're trying to create the output folder inside the source folder.

**Solution:** Choose an output directory that's not a subdirectory of your source:

```bash
# Bad - output is inside source
python batch_images.py /photos --output /photos/organized

# Good - output is separate
python batch_images.py /photos --output /organized_photos
```

### "Permission denied" errors

**Cause:** Insufficient permissions to read source or write to output.

**Solutions:**
- Ensure you have read access to the source folder
- Ensure you have write access to the output location
- On Linux/macOS, you may need to use `sudo` (not recommended) or fix permissions

### Script runs slowly with many images

**Cause:** Processing tens of thousands of images takes time.

**Solutions:**
- This is normal behavior - the script shows progress every 100 images
- Use `--dry-run` first to estimate the scope
- Consider running overnight for very large collections
- The bottleneck is usually disk I/O, not the script itself

### Duplicate handling creates many numbered files

**Cause:** Multiple source files have the same name.

**This is expected behavior.** The script preserves all files by appending numbers:
- `photo.jpg` (first occurrence)
- `photo_1.jpg` (second occurrence)
- `photo_2.jpg` (third occurrence)

To avoid this, consider renaming files before processing or using folder-based prefixes in your workflow.

### Memory usage with huge collections

The script loads the file list into memory but doesn't load image contents. Even with millions of files, memory usage should stay reasonable (under 1GB). If you have concerns:

```bash
# Check how many images first
find /path/to/source -type f \( -iname "*.jpg" -o -iname "*.png" \) | wc -l
```

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
