# imgdimss3.py - create a list of filenames and dimensions from image files in the current directory
# this is a special case of wanting to only use the images that were already in a SmartSlider3 (SS3)
# slider, so an input file that has a list of the desired images is used to control which files to
# examine (created by imglist.py). These filenames are in the form that SS3 generates, which are not
# the names of the files that were uploaded to WordPress's media library originally, and thus there
# is imperfect code to back-convert the filenames based on the empirically observed transformations.

import sys
import os
from PIL import Image

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print(f"Usage: python '{sys.argv[0]}' <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    output_file = "image_dimensions_output.txt"

    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                image_path = line.strip()
#                print(image_path)
                if not image_path:
                    continue

                # special case: no way to back convert this as a general pattern
                if (image_path == 'Legends-of-Jazz-at-the-Cove-021-Copy.jpg'):
                    image_path = 'Legends of Jazz at the Cove 021 - Copy.JPG'
                else:
                    image_path = image_path.replace('-', ' ')
                    image_path = image_path.replace(' scaled', '')

                try:
                    with Image.open(image_path) as img:
                        width, height = img.size
                        outfile.write(f"{os.path.basename(image_path)},{width},{height}\n")
                except Exception as e:
                    outfile.write(f"{os.path.basename(image_path)}: Error - {str(e)}\n")

        print(f"Output written to '{output_file}'")

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
