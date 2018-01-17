import typing as t
from datetime import datetime

import pytest

from valuable import load
from valuable.utils import identity


@pytest.fixture
def registry():
    return load.PrimitiveRegistry({
        int:        int,
        float:      float,
        bool:       {'true': True, 'false': False}.__getitem__,
        str:        str,
        type(None): identity,
        object:     identity,
        datetime:   load.parse_iso8601,
    }) | load.GenericRegistry({
        t.List:  load.list_loader,
        t.Set:   load.set_loader,
    }) | load.get_optional_loader
