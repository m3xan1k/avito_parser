#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import lxml
import os.path

url = 'https://avito.ru/'
params = {
    'city': 'moskva',
    'query': 'бультерьер'
}

pages = [i for i in range(6) if i > 0]

def construct_query(url, page, params):
    full_query = '{0}{1}?p={2}q={3}'.format(url, params['city'], page, params['query'])
    return full_query

def get_html(full_query):
    r = requests.get(full_query)
    html = r.text
    return html

def read_pages(pages):
    for page in pages:
        full_query = construct_query(url, page, params)
        html = get_html(full_query)
        if os.path.exists('bully.html'):
            with open('bully.html', 'a') as f:
                f.write(html)
        else:
            with open('bully.html', 'w') as f:
                f.write(html)





# r = requests.get(full_query)
# html = r.text
#
# soup = BeautifulSoup(r.text, 'lxml')
#
# print(soup)

# with open('output.txt', 'w') as f:
#     f.write(r.text)


def main():
    read_pages(pages)

main()
