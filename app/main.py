#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import lxml
import os.path
import time
import re

url = 'https://avito.ru/'
user_agent = {'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
settings = {
    'city': 'moskva',
    'query': 'бультерьер'
}

pages = [i for i in range(6) if i > 0]

def construct_query(url, settings, page):
    full_query = '{0}{1}?p={2}&q={3}'.format(url, settings['city'], page, settings['query'])
    return full_query

def get_html(full_query):
    r = requests.get(full_query, params=user_agent)
    html = r.text
    return html

def count_pages():
    full_query = construct_query(url, settings, page=1)
    html = get_html(full_query)
    soup = BeautifulSoup(html, 'lxml')
    pagination_last_child_href = soup.find_all('a', class_='pagination-page')[-1]['href']
    p = re.findall(r'p=\d+', pagination_last_child_href)[0]
    pages = re.findall(r'\d+', p)[0]
    return pages

def read_pages():
    pages = int(count_pages()) + 1
    page_counter = [i for i in range(pages) if i > 0]
    for page in page_counter:
        full_query = construct_query(url, settings, page)
        print(full_query)
        html = get_html(full_query)
        if os.path.exists('bully.html'):
            with open('bully.html', 'a') as f:
                f.write(html)
        else:
            with open('bully.html', 'w') as f:
                f.write(html)
        time.sleep(3)






# r = requests.get(full_query)
# html = r.text
#
# soup = BeautifulSoup(r.text, 'lxml')
#
# print(soup)

# with open('output.txt', 'w') as f:
#     f.write(r.text)


def main():
    read_pages()

main()
