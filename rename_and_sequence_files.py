"""
Rename and Sequence Files Script

This script reads an input file where each line contains the name of a file in the current directory.
It renames each file according to these rules:
- The new name starts with a four-digit, zero-padded sequence number corresponding to the line number in the input file.
- The sequence number is followed by a hyphen.
- Spaces in the original filename are replaced with hyphens.

Usage:
    python rename_and_sequence_files.py [-v | --verbose] <input_file>

Arguments:
    -v, --verbose  Enable verbose output (optional, may appear in any position).
    <input_file>    A text file containing one filename per line.

Example:
    python rename_and_sequence_files.py --verbose filenames.txt
"""

import os
import sys

def rename_files(input_file, verbose):
    """
    Reads an input file containing filenames and renames each file by prefixing it with a 
    four-digit, zero-padded sequence number followed by a hyphen. Spaces in filenames are 
    replaced with hyphens. 

    Parameters:
        input_file (str): The path to the input text file containing filenames.
        verbose (bool): If True, prints informational messages during execution.

    Raises:
        Exception: Captures and prints any errors encountered during file operations.
    """
    try:
        with open(input_file, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        for index, original_name in enumerate(lines, start=1):
            if os.path.exists(original_name):
                # Create the new filename
                sequence_number = f"{index:04d}"  # Four-digit, zero-padded
                sanitized_name = original_name.replace(" ", "-")
                new_name = f"{sequence_number}-{sanitized_name}"
                
                # Rename the file
                os.rename(original_name, new_name)
                if verbose:
                    print(f"Renamed '{original_name}' to '{new_name}'")
            else:
                print(f"Warning: File '{original_name}' not found, skipping.", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    verbose_flag = False
    input_file = None
    
    for arg in sys.argv[1:]:
        if arg in ("-v", "--verbose"):
            verbose_flag = True
        else:
            input_file = arg
    
    if not input_file:
        print(f"Usage: {sys.argv[0]} [-v | --verbose] <input_file>", file=sys.stderr)
        sys.exit(1)
    
    rename_files(input_file, verbose_flag)
