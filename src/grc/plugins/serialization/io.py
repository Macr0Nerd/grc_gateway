"""Serialization I/O Module."""

import asyncio
import logging
from collections.abc import Awaitable, Iterable, Mapping
from types import NoneType
from typing import Any, SupportsFloat, SupportsInt, overload

from grc.plugins.logging import TemplateStringAdapter
from grc.plugins.serialization.abstract import (
    IsSerialized,
    ObjectSerializable,
    Serializable,
    SupportsStr,
)

logger = TemplateStringAdapter(logging.getLogger(__name__))


@overload
async def serialize(obj: bool) -> bool:
    return obj


@overload
async def serialize(obj: Iterable[Serializable]) -> list[IsSerialized]:
    return await asyncio.gather(*[serialize(x) for x in obj])


@overload
async def serialize(
    obj: Mapping[SupportsStr, Serializable],
) -> dict[str, IsSerialized]:
    out = {}

    async def add_map_pair(key: SupportsStr, value: Serializable) -> None:
        out[await serialize(key)] = await serialize(value)

    async with asyncio.TaskGroup() as tg:
        for k, v in obj.items():
            tg.create_task(add_map_pair(k, v))

    return out


@overload
async def serialize(obj: NoneType) -> None:
    return None


@overload
async def serialize(obj: ObjectSerializable) -> dict[str, IsSerialized]:
    out = obj.__serialize__()

    if isinstance(out, Awaitable):
        return await out

    return out


@overload
async def serialize(obj: float | SupportsFloat) -> float:
    return float(obj)


@overload
async def serialize(obj: SupportsInt) -> int:
    return int(obj)


@overload
async def serialize(obj: SupportsStr) -> SupportsStr:
    return str(obj)


async def serialize(obj: Any) -> IsSerialized:
    """Serialize an object to be JSON serializable.

    Args:
        obj (Any): The object to be serialized.

    Returns:
        IsSerialized: The serialized object.

    Raises:
        TypeError: If this base class is triggered then the object is not serializable.
    """
    if isinstance(obj, Serializable):
        return await serialize(obj)

    raise TypeError()
