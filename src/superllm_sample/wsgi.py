#!/usr/bin/env python
from .main import application
from waitress import serve
import logging
def wsgi():
    logging.info('Iniciado WSGI')
    serve(application, port=3000, unix_socket_perms='666', ident="somch_api_market",threads=64)
