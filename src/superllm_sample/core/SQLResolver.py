import json
from sqlalchemy.engine import create_engine
import logging


class SQLResolver():
    def __init__(self, *args, **kwargs):
        with open('config.json','r') as f:
            self.servers = json.load(f)['sql']
        self.engine = None
        

    def get_engine(self, name = '',*args, **kwargs):
        config_server = self.servers[name]
        if config_server.get('password'):
            connect_str = '{}://{}:{}@{}:{}/{}'.format(config_server['type'],config_server['user'],config_server['password'],config_server['host'],config_server['port'],config_server['database'])
            return create_engine(connect_str)
        else:
            connect_str = '{}://{}@{}:{}/{}'.format(config_server['type'],config_server['user'],config_server['host'],config_server['port'],config_server['database'])
            logging.info(connect_str)
            return create_engine(connect_str)
