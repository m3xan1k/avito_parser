#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

main_url = 'https://avito.ru'

r = requests.get(main_url)

with open('output.txt', 'w') as f:
    f.write(r.text)
