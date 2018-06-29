"""
proxy_handler.py

Copyright 2018 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
from w3af.core.data.request.fuzzable_request import FuzzableRequest
from w3af.core.controllers.daemons.proxy import Proxy, ProxyHandler


class LoggingHandler(ProxyHandler):

    def _send_http_request(self, http_request, grep=True):
        """
        Send a w3af HTTP request to the web server using w3af's HTTP lib,
        capture the HTTP response and send it to the upstream Queue.

        The Queue should be consumed by another part of the code, requests
        and responses should be sent to the framework for further processing.

        No error handling is performed, someone else should do that.

        :param http_request: The request to send
        :return: The response
        """
        http_response = super(LoggingHandler, self)._send_http_request(http_request, grep=grep)

        # Send the request to the core
        freq = FuzzableRequest.from_http_request(http_request)
        self.parent_process.queue.put((freq, http_response))

        return http_response


class LoggingProxy(Proxy):
    def __init__(self, ip, port, uri_opener, handler_klass=LoggingHandler,
                 ca_certs=Proxy.CA_CERT_DIR, name='LoggingProxyThread',
                 queue=None):
        """
        Override the parent init so we can save the plugin reference, all the
        rest is just the same.
        """
        super(LoggingProxy, self).__init__(ip, port, uri_opener,
                                           handler_klass=handler_klass,
                                           ca_certs=ca_certs,
                                           name=name)
        self.queue = queue