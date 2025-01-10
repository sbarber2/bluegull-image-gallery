import sys
from pathlib import Path
from bs4 import BeautifulSoup

html = ""

# Enure a file path argument is provided
if len(sys.argv) < 2:
    print(f"Usage: python '{sys.argv[0]}' <path_to_html_file>")
    sys.exit(1)

# Get the file path from the first argument
file_path = sys.argv[1]

# Open and read the HTML file into a string
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    
    # Print the HTML content (or use it in further processing)
    # print(html)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"Error: {e}")


soup = BeautifulSoup(html, 'html.parser')

# Using CSS selector
elements = soup.select('img')
for element in elements:
    # print(element)
    href_value = element['src']
    print(Path(href_value).parent)
