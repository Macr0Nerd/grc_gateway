"""Serialization."""

import logging
from collections.abc import Iterable, Mapping
from typing import (
    Protocol,
    SupportsFloat,
    SupportsInt,
    Union,
    runtime_checkable,
)

from grc.plugins.logging import TemplateStringAdapter

logger = TemplateStringAdapter(logging.getLogger(__name__))


@runtime_checkable
class ObjectSerializable(Protocol):
    """Object Serialization protocol."""

    __serializable_attributes__: Iterable[str]


@runtime_checkable
class SupportsStr(Protocol):
    """Protocol to check if an object supports __str__."""

    def __str__(self) -> str:
        """Ensure that __str__ is implemented."""
        return ''


_SerializablePrimitives = Union[
    bool, None, SupportsFloat, SupportsInt, SupportsStr
]
_SerializableObjects = Union[
    Iterable[_SerializablePrimitives],
    Mapping[SupportsStr, _SerializablePrimitives],
    ObjectSerializable,
]
Serializable = Union[
    _SerializablePrimitives,
    _SerializableObjects,
    Iterable[_SerializableObjects],
    Mapping[SupportsStr, _SerializableObjects],
]
"""Defines what types are serializable."""

_IsSerializedPrimitives = Union[bool, float, int, str, None]
_IsSerializedObjects = Union[
    dict[str, _IsSerializedPrimitives], list[_IsSerializedPrimitives]
]
IsSerialized = Union[
    _IsSerializedPrimitives,
    _IsSerializedObjects,
    dict[str, _IsSerializedObjects],
    list[_IsSerializedObjects],
]
"""If an object is already a serialized type."""
