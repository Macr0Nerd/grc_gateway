"""Serialization I/O Module."""

from typing import Mapping, Sequence, SupportsFloat, SupportsInt, overload

from grc.plugins.serialization.abstract import (
    IsSerialized,
    ObjectSerializable,
    Serializable,
    SupportsStr,
)

@overload
async def serialize(obj: bool) -> bool: ...
@overload
async def serialize(obj: float | SupportsFloat) -> float: ...
@overload
async def serialize(obj: int | SupportsInt) -> int: ...
@overload
async def serialize(obj: str | SupportsStr) -> str: ...
@overload
async def serialize(obj: None) -> None: ...
@overload
async def serialize(obj: Sequence[Serializable]) -> list[IsSerialized]: ...
@overload
async def serialize(
    obj: Mapping[str | SupportsStr, Serializable],
) -> dict[str, IsSerialized]: ...
@overload
async def serialize(obj: ObjectSerializable) -> dict[str, IsSerialized]: ...
async def serialize(obj: Serializable) -> IsSerialized: ...
