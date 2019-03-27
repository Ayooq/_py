from re import search
from os import curdir, sep, extsep

from json import dump
from requests import get, post
from api import bot_api


def set_webhook(link):
    url = bot_api + 'setwebhook?url={}'.format(link)
    response = get(url)
    print(response.text)
    return response.json


def delete_webhook(link):
    url = bot_api + 'deletewebhook?url={}'.format(link)
    response = get(url)
    print(response.text)
    return response.json


def write_json(data, filename='answer' + extsep + 'json'):
    with open(
        '{dir}{sep}{name}'.format(dir=curdir, sep=sep, name=filename), 'w'
    ) as file:
        dump(data, file, indent=2, sort_keys=True, ensure_ascii=False)


def send_message(chat_id, text='Unknown command.'):
    url = bot_api + 'sendmessage'
    answer = {'chat_id': chat_id, 'text': text}
    response = post(url, json=answer)
    write_json(response.json())
    return response.json()


def parse_text(string):
    pattern = r'/\w+'
    currency = search(pattern, string)
    if currency:
        return currency.group()


def get_price(currency):
    """
    Записать полученные данные о криптовалюте в JSON файл. Отобразить текущий курс в долларовом эквиваленте.
    """
    url = 'https://api.coinmarketcap.com/v1/ticker{}'.format(currency)
    response = get(url)
    write_json(response.json(), filename='price' + extsep + 'json')
    try:
        price = response.json()[-1]['price_usd']
        return price
    except KeyError:
        return 'Некорректное название криптовалюты.'
