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


import logging

import uvicorn

from grc.plugins.logging import LOG_CONFIG, TemplateStringAdapter


logger = TemplateStringAdapter(logging.getLogger(__name__))


def run(**kwargs) -> int:
    uvicorn.run(
        'grc:app',
        factory=True,
        log_config=LOG_CONFIG,
        host=kwargs.get('host'),
        port=kwargs.get('port'),
        env_file=kwargs.get('env_file'),
        root_path=kwargs.get('root_path'),
        proxy_headers=kwargs.get('proxy_headers'),
        forwarded_allow_ips=kwargs.get('forwarded_allow_ips'),
        server_header=kwargs.get('server_header'),
        date_header=kwargs.get('date_header'),
        ssl_keyfile=kwargs.get('ssl_keyfile'),
        ssl_keyfile_password=kwargs.get('ssl_keyfile_password'),
        ssl_certfile=kwargs.get('ssl_certfile'),
        ssl_version=kwargs.get('ssl_version'),
        ssl_ca_certs=kwargs.get('ssl_ca_certs'),
        ssl_ciphers=kwargs.get('ssl_ciphers'),
        limit_concurrency=kwargs.get('limit_concurrency'),
        limit_max_requests=kwargs.get('limit_max_requests'),
        limit_max_requests_jitter=kwargs.get('limit_max_requests_jitter'),
        backlog=kwargs.get('backlog'),
        timeout_keep_alive=kwargs.get('timeout_keep_alive'),
        timeout_graceful_shutdown=kwargs.get('timeout_graceful_shutdown'),
    )

    return 0