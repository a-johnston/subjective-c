import bodybuilder
from textblob import TextBlob


class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def objective(o):
    if isinstance(o, Subjective):
        return o.target
    return o


class Subjective(object):
    def __init__(self, name, target):
        self.__dict__ = {
            'name': name,
            'target': target,
        }

    def __call__(self, *args, **kwargs):
        return Subjective(self.target(*args, **kwargs))

    def __getattr__(self, name):
        return Subjective(getattr(self.target, name))

    def __setattr__(self, name, value):
        if not self.__dict__ or name in self.__dict__:
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self.target, name, value)

    def __int__(self):
        return int(self.target)

    def __str__(self):
        return str(self.target)

    def __repr__(self):
        return repr(self.target)

    def __blob__(self):
        return get_basis_blob(self.name)

    def __score__(self):
        blob = self.__blob__()
        return blob.polarity / blob.subjectivity

    def __eq__(self, other):
        if isinstance(other, Subjective):
            return (abs(self.__score__() - other.__score__()) < 0.005)
        return self.target == other

    def __gt__(self, other):
        if isinstance(other, Subjective):
            return self.__score__() > other.__score__()
        return self.target > other

    def __lt__(self, other):
        if isinstance(other, Subjective):
            return self.__score__() < other.__score__()
        return self.target < other

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __hash__(self):
        return self.target.__hash__()


def similarity(a, b):
    a = _get_as_blob(a)
    b = _get_as_blob(b)

    intersection = sum(map(a.word_counts[x] + b.word_counts[x] for x in (set(a.words) & set(b.words))))
    union = sum(map(a.word_counts[x] + b.word_counts[x] for x in (set(a.words) | set(b.words))))

    return float(intersection) / float(union)


def _get_as_blob(term):
    if isinstance(term, TextBlob):
        return term
    return get_basis_blob(term)


@memoize
def get_basis_blob(term):
    return bodybuilder.build_basis(term)
