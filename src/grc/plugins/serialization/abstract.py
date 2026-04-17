"""Serialization."""

import logging
from abc import abstractmethod
from typing import (
    Mapping,
    Protocol,
    Sequence,
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

    @abstractmethod
    def __serialize__(self) -> dict:
        """Serialize a network object to a dictionary."""
        raise NotImplementedError()


@runtime_checkable
class SupportsStr(Protocol):
    """Protocol to check if an object supports __str__."""

    def __str__(self) -> str:
        """Ensure that __str__ is implemented."""
        return ''


SerializablePrimitives = Union[
    bool, None, SupportsFloat, SupportsInt, SupportsStr
]
SerializableObjects = Union[
    Sequence[SerializablePrimitives],
    Mapping[SupportsStr, SerializablePrimitives],
    ObjectSerializable,
]
Serializable = Union[
    SerializablePrimitives,
    SerializableObjects,
    Sequence[SerializableObjects],
    Mapping[SupportsStr, SerializableObjects],
]
"""Defines what types are serializable."""

IsSerializedPrimitives = Union[bool, float, int, str, None]
IsSerializedObjects = Union[
    dict[str, IsSerializedPrimitives], list[IsSerializedPrimitives]
]
IsSerialized = Union[
    IsSerializedPrimitives,
    IsSerializedObjects,
    dict[str, IsSerializedObjects],
    list[IsSerializedObjects],
]
"""If an object is already a serialized type."""
