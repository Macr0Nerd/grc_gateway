"""CLI abstracts module."""

import dataclasses
from types import ModuleType
from typing import Callable


@dataclasses.dataclass
class PluginMetadata:
    """CLI plugin metadata class.

    Attributes:
        arguments_callable (callable): Callable that adds CLI arguments
        command_module (ModuleType): Module that has CLI plugin commands as callable attributes
    """

    arguments_callable: Callable
    command_module: ModuleType
