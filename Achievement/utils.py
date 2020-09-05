import requests
import numpy as np
from PIL import Image
from random import choice
from bs4 import BeautifulSoup


# Pasting image on image #
def alpha_composite(src, dst):
    """
    Return the alpha composite of src and dst.

    Parameters:
    src -- PIL RGBA Image object
    dst -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing
    """

    # http://stackoverflow.com/a/3375291/190597
    # http://stackoverflow.com/a/9166671/190597
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype='float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid='ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)
    out[alpha] *= 255
    np.clip(out, 0, 255)
    # astype('uint8') maps np.nan (and np.inf) to 0
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out
# ---------- #


# Searching icons #
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
def get_google(text, search_all=False, return_all=False):
    url = "https://www.google.ru/search?tbm=isch&tbs=iar:s&as_q=" + text
    if search_all:
        url = "https://www.google.ru/search?tbm=isch&as_q=" + text

    req = requests.get(url)
    if req.status_code != 200:
        return None

    soup = BeautifulSoup(req.text, features="html.parser")
    images = soup.findAll("img", {"class": "t0fcAb"})

    if len(images) > 0:
        if not return_all:
            return choice(images)['src']
        urls = []
        for img in images:
            urls.append(img['src'])
        return urls
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
# ---------- #
