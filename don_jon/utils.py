import random
from collections import OrderedDict
import os

ugettext_lazy = lambda s: s

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
def get_asset(name):
    return os.path.join(ASSETS_DIR, name)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class NameObject(object):

    @classmethod
    def clsname(cls):
        if isinstance(cls, type):
            return cls.__name__.lower()
        # was called with an instance instead of  class
        return cls.__class__.__name__.lower()


class AttrOrderedDict(OrderedDict):
    pass


class D:

    def __init__(self, r):
        self.range = r
        self.value = random.randrange(1, r+1)

    
    def __mul__(self, other):

        total = self.value
        i = 1
        while i < other:
            total += self.__class__(self.range).value
            i += 1
        return total
    def __rmul__(self, other):
        return self.__mul__(other)

    def __int__(self):
        return self.value

from registries import routes
from routing import NoReverseMatch

def reverse(name, **kwargs):
    """
    Try to find a view registered under the given name, and pass it kwargs
    """
    r = routes.get(name, None)
    if r is None:
        raise NoReverseMatch("No route found for name '{0}'".format(name))
    return r.view(**kwargs).process()

from vendor.molecular import molecular
def random_name(name_file="general"):
    """return a random name"""
    m = molecular.Molecule()
    m.load(name_file+".nam")
    return m.name()