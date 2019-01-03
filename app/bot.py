#!/usr/bin/env python3

import json
import requests
import avito_parser as ap
import time

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

def send_photo(photo):
    query_string = 'sendPhoto?chat_id={0}&photo={1}&parse_mode=HTML&disable_notification=true'.format(chat_id, photo)
    make_request(query_string)

def send_message(formatted_text):
    query_string = 'sendMessage?chat_id={0}&text={1}&parse_mode=HTML&disable_notification=true'.format(chat_id, str(formatted_text))
    make_request(query_string)

def format_and_send():
    cards = ap.get_top_ten(ap.sort_by_date(ap.read_pages()))
    for card in cards:
        text = '*****', '<b>' + card['header'] + '</b>', 'Цена: ' + str(card['price']), 'Локация: ' + card['place'], str(card['date']) + ' дня назад', '<a href="' + card['link'] + '">Ссылка</a>' + '\n'

        formatted_text = '\n'.join(text)
        photo = card['photo']

        send_message(formatted_text)
        time.sleep(1)
        send_photo(photo)
        time.sleep(2)




def main():
    # send_message()
    format_and_send()
    # send_photo('63.img.avito.st/208x156/5053176863.jpg')

main()
