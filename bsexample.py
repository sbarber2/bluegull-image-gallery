from bs4 import BeautifulSoup

html = """<html><body><a href="http://example.com" class="my-link">Click Here</a></body></html>"""
soup = BeautifulSoup(html, 'html.parser')

# Using CSS selector
element = soup.select_one('a.my-link')
href_value = element['href']
print(href_value)