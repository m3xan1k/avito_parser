#!/usr/bin/env python3

import json
import requests
import avito_parser as ap
import time

# this function reads bot settings like ali token and chat id from json file
def read_token(filename):
    with open(filename, 'r') as f:
        bot_settings = json.load(f)
        token = bot_settings['token']
        chat_id = bot_settings['chat_id']
    return token, chat_id

# save settings to variables
token, chat_id = read_token('bot_settings.json')
# construct url to make request to tg api
url = 'https://api.telegram.org/bot{0}/'.format(token)

# make http request with url + method
def make_request(method):
    r = requests.get(url + method)
    return r.text

# this can check updates
def get_updates():
    updates = make_request('getUpdates')
    return updates

# send photo api method
def send_photo(photo):
    query_string = 'sendPhoto?chat_id={0}&photo={1}&parse_mode=HTML&disable_notification=true'.format(chat_id, photo)
    make_request(query_string)

# send message api method
def send_message(formatted_text):
    query_string = 'sendMessage?chat_id={0}&text={1}&parse_mode=HTML&disable_notification=true'.format(chat_id, str(formatted_text))
    make_request(query_string)

# format and send message and photo
def format_and_send():
    # call parser to grab data
    cards = ap.get_top_ten(ap.sort_by_date(ap.read_pages()))
    for card in cards:
        # construct and format text
        text = '*****', '<b>' + card['header'] + '</b>', 'Цена: ' + str(card['price']), 'Локация: ' + card['place'], str(card['date']) + ' дня назад', '<a href="' + card['link'] + '">Ссылка</a>' + '\n'

        formatted_text = '\n'.join(text)
        # variable to save foto src url
        photo = card['photo']
        # send all together
        send_message(formatted_text)
        time.sleep(1)
        send_photo(photo)
        time.sleep(2)




def main():
    format_and_send()

main()
