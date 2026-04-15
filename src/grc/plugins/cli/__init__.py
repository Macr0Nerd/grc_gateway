##############################################################################
##  Copyright (C) 2026  Eva Ron-Bonilla                                     ##
##                                                                          ##
##  This program is free software: you can redistribute it and/or modify    ##
##  it under the terms of the GNU General Public License as published by    ##
##  the Free Software Foundation, either version 3 of the License, or       ##
##  (at your option) any later version.                                     ##
##                                                                          ##
##  This program is distributed in the hope that it will be useful,         ##
##  but WITHOUT ANY WARRANTY; without even the implied warranty of          ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           ##
##  GNU General Public License for more details.                            ##
##                                                                          ##
##  You should have received a copy of the GNU General Public License       ##
##  along with this program.  If not, see <https://www.gnu.org/licenses/>.  ##
##############################################################################


__all__ = [
    '__version__',
    'cli',
]

from grc.dunders import __version__
from grc.plugins.plugins import PluginInfo

from grc.plugins.cli.application import cli


plugin_info = PluginInfo(
    plugin_name="cli",
    plugin_description="command line interface plugin",
    plugin_version=__version__,
)
