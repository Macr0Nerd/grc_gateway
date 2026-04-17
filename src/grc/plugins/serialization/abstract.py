"""Serialization."""

import logging
from abc import abstractmethod
from collections.abc import Iterable, Mapping
from types import NoneType
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


Serializable = Union[
    bool,
    Iterable['Serializable'],
    Mapping[SupportsStr, 'Serializable'],
    NoneType,
    ObjectSerializable,
    SupportsFloat,
    SupportsInt,
    SupportsStr,
]
"""Defines what types are serializable."""


IsSerialized = Union[
    bool, dict[str, 'IsSerialized'], float, int, list, NoneType, str
]
"""If an object is already a serialized type."""
