import statistics

__COMMON_WORDS = None


class memoize(dict):
    def __init__(self, target):
        self.target = target

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.target(*key)
        return result


def get_keywords(word_counts, num_keywords=10):
    if not isinstance(word_counts, dict):
        word_counts = word_counts.word_counts

    word_counts = [(pair[1] * cheap_idf(pair[0]), pair[0]) for pair in word_counts.items()]

    counts = [x[0] for x in word_counts]
    mean = statistics.mean(counts)

    word_counts = filter(lambda pair: pair[0] > mean, word_counts)
    word_counts.sort()

    return [pair[1] for pair in word_counts[-num_keywords:]]


def cheap_idf(word):
    if word in __common_words():
        return __common_words().index(word) / float(len(__common_words()))
    return 1.0


def __common_words():
    global __COMMON_WORDS
    if not __COMMON_WORDS:
        with open('subjectivity/words.txt') as lines:
            __COMMON_WORDS = [line.strip() for line in lines]
    return __COMMON_WORDS
