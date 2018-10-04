
from bs4 import BeautifulSoup


raw_html = open('1.html').read()
html = BeautifulSoup(raw_html, 'html.parser')

for p in html.select('p'):
    if p['id'] == 'walrus':
        print(p.text)

print(html.select('p'))
