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


import argparse
import logging

from grc.plugins.logging import TemplateStringAdapter


logger = TemplateStringAdapter(logging.getLogger(__name__))


def add_plugin_parser(subparsers: argparse._SubParsersAction) -> None:
    run_parser = subparsers.add_parser('run', help='run webserver', description='run_webserver')

    run_parser_server_group = run_parser.add_argument_group('server options')

    run_parser_server_group.add_argument('--host', metavar='HOST')
    run_parser_server_group.add_argument('--port', metavar='PORT', type=int)
    run_parser_server_group.add_argument('--env-file', metavar='PATH')

    run_parser_header_group = run_parser.add_argument_group('header options')

    run_parser_header_group.add_argument('--root-path', metavar='PATH')
    run_parser_header_group.add_argument('--proxy-headers')
    run_parser_header_group.add_argument('--forwarded-allow-ips', metavar='IP', action='extend', nargs='+')
    run_parser_header_group.add_argument('--server-header', action=argparse.BooleanOptionalAction)
    run_parser_header_group.add_argument('--date-header', action=argparse.BooleanOptionalAction)

    run_parser_ssl_group = run_parser.add_argument_group('ssl options')

    run_parser_ssl_group.add_argument('--ssl-keyfile', metavar='PATH')
    run_parser_ssl_group.add_argument('--ssl-keyfile-passwd', metavar='STR')
    run_parser_ssl_group.add_argument('--ssl-certfile', metavar='PATH')
    run_parser_ssl_group.add_argument('--ssl-version', metavar='VERSION')
    run_parser_ssl_group.add_argument('--ssl-ca-certs', metavar='PATH')
    run_parser_ssl_group.add_argument('--ssl-ciphers', metavar='CIPHERS')

    run_parser_limit_group = run_parser.add_argument_group('limit options')

    run_parser_limit_group.add_argument('--limit-concurrency', type=int)
    run_parser_limit_group.add_argument('--limit-max-requests', type=int)
    run_parser_limit_group.add_argument('--limit-max-requests-jitter', type=int)
    run_parser_limit_group.add_argument('--backlog', type=int)

    run_parser_timeout_group = run_parser.add_argument_group('timeout options')

    run_parser_timeout_group.add_argument('--timeout-keep-alive', type=int)
    run_parser_timeout_group.add_argument('--timeout-graceful-shutdown', type=int)
