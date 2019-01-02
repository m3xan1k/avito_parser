#!/usr/bin/env python3

import json
import requests
import avito_parser as ap

def read_token(filename):
    with open(filename, 'r') as f:
        bot_settings = json.load(f)
        token = bot_settings['token']
        chat_id = bot_settings['chat_id']
    return token, chat_id

token, chat_id = read_token('bot_settings.json')
url = 'https://api.telegram.org/bot{0}/'.format(token)


def make_request(method):
    r = requests.get(url + method)
    return r.text

def get_updates():
    updates = make_request('getUpdates')
    return updates

def format_text():
    cards = ap.get_top_ten(ap.sort_by_date(ap.read_pages()))
    formatted_text = ''
    for card in cards:
        text = '*****', '<b>' + card['header'] + '</b>', 'Цена: ' + str(card['price']), 'Локация: ' + card['place'], str(card['date']) + ' дня назад', '<a href="' + card['link'] + '">Ссылка</a>' + '\n'
        advert = '\n'.join(text)
        formatted_text += advert
    return formatted_text

def send_message():
    text = format_text()
    query_string = 'sendMessage?chat_id={0}&text={1}&parse_mode=HTML'.format(chat_id, str(text))
    print(query_string)
    make_request(query_string)

def main():
    send_message()
    # format_text()

main()
