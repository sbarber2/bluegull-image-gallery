import sys
import os
from PIL import Image, ExifTags

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print(f"Usage: python '{sys.argv[0]}' <input_file> <output_path> <width>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    output_path = sys.argv[2]

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output path '{output_path}'")

    max_width = int(sys.argv[3])

    try:
        with open(input_file, 'r') as infile:
            for line in infile:
                image_path = line.strip()
#                print(image_path)
                if not image_path:
                    continue
                    
                output_file = os.path.join(output_path, os.path.basename(image_path))

                try:
                    with Image.open(image_path) as img:
                        # Handle EXIF orientation (if present)
                        try:
                            exif = img._getexif()
                            if exif:
                                for tag, value in exif.items():
                                    if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == "Orientation":
                                        orientation = value
                                        if orientation == 3:  # Rotate 180°
                                            img = img.rotate(180, expand=True)
                                        elif orientation == 6:  # Rotate 270° (90° clockwise)
                                            img = img.rotate(270, expand=True)
                                        elif orientation == 8:  # Rotate 90° (90° counterclockwise)
                                            img = img.rotate(90, expand=True)
                                        break
                        except AttributeError:
                            print("No EXIF data found for orientation.")

                        width, height = img.size
                        # Check if the image width exceeds the maximum width
                        if width > max_width:
                            # Calculate the new height to maintain aspect ratio
                            new_height = int((max_width / width) * height)
                            img = img.resize((max_width, new_height), Image.LANCZOS)
                            print(f"Resized {image_path} to {max_width}x{new_height} and saved as {output_file}")
                        else:
                            print(f"{image_path} {width}x{height} is within the size limit. No resizing needed.")
                        # Save the resized image to the output directory
                        img.save(output_file)
                except Exception as e:
                    print(f"{os.path.basename(image_path)}: Error - {str(e)}\n")

        print(f"Resizing complete")

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
