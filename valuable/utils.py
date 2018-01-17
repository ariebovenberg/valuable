"""Miscellaneous tools, boilerplate, and shortcuts"""
import typing as t
from collections import Mapping

T = t.TypeVar('T')


class NO_DEFAULT:
    """sentinel for no default"""


def identity(obj):
    """identity function, returns input unmodified"""
    return obj


class compose:
    """compose a function from a chain of functions

    Parameters
    ----------
    *funcs
        callables to compose

    Note
    ----
    * if given no functions, acts as :func:`identity`
    """
    def __init__(self, *funcs: t.Callable):
        self.funcs = funcs

    def __hash__(self):
        return hash(self.funcs)

    def __eq__(self, other):
        if isinstance(other, compose):
            return self.funcs == other.funcs
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, compose):
            return self.funcs != other.funcs
        return NotImplemented

    def __call__(self, *args, **kwargs):
        if not self.funcs:
            return identity(*args, **kwargs)
        *tail, head = self.funcs
        value = head(*args, **kwargs)
        for func in reversed(tail):
            value = func(value)
        return value


class _EmptyMapping(Mapping):
    """an empty mapping to use as a default value"""
    def __iter__(self):
        yield from ()

    def __getitem__(self, key):
        raise KeyError(key)

    def __len__(self):
        return 0

    def __repr__(self):
        return '{}'


EMPTY_MAPPING = _EmptyMapping()
