from bs4 import BeautifulSoup
import re
import requests


class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


class SubjectiveObject(object):
    def __init__(self, target):
        self.target = target


@memoize
def _scrape_results(query):
    r = requests.get('http://www.google.com/search', params={'q': query})
    soup = BeautifulSoup(r.text, 'lxml')
    stats = soup.find('div', {'id': 'resultStats'}).text
    return int(re.sub(r'\D+', '', stats))

