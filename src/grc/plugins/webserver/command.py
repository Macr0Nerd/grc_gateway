"""Webserver CLI commands."""

import argparse
import logging

import uvicorn

from grc.plugins.logging import LOG_CONFIG, TemplateStringAdapter

logger = TemplateStringAdapter(logging.getLogger(__name__))


def add_plugin_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add webserver arguments.

    Args:
        subparsers (argparse._SubParsersAction): Plugin arguments subparser
    """
    run_parser = subparsers.add_parser(
        'run', help='run webserver', description='run_webserver'
    )

    run_parser_server_group = run_parser.add_argument_group('server options')

    run_parser_server_group.add_argument('--host', metavar='HOST')
    run_parser_server_group.add_argument('--port', metavar='PORT', type=int)
    run_parser_server_group.add_argument('--env-file', metavar='PATH')

    run_parser_header_group = run_parser.add_argument_group('header options')

    run_parser_header_group.add_argument('--root-path', metavar='PATH')
    run_parser_header_group.add_argument('--proxy-headers')
    run_parser_header_group.add_argument(
        '--forwarded-allow-ips', metavar='IP', action='extend', nargs='+'
    )
    run_parser_header_group.add_argument(
        '--server-header', action=argparse.BooleanOptionalAction
    )
    run_parser_header_group.add_argument(
        '--date-header', action=argparse.BooleanOptionalAction
    )

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
    run_parser_timeout_group.add_argument(
        '--timeout-graceful-shutdown', type=int
    )


def run(**kwargs: dict) -> int:
    """Run uvicorn webserver.

    Args:
        **kwargs (dict): Keyword arguments optionally containing uvicorn configuration

    Returns:
        int: status code
    """
    uvicorn.run(
        'grc:app',
        factory=True,
        log_config=LOG_CONFIG,
        **{
            k: v
            for k, v in {
                'host': kwargs.get('host'),
                'port': kwargs.get('port'),
                'env_file': kwargs.get('env_file'),
                'root_path': kwargs.get('root_path'),
                'proxy_headers': kwargs.get('proxy_headers'),
                'forwarded_allow_ips': kwargs.get('forwarded_allow_ips'),
                'server_header': kwargs.get('server_header'),
                'date_header': kwargs.get('date_header'),
                'ssl_keyfile': kwargs.get('ssl_keyfile'),
                'ssl_keyfile_password': kwargs.get('ssl_keyfile_password'),
                'ssl_certfile': kwargs.get('ssl_certfile'),
                'ssl_version': kwargs.get('ssl_version'),
                'ssl_ca_certs': kwargs.get('ssl_ca_certs'),
                'ssl_ciphers': kwargs.get('ssl_ciphers'),
                'limit_concurrency': kwargs.get('limit_concurrency'),
                'limit_max_requests': kwargs.get('limit_max_requests'),
                'limit_max_requests_jitter': kwargs.get(
                    'limit_max_requests_jitter'
                ),
                'backlog': kwargs.get('backlog'),
                'timeout_keep_alive': kwargs.get('timeout_keep_alive'),
                'timeout_graceful_shutdown': kwargs.get(
                    'timeout_graceful_shutdown'
                ),
            }.items()
            if v is not None
        },
    )

    return 0
