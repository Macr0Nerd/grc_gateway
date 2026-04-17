"""Plugin filters."""

from abc import ABC, abstractmethod
from typing import Any, Mapping

from grc.plugins.plugins.abstract import PluginInfo


class PluginFilter(ABC):
    """Plugin filter base class."""

    @abstractmethod
    def __call__(self, plugin: PluginInfo) -> bool:
        """Filter callable.

        Args:
            plugin (PluginInfo): Plugin information

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError()


class MetadataFilter(PluginFilter):
    """Metadata plugin filter.

    Examples:
        filter = MetadataFilter({'plugin_name': {}})

    Attributes:
        filters (dict[str, str | None]): key:value pairs to filter on
    """

    def __init__(self, filters: dict[str, str | None]) -> None:
        """Initialize the filter.

        Args:
            filters (dict[str, Optional[str]]): key:value pairs to filter on
        """
        self.filters = filters

    def __call__(self, plugin: PluginInfo) -> bool:
        """Call the filter.

        Args:
            plugin (PluginInfo): Plugin information

        Returns:
            bool: True if the plugin matches the filter, False otherwise
        """
        if plugin.plugin_metadata:
            for key, value in self.filters.items():
                if not self.validate(key, value, plugin.plugin_metadata):
                    return False

            return True

        return False

    @classmethod
    def validate(cls, key: str, expected: Any, actual: Mapping) -> bool:  # noqa: ANN401
        """Validate the given key and expected value.

        This checks against the type of the expected value. If the type is none
        then the filter is a key only filter. If the expected value is a mapping
        then it is a complex filter and we have to recursively iterate through
        the filter. If the expected value is not a mapping then it is considered
        the value to compare against.

        Args:
            key (str): The key to validate
            expected (Any): The expected value
            actual (Mapping): The actual value

        Returns:
            bool: True if the key matches the expected value, False otherwise

        Todo:
            * Add checking against a list of options
        """
        if key in actual:
            if expected is None:
                return True

            if isinstance(expected, Mapping):
                for expected_key, expected_value in expected.items():
                    if not cls.validate(
                        expected_key, expected_value, actual[key]
                    ):
                        return False

                return True

            return expected == actual

        return False
