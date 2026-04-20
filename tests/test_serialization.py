"""Serialization tests."""

import asyncio
import datetime
from dataclasses import dataclass

import pytest

from grc.plugins.serialization.abstract import IsSerialized, Serializable
from grc.plugins.serialization.io import serialize


@dataclass
class SerializableObject:
    """Serializable object for testing.

    Attributes:
        a (bool)
        b (tuple[int, float])
        c (list[str])
        d (datetime.datetime)
        f (dict[str, SerializableObject], optional)
    """

    __serializable_attributes__ = ('a', 'b', 'c', 'd', 'e')

    a: bool
    b: tuple[int, float]
    c: list[str]
    d: datetime.datetime
    e: dict[str, SerializableObject] | None


so_1 = SerializableObject(
    a=False,
    b=(-1, 2.0),
    c=['Hello', 'World!'],
    d=datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.UTC),
    e=None,
)

ex_1 = {
    'a': False,
    'b': [-1, 2.0],
    'c': ['Hello', 'World!'],
    'd': '2000-01-01 00:00:00+00:00',
    'e': None,
}

so_2 = SerializableObject(
    a=True,
    b=(8192, 3.141592),
    c=['adsigb', 'yuwbnefom', '   ', 'weigvvo'],
    d=datetime.datetime(2000, 12, 12, 23, 59, 59, tzinfo=datetime.UTC),
    e={'so_1': so_1},
)

ex_2 = {
    'a': True,
    'b': [8192, 3.141592],
    'c': ['adsigb', 'yuwbnefom', '   ', 'weigvvo'],
    'd': '2000-12-12 23:59:59+00:00',
    'e': {'so_1': ex_1},
}


@pytest.mark.parametrize('so', [so_1, so_2])
def test_abstract(so: SerializableObject) -> None:
    """Test serialization abstracts.

    Args:
        so: Serializable object for testing.
    """
    assert issubclass(SerializableObject, Serializable)
    assert isinstance(so_1, Serializable)


@pytest.mark.parametrize('so, ex', [(so_1, ex_1), (so_2, ex_2)])
def test_serialize(so: SerializableObject, ex: dict[str, IsSerialized]) -> None:
    """Test serialization functionality.

    Args:
        so: Serializable object for testing.
        ex: Expected serialized output.
    """
    assert asyncio.run(serialize(so)) == ex
