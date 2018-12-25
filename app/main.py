#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://avito.ru/'
params = {
    'city': 'moskva',
    'query': 'бультерьер'
}

full_query = url + params['city'] + '?q=' + params['query']

r = requests.get(full_query)
html = r.text

soup = BeautifulSoup(r.text, 'lxml')

print(soup)

# with open('output.txt', 'w') as f:
#     f.write(r.text)
