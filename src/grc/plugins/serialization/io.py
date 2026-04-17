"""Serialization I/O Module."""

import asyncio
import logging
from typing import Awaitable, Mapping, Sequence, SupportsFloat, SupportsInt

from grc.plugins.logging import TemplateStringAdapter
from grc.plugins.serialization.abstract import (
    IsSerialized,
    ObjectSerializable,
    Serializable,
    SupportsStr,
)

logger = TemplateStringAdapter(logging.getLogger(__name__))


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
