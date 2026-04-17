"""Logging abstracts module.

Defines classes to enable extended logging functionality that the logging module does not currently have, mainly
utilizing t-strings so that they can be used as log messages. As str() does not convert t-strings automatically, they
cannot be logged without issues. To solve this t-strings are encapsulated in a wrapper class that provides the __str__
method. To make sure that this does not need to be done by the programmer for every t-string, an adapter is provided
that will automate this encapsulation.

Example:
    logger = TemplateStringAdapter(logging.getLogger(__name__))

    logger.info(t'Hello World')
"""

import logging
from string.templatelib import Interpolation, Template, convert
from typing import Mapping


class TemplateStringAdapterWrapper:
    """Wrapper class for template strings to allow them to be used with logging.

    What this does is encapsulate a t-string so that when str() is called it will automatically be converted.
    Normally t-strings do not support this behavior. The benefit is when combined with the TemplateStringAdapter. It can
    take the t-string by default, allowing one to use t-strings normally to write log messages, and wraps them in this
    adapter. Thus, the t-string can be rendered normally by existing logging mechanisms without any extra change.

    Attributes:
        template (Union[str, string.templatelib.Template]): String or template string to wrap
    """

    template: Interpolation | str | Template

    def __init__(self, template: Interpolation | str | Template) -> None:
        """Initialize the wrapper with a template string.

        Args:
            template (Union[str, string.templatelib.Template]): String or template string to wrap
        """
        self.template = template

    def __str__(self) -> str:
        """Convert to string.

        Returns:
            str: String representation of self.template
        """
        if isinstance(self.template, Interpolation) or isinstance(
            self.template, Template
        ):
            return convert(self.template, 's')

        return self.template.__str__()


class TemplateStringAdapter(logging.LoggerAdapter):
    """LoggerAdapter that accepts t-strings as log messages.

    This anticipates that a log message is passed in as a string or t-string. If
    it is a string it is handled normally, but if it is a t-string it is
    deconstructed. The string portions of the t-string will be passed as the
    message with sequential IDs. The interpolations themselves will be added to
    the extra kwarg wrapped in a TemplateStringAdapterWrapper. This allows for
    sensitive data to be hidden until rendering while also benefitting from the
    template strings deferred rendering. Finally, it provides an exceptionally
    easy logging interface that allows developers to use normal logging
    functions with t-strings as if they were f-strings. It turns a bad pattern
    into a perfectly acceptable practice using t-strings.
    """

    def process(
        self, msg: str | Template, kwargs: Mapping | None
    ) -> tuple[str | TemplateStringAdapterWrapper, Mapping | None]:
        """Process log messages and wrap t-strings in TemplateStringAdapter.

        Args:
            msg (Union[str, string.templatelib.Template]): String or template string to wrap
            kwargs (Optional[Mapping]): Logging kwargs

        Returns:
            tuple[Union[str, TemplateStringAdapterWrapper], Optional[Mapping]]: Log message and kwargs. May or may not
            be wrapped in a TemplateStringAdapterWrapper depending on if it is a string or not already.
        """
        if isinstance(msg, str):
            return msg, kwargs
        elif isinstance(msg, Template):
            extra = kwargs.get('extra', {}) if kwargs else {}

            ret = ''
            for obj in iter(msg):
                if isinstance(obj, Interpolation):
                    uid = f'_{len(extra)}'
                    extra[uid] = TemplateStringAdapterWrapper(obj)
                    ret += f'{{{uid}}}'
                else:
                    ret += obj

            kwargs['extra'] = extra

            return ret, kwargs
        else:
            raise TypeError('msg must be a string or template object')
