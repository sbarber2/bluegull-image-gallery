#
# imgdim.py - output filename,width,height,exifOrientation for each image 
#             file in a specified directory
# 

import sys
from pathlib import Path
from PIL import Image, UnidentifiedImageError, ExifTags

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print(f"Usage: python '{sys.argv[0]}' <input_file>")
        sys.exit(1)

    image_dir = Path(sys.argv[1])

    # Check if the input file exists
    if not image_dir.is_dir():
        print(f"Error: File '{image_dir}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    exifOrientation = 0
    # Header line: print(f"filename,width,height")
    for thisKey in ExifTags.TAGS.keys():
        if ExifTags.TAGS[thisKey]=='Orientation':
            exifOrientation = thisKey
            break
    try:
        for f in image_dir.iterdir():
            try:
                with Image.open(f) as img:
                    width, height = img.size
                    exif = img.getexif()
                    orientation = exif.get(exifOrientation, 1)
                    print(f"{f.name},{width},{height},{orientation}")
            except UnidentifiedImageError as uiex:
                print(f"{f.name}: not an image file; skipping - {str(uiex)}", file=sys.stderr)
                continue
            except Exception as ex:
                print(f"{f.name}: Error processing file - {str(ex)}", file=sys.stderr)
    except Exception as e:
        print(f"Error iterating directory: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
