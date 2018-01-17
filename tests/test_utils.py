import collections

import pytest

from valuable import utils


def test_identity():
    obj = object()
    assert utils.identity(obj) is obj


class TestCompose:

    def test_empty(self):
        obj = object()
        func = utils.compose()
        assert func(obj) is obj
        assert isinstance(func.funcs, tuple)
        assert func.funcs == ()

    def test_one_func_with_multiple_args(self):
        func = utils.compose(int)
        assert func('10', base=5) == 5
        assert isinstance(func.funcs, tuple)
        assert func.funcs == (int, )

    def test_multiple_funcs(self):
        func = utils.compose(str, lambda x: x + 1, int)
        assert isinstance(func.funcs, tuple)
        assert func('30', base=5) == '16'

    def test_equality(self):
        func = utils.compose(int, str)
        other = utils.compose(int, str)
        assert func == other
        assert not func != other
        assert hash(func) == hash(other)

        assert not func == utils.compose(int)
        assert func != utils.compose(int)

        assert func != object()
        assert not func == object()


def test_empty_mapping():
    assert isinstance(utils.EMPTY_MAPPING, collections.Mapping)
    assert utils.EMPTY_MAPPING == {}
    with pytest.raises(KeyError):
        utils.EMPTY_MAPPING['foo']

    assert len(utils.EMPTY_MAPPING) == 0
    assert list(utils.EMPTY_MAPPING) == []
    assert repr(utils.EMPTY_MAPPING) == '{}'
