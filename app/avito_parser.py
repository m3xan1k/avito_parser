#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import lxml
import os.path
import time
import re
from operator import itemgetter
import json

# main url
url = 'https://avito.ru/'

# some http params
user_agent = {'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

# settings to complete http query
settings = {
    'city': 'moskva',
    'query': 'бультерьер'
}


# constructing query-string with all setting
def construct_query(url, settings, page):
    full_query = '{0}{1}?p={2}&q={3}'.format(url, settings['city'], page, settings['query'])
    return full_query

# making an http request
def get_html(full_query):
    r = requests.get(full_query, params=user_agent)
    html = r.text
    return html

# getting first page soup with count_pages we will know how long pagination is
def get_first_page_soup():
    full_query = construct_query(url, settings, page=1)
    html = get_html(full_query)
    soup = BeautifulSoup(html, 'lxml')
    return soup

# getting any page soup
def get_any_page_soup(page):
    full_query = construct_query(url, settings, page)
    html = get_html(full_query)
    soup = BeautifulSoup(html, 'lxml')
    return soup

# count how long pagination is
def count_pages():
    full_query = construct_query(url, settings, page=1)
    html = get_html(full_query)
    soup = BeautifulSoup(html, 'lxml')
    pagination_last_child_href = soup.find_all('a', class_='pagination-page')[-1]['href']
    p = re.findall(r'p=\d+', pagination_last_child_href)[0]
    pages = re.findall(r'\d+', p)[0]
    return pages

# parsing тeeded description of items
def get_item_description(soup, id=1):

    # all description can be found in one div
    item_cards = soup.find_all('div', class_='description item_table-description')

    # make empty array to collect item descriptions
    all_bullys = []

    # loop through items to collect data
    for card in item_cards:
        item = {}

        header = card.find_all('span', itemprop="name")
        price = card.find_all('span', class_="price")
        place = card.find_all('div', class_="data")
        date = card.find_all('div', class_="js-item-date c-2")
        link = card.find_all('a', class_="item-description-title-link")

        item["id"] = id
        item["header"] = header[0].get_text()
        item["price"] = price[0].get_text().replace('₽', '').replace(' ', '').strip()
        try:
            item["place"] = place[0].select("p:nth-of-type(2)")[0].get_text().replace(u'\xa0', u' ')
        except:
            item["place"] = "Местонахождение не указано"
        # filter on date. some custom logic =)
        item["date"] = date[0].get_text().strip()
        h = ['час', 'часа', 'часов']
        d = ['день', 'дней', 'дня']
        w = ['неделя', 'недели', 'недель', 'неделю']
        if any(x in item['date'] for x in h):
            item['date'] = 0
        elif any(x in item['date'] for x in d):
            multiplier = 1
            days = int(item['date'][0]) * multiplier
            item['date'] = days
        elif any(x in item['date'] for x in w):
            multiplier = 7
            days = int(item['date'][0]) * multiplier
            item['date'] = days
        else:
            item['date'] = 30

        item["link"] = 'https://avito.ru' + link[0]['href']

        # filter items by price
        statements = ['Ценанеуказана', 'Бесплатно', 'Договорная']
        if item['price'] not in statements:
            if (10000 <= int(item['price']) <= 25000):
                all_bullys.append(item)
                id += 1
        # returning id for fix starting new count in pagination loop
    return all_bullys, id



def read_pages():
    # counting pages with count_pages()
    pages = int(count_pages()) + 1
    # generate counter
    page_counter = [i for i in range(pages) if i > 0]
    id = 1
    # list of all cards
    all_cards = []
    for page in page_counter:
        # simply getting soup on every page
        soup = get_any_page_soup(page)
        # getting list of items with data and new_id for start new page with count of 51
        item_cards, new_id = get_item_description(soup, id)
        id += new_id
        all_cards.append(item_cards)
        time.sleep(3)
    # getting flat list
    all_cards_flat = []
    for page in all_cards:
        for card in page:
            all_cards_flat.append(card)
    return all_cards_flat

def sort_by_date(all_cards_flat):
    # create sorted array of dictionaries
    sorted_cards = sorted(all_cards_flat, key=lambda k: int(k['date']))
    return sorted_cards

def get_top_ten(sorted_cards):
    top_ten = sorted_cards[0:10]
    return top_ten

def write_html(html):
    if os.path.exists('bully.html'):
        with open('bully.html', 'a') as f:
            f.write(html)
    else:
        with open('bully.html', 'w') as f:
            f.write(html)


#def main():
    # write_html(get_first_page())
    # get_top_ten(sort_by_date(read_pages()))
    # read_pages()
    # get_item_description(get_first_page_soup())

#main()
