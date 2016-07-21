from bs4 import BeautifulSoup
import re
import requests

_common_attr = set(dir(type)) | set(['__self__', '__objclass__'])
_subjective_map = lambda x: x if isinstance(x, Subjective) else Subjective(x)


class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


class Subjective(object):
    def __init__(self, target):
        self.target = target

        valid_attrs = set(dir(target)) - _common_attr

        if '__name__'

        for attr in (set(dir(target)) - _common_attr - set([target.__name__])):
            print('subjective {} {}'.format(target, attr))
            setattr(self, attr, _subjective_map(getattr(target, attr)))

    def __call__(self, *args, **kwargs):
        self.target(
            map(_subjective_map, args),
            zip(kwargs.keys(), map(_subjective_map, kwargs.values()))
        )

@memoize
def _scrape_results(query):
    r = requests.get('http://www.google.com/search', params={'q': query})
    soup = BeautifulSoup(r.text, 'lxml')
    stats = soup.find('div', {'id': 'resultStats'}).text
    return int(re.sub(r'\D+', '', stats))

