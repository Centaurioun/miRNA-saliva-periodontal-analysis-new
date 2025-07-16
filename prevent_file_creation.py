#!/usr/bin/env python3
"""
File Creation Prevention Script
This script prevents automatic creation of specific files in the repository root.
Run this script to set up protection against unwanted file creation.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# List of files that should NOT be created in the root directory
PROHIBITED_FILES = [
    "COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md",
    "COMPREHENSIVE_ANALYSIS_RESULTS_REPORT.md", 
    "FINAL_ANALYSIS_REPORT.md",
    "fix_columns.py",
    "miRNA_analysis.py",
    "miRNA_analysis_part2.py",
    "miRNA_analysis_part3.py", 
    "miRNA_analysis_part4.py",
    "miRNA_analysis_part4_corrected.py",
    "rename_files.py"
]

def remove_prohibited_files():
    """Remove any prohibited files from the root directory"""
    removed_files = []
    for filename in PROHIBITED_FILES:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                removed_files.append(filename)
                print(f"Removed: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")
    
    return removed_files

def create_file_guards():
    """Create read-only directories to prevent file creation"""
    for filename in PROHIBITED_FILES:
        if not os.path.exists(filename):
            try:
                # Create a directory with the same name to prevent file creation
                os.makedirs(filename, exist_ok=True)
                # Make it read-only
                os.chmod(filename, 0o444)
                print(f"Created guard directory: {filename}")
            except Exception as e:
                print(f"Error creating guard for {filename}: {e}")

def remove_file_guards():
    """Remove guard directories"""
    for filename in PROHIBITED_FILES:
        if os.path.exists(filename) and os.path.isdir(filename):
            try:
                os.chmod(filename, 0o755)  # Make writable first
                os.rmdir(filename)
                print(f"Removed guard directory: {filename}")
            except Exception as e:
                print(f"Error removing guard for {filename}: {e}")

def main():
    """Main function"""
    print("File Creation Prevention Script")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "guard":
            print("Creating file guards...")
            remove_prohibited_files()
            create_file_guards()
        elif sys.argv[1] == "unguard":
            print("Removing file guards...")
            remove_file_guards()
        elif sys.argv[1] == "clean":
            print("Cleaning prohibited files...")
            removed = remove_prohibited_files()
            if removed:
                print(f"Removed {len(removed)} files")
            else:
                print("No prohibited files found")
        else:
            print("Usage: python prevent_file_creation.py [guard|unguard|clean]")
    else:
        print("Available commands:")
        print("  python prevent_file_creation.py clean   - Remove prohibited files")
        print("  python prevent_file_creation.py guard   - Create file guards")
        print("  python prevent_file_creation.py unguard - Remove file guards")

if __name__ == "__main__":
    main()
