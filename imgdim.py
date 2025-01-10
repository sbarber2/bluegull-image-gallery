#
# imgdim.py - create a list of filenames,width,height from all image files in a specified directory
# 

import sys
from pathlib import Path
from PIL import Image, UnidentifiedImageError

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print(f"Usage: python '{sys.argv[0]}' <input_file>")
        sys.exit(1)

    dir = Path(sys.argv[1])

    # Check if the input file exists
    if not dir.is_dir():
        print(f"Error: File '{dir}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Header line: print(f"filename,width,height")

    try:
        for f in dir.iterdir():
            try:
                with Image.open(f) as img:
                    width, height = img.size
                    print(f"{f.name},{width},{height}")
            except UnidentifiedImageError as uiex:
                print(f"{f.name}: not an image file; skipping - {str(uiex)}", file=sys.stderr)
                continue;
            except Exception as ex:
                print(f"{f.name}: Error processing file - {str(ex)}", file=sys.stderr)
    except Exception as e:
        print(f"Error iterating directory: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
