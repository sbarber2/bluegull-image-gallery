"""
Usage:
Run the script from the command line:

python filelists2csv.py file1.txt file2.txt

This will print the merged output as CSV to stdout, allowing you to redirect it to a file if needed:

python filelists2csv.py file1.txt file2.txt > output.csv
"""

import csv
import sys

# Check if correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python merge_files.py <file1> <file2>")
    sys.exit(1)

# Get file names from command-line arguments
file1_path = sys.argv[1]
file2_path = sys.argv[2]

# Read content from both files
with open(file1_path, "r") as f1:
    lines1 = [line.strip() for line in f1.readlines()]

with open(file2_path, "r") as f2:
    lines2 = [line.strip() for line in f2.readlines()]

# Determine the max length to ensure all rows are included
max_length = max(len(lines1), len(lines2))

# Pad shorter list with empty strings
lines1.extend([""] * (max_length - len(lines1)))
lines2.extend([""] * (max_length - len(lines2)))

# Write to stdout
writer = csv.writer(sys.stdout)
writer.writerow(["Column1", "Column2"])  # Header
for col1, col2 in zip(lines1, lines2):
    writer.writerow([col1, col2])
