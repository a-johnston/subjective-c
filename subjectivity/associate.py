from bs4 import BeautifulSoup
from google import search
from operator import itemgetter
import re
import requests
import statistics

_SEARCH_LIMIT = 10
_LOW_Z = 1
_HIGH_Z = 2


def _find_cutoffs(counts, low_z=_LOW_Z, high_z=_HIGH_Z):
    mean = statistics.mean(counts)
    stdev = statistics.pstdev(counts)

    low = low_z * stdev + mean
    high = high_z * stdev + mean

    return low, high

def _graph_related(term, stop=_SEARCH_LIMIT, cross_check=True):
    results = search(term)
    word_sums = {}

    print('term {}'.format(term))
    for url in results:
        if not stop:
            break
        stop -= 1

        print('\ttrying {}'.format(url))
        text = BeautifulSoup(requests.get(url).text, 'lxml').get_text().lower()
        text_blocks = re.split(r'\s+', text)
        words = [word for word in text_blocks if re.match(r'[a-z]+$', word)]
   
        if len(words) == 0:
            print(text_blocks)
            return []

        for word in words:
            if word in word_sums:
                word_sums[word] += 1
            else:
                word_sums[word] = 1

    low, high = _find_cutoffs(word_sums.values())

    good_words = [pair[0] for pair in word_sums.items() if low < pair[1] < high]

    if cross_check:
        good_words = [word for word in good_words if term in _graph_related(word, stop=stop, cross_check=False)]

    print(good_words)

