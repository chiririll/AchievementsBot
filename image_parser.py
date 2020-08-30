from random import choice
import requests
from bs4 import BeautifulSoup


def get_size(meta_text):
    number = ""
    for symb in meta_text:
        if symb == '×':
            break
        else:
            number += symb
    try:
        return int(number)
    except ValueError:
        return 0


# Google
def get_google(text):
    url = "https://www.google.ru/search?tbm=isch&tbs=iar:s&as_q=" + text
    req = requests.get(url)
    if req.status_code != 200:
        return None

    soup = BeautifulSoup(req.text, features="html.parser")
    images = soup.findAll("img", {"class": "t0fcAb"})

    if len(images) > 0:
        return choice(images)['src']
    return None


# Yandex
def get_yandex(text):
    url = "https://yandex.ru/images/search?iorient=square&text=" + text
    req = requests.get(url)
    if req.status_code != 200:
        return None

    soup = BeautifulSoup(req.text, features="html.parser")

    images = soup.findAll("img", {"class": "serp-item__thumb justifier__thumb"})

    if len(images) > 0:
        return choice(images)['src']
    return None
