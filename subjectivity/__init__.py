import bodybuilder
from util import memoize


def s(name):
    return Subjective(name, name)


def objective(o):
    if isinstance(o, Subjective):
        return o.target
    return o


class Subjective(object):
    def __init__(self, target, name=None):
        if not name:
            try:
                name = target.__name__
            except:
                name = target.__class__.__name__
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

    def __str__(self):
        return str(self.target)

    def __repr__(self):
        return repr(self.target)

    def __getitem__(self, index):
        return Subjective(self.target[index])

    def __getslice__(self, i, j):
        return Subjective(self.target[i:j])

    def __basis__(self):
        return get_term_basis(self.name)

    def __score__(self):
        return self.__basis__().score

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


def similarity(a, b):
    a = _get_as_basis(a).blob
    b = _get_as_basis(b).blob

    intersect = set(a.words) & set(b.words)
    union = set(a.words) | set(b.words)

    intersect = sum(a.word_counts[x] + b.word_counts[x] for x in intersect)
    union = sum(a.word_counts[x] + b.word_counts[x] for x in union)

    return float(intersect) / float(union)


def _get_as_basis(term):
    if isinstance(term, bodybuilder.TermBasis):
        return term
    return get_term_basis(term)


@memoize
def get_term_basis(term):
    return bodybuilder.TermBasis(term)
