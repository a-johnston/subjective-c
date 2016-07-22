from bs4 import BeautifulSoup
from google import search
import re
import requests
from textblob import TextBlob
from textblob import Word


def sane_english(text):
    text = text.strip().lower()

    if len(text) == 0:
        return None

    sane = re.sub(r'[^a-z ]', '', text)
    sane = re.sub(r'[ ]{2,}', ' ', sane).strip()

    if float(len(sane)) / float(len(text)) < 0.85:
        return None

    good = []
    for word in sane.split(' '):
        if Word(word).define():
            good.append(word)

    if float(len(good)) / len(sane.split(' ')) < 0.5:
        return None

    return ' '.join(good)


def get_top_blocks(url):
    try:
        blocks = BeautifulSoup(requests.get(url).text, 'lxml')
        blocks = blocks.get_text().split('\n')
        blocks = filter(
            lambda x: x,
            map(lambda x: sane_english(x), blocks)
        )

        top_blocks = sorted(zip(map(lambda x: len(x), blocks), blocks))
        top_blocks = map(lambda x: x[1], top_blocks[-len(top_blocks)/10:])

        return reduce(lambda a, b: a + b, top_blocks, '')
    except:
        return ''


def build_basis(term):
    urls = list(search('wiki ' + term, stop=10))
    return TextBlob(' '.join([get_top_blocks(url) for url in urls]).strip())
