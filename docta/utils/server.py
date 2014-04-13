"""
Simple HTTP-server for local testing.
"""
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import os

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000

# Python 3.x server
try:
    import http.server
    HTTPServer = http.server.HTTPServer
    HTTPRequestHandler = http.server.SimpleHTTPRequestHandler
# Python 2.x server
except ImportError:
    import BaseHTTPServer
    import SimpleHTTPServer
    HTTPServer = BaseHTTPServer.HTTPServer
    HTTPRequestHandler = SimpleHTTPServer.SimpleHTTPRequestHandler


def run(path, port=DEFAULT_PORT):
    """
    Start simple HTTP server at specified web root directory and port.
    """
    os.chdir(path)
    server_address = (DEFAULT_HOST, port)
    print("Serving directory: %s" % path)
    print("Running at http://%s:%s" % server_address)
    print(datetime.datetime.now().strftime('%d %B %Y - %H:%M:%S'))
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()
