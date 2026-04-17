"""Webserver application."""

import logging

from grc.plugins.logging.abstract import TemplateStringAdapter

logger = TemplateStringAdapter(logging.getLogger(__name__))
