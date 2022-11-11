#!/usr/bin/env python3
# From: 
# - https://gist.github.com/SeanPesce/af5f6b7665305b4c45941634ff725b7a
# - https://stackoverflow.com/a/69088143/11438489

# References:
#   https://stackoverflow.com/questions/19705785/python-3-simple-https-server
#   https://docs.python.org/3/library/ssl.html
#   https://docs.python.org/3/library/http.server.html

from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import ssl

HTTPS_PORT=2008
PATH_TO_SERVER_CERT="/files/certs/server.crt"
PATH_TO_SERVER_KEY="/files/certs/server.key"
SERVE_PATH="/files/bins/"

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(certfile=PATH_TO_SERVER_CERT, keyfile=PATH_TO_SERVER_KEY, password='')
    handler = partial(SimpleHTTPRequestHandler, directory=SERVE_PATH)
    httpd = HTTPServer(('0.0.0.0', HTTPS_PORT), handler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
