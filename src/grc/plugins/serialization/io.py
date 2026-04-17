"""Serialization I/O Module."""

import asyncio
import logging
from typing import (
    Awaitable,
    Mapping,
    Sequence,
    SupportsFloat,
    SupportsInt,
    overload,
)

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
    pass


@overload
async def serialize(obj: float | SupportsFloat) -> float:
    pass


@overload
async def serialize(obj: int | SupportsInt) -> int:
    pass


@overload
async def serialize(obj: str | SupportsStr) -> str:
    pass


@overload
async def serialize(obj: None) -> None:
    pass


@overload
async def serialize(obj: Sequence[Serializable]) -> list[IsSerialized]:
    pass


@overload
async def serialize(
    obj: Mapping[str | SupportsStr, Serializable],
) -> dict[str, IsSerialized]:
    pass


@overload
async def serialize(obj: ObjectSerializable) -> dict[str, IsSerialized]:
    pass


async def serialize(obj: Serializable) -> IsSerialized:
    """Serialize an object to be JSON serializable.

    Args:
        obj (Any): The object to be serialized.

    Returns:
        IsSerialized: The serialized object.

    Raises:
        TypeError: If this base class is triggered then the object is not serializable.
    """
    if (
        isinstance(obj, bool)
        or isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, str)
        or obj is None
    ):
        return obj
    elif isinstance(obj, Sequence):
        return await asyncio.gather(*[serialize(x) for x in obj])
    elif isinstance(obj, Mapping):
        out = {}

        async def add_map_pair(key: SupportsStr, value: Serializable) -> None:
            out[await serialize(key)] = await serialize(value)

        async with asyncio.TaskGroup() as tg:
            for k, v in obj.items():
                tg.create_task(add_map_pair(k, v))

        return out
    elif isinstance(obj, ObjectSerializable):
        out = obj.__serialize__()

        if isinstance(out, Awaitable):
            return await out

        return out
    elif isinstance(obj, SupportsStr):
        return str(obj)
    elif isinstance(obj, SupportsFloat):
        return float(obj)
    elif isinstance(obj, SupportsInt):
        return int(obj)

    logger.error(t'Could not serialize object {repr(obj)}')
    raise TypeError()
