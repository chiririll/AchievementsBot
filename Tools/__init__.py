from io import BytesIO
from random import choice

import requests
from bs4 import BeautifulSoup


def search_image(text, search_all=False):
    url = f"https://www.google.ru/search?tbm=isch{'&tbs=iar:s' if search_all else ''}&as_q={text}"

    req = requests.get(url)
    if req.status_code != 200:
        return None

    soup = BeautifulSoup(req.text, features="html.parser")
    images = soup.findAll("img")[1:]

    if len(images) > 0:
        return download_image(choice(images)['src'])
    return None


def download_image(url):
    return BytesIO(requests.get(url).content)
