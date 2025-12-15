# Text Truncation Script - Mac User Guide

A beginner-friendly guide to running the `truncate_texts.py` script on macOS.

---

## Table of Contents

1. [What This Script Does](#what-this-script-does)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Instructions](#step-by-step-instructions)
4. [Examples](#examples)
5. [Understanding the Output](#understanding-the-output)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## What This Script Does

This script takes a folder full of `.txt` files and creates shortened versions of each file:

- **Extracts the first ~1500 characters** from each text file
- **Ends at a complete sentence** (doesn't cut off mid-sentence)
- **Saves the shortened files** to your Desktop in a folder called `TruncatedScripts`
- **Preserves original files** - your source files are never modified

---

## Prerequisites

### Check if Python 3 is Installed

Mac comes with Python, but let's verify you have Python 3:

1. **Open Terminal** (see instructions below)
2. **Type this command and press Enter:**
   ```
   python3 --version
   ```
3. **You should see something like:**
   ```
   Python 3.11.4
   ```
   (The exact number may vary - any version 3.x is fine)

### How to Open Terminal on Mac

**Option 1: Using Spotlight (Fastest)**
1. Press `Command (⌘) + Space` to open Spotlight
2. Type `Terminal`
3. Press `Enter` or click on Terminal

**Option 2: Using Finder**
1. Open **Finder**
2. Go to **Applications** → **Utilities**
3. Double-click **Terminal**

**Option 3: Using Launchpad**
1. Click the **Launchpad** icon in the Dock (rocket ship icon)
2. Type `Terminal` in the search bar
3. Click **Terminal**

---

## Step-by-Step Instructions

### Step 1: Download the Script

Save the `truncate_texts.py` file somewhere on your Mac. Common locations:
- Your **Downloads** folder: `/Users/YOURUSERNAME/Downloads/`
- Your **Documents** folder: `/Users/YOURUSERNAME/Documents/`
- Your **Desktop**: `/Users/YOURUSERNAME/Desktop/`

### Step 2: Know Your Folder Paths

You need to know two paths:
1. **Where the script is saved** (e.g., `/Users/YOURUSERNAME/Downloads/truncate_texts.py`)
2. **Where your .txt files are** (e.g., `/Users/YOURUSERNAME/Documents/MyTextFiles/`)

#### How to Find a Folder's Path on Mac

**Method 1: Drag and Drop (Easiest)**
1. Open Terminal
2. Type `cd ` (with a space after it) - don't press Enter yet
3. Drag the folder from Finder into the Terminal window
4. The path will appear automatically!

**Method 2: Using Finder**
1. Open Finder and navigate to the folder
2. Right-click (or Control-click) on the folder
3. Hold the **Option (⌥)** key
4. Click **Copy "FolderName" as Pathname**
5. Now you can paste (Command+V) the path anywhere

### Step 3: Run the Script

1. **Open Terminal**

2. **Type the command in this format:**
   ```
   python3 /path/to/truncate_texts.py /path/to/your/txt/files
   ```

3. **Press Enter**

---

## Examples

### Example 1: Script in Downloads, Text Files in Documents

Let's say:
- You saved the script to your Downloads folder
- Your text files are in a folder called "Scripts" in Documents
- Your username is "john"

**Command:**
```
python3 /Users/john/Downloads/truncate_texts.py /Users/john/Documents/Scripts
```

### Example 2: Using the ~ Shortcut

The `~` symbol is a shortcut for your home folder (`/Users/YOURUSERNAME`).

**These two commands are identical:**
```
python3 /Users/john/Downloads/truncate_texts.py /Users/john/Documents/Scripts
python3 ~/Downloads/truncate_texts.py ~/Documents/Scripts
```

### Example 3: Script and Files Both on Desktop

```
python3 ~/Desktop/truncate_texts.py ~/Desktop/MyTextFiles
```

### Example 4: Folder Name with Spaces

If your folder name has spaces, wrap the path in quotes:

```
python3 ~/Downloads/truncate_texts.py "/Users/john/Documents/My Text Files"
```

Or use backslashes before each space:

```
python3 ~/Downloads/truncate_texts.py /Users/john/Documents/My\ Text\ Files
```

---

## Understanding the Output

### While Running

You'll see output like this:

```
==================================================
Text Truncation Script
==================================================
Found 5 .txt file(s) in: /Users/john/Documents/Scripts
Output folder: /Users/john/Desktop/TruncatedScripts
--------------------------------------------------
[OK] chapter1.txt (5420 → 1487 chars)
[OK] chapter2.txt (8932 → 1456 chars)
[OK] short_note.txt (340 chars, full content copied)
[SKIP] empty_file.txt - empty file
[OK] chapter3.txt (12050 → 1499 chars)
--------------------------------------------------
Summary: 4 file(s) processed, saved to /Users/john/Desktop/TruncatedScripts
==================================================
```

### What Each Status Means

| Status | Meaning |
|--------|---------|
| `[OK]` | File processed successfully |
| `[SKIP]` | File was skipped (empty file) |
| `[ERROR]` | Something went wrong with this file |

### Where to Find Your Output Files

After running the script:

1. Open **Finder**
2. Go to your **Desktop**
3. Look for a folder called **TruncatedScripts**
4. Your truncated files will be inside, named like:
   - `chapter1_truncated.txt`
   - `chapter2_truncated.txt`
   - etc.

---

## Troubleshooting

### "command not found: python3"

**Problem:** Python 3 isn't installed or isn't in your PATH.

**Solution:** Install Python from [python.org](https://www.python.org/downloads/macos/)

### "No such file or directory"

**Problem:** The path to the script or folder is wrong.

**Solutions:**
1. Double-check the path for typos
2. Use the drag-and-drop method to get the correct path
3. Make sure the file/folder actually exists

### "Permission denied"

**Problem:** You don't have permission to read the files or write to the output folder.

**Solution:** Try running with your own folders (Documents, Desktop, etc.)

### "No .txt files found"

**Problem:** The source folder doesn't contain any `.txt` files.

**Solutions:**
1. Make sure your files have the `.txt` extension
2. Check that you're pointing to the correct folder
3. Note: The script only looks at files directly in the folder, not in subfolders

### Script Runs But Nothing Happens

**Problem:** The script might be looking at an empty folder.

**Solution:** Navigate to the folder in Finder and verify it contains `.txt` files

---

## FAQ

### Q: Will my original files be changed?
**A:** No! The script only reads your original files and creates new copies. Your originals are never modified.

### Q: Can I change where the output files are saved?
**A:** The script always saves to `~/Desktop/TruncatedScripts/`. If you need a different location, you'd need to edit the script.

### Q: What if I run the script twice?
**A:** The output files will be overwritten with new versions. The script doesn't create duplicates.

### Q: Does it work with .doc or .docx files?
**A:** No, only `.txt` files. You'd need to convert other formats to `.txt` first.

### Q: Can I process files in subfolders?
**A:** No, the script only processes `.txt` files directly in the folder you specify, not in subfolders.

### Q: What counts as a "sentence ending"?
**A:** The script looks for periods (.), exclamation marks (!), and question marks (?).

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    QUICK REFERENCE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Basic Command Format:                                      │
│  python3 /path/to/script.py /path/to/txt/folder            │
│                                                             │
│  Example:                                                   │
│  python3 ~/Downloads/truncate_texts.py ~/Documents/Texts   │
│                                                             │
│  Output Location:                                           │
│  ~/Desktop/TruncatedScripts/                                │
│                                                             │
│  Output Filename Format:                                    │
│  originalname_truncated.txt                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Need More Help?

If you're still having trouble:

1. Make sure you copied the command exactly as shown
2. Check that all paths are correct
3. Verify your `.txt` files exist in the source folder
4. Try with a simple test folder first

---

*Last updated: December 2024*
