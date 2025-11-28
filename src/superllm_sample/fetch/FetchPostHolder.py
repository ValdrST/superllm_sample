from ..core.Crawler import Crawler
import logging
import json
import requests
import requests

class FetchPostHolder(Crawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_dir = self.create_cache_dir()

    def get_session_custom(self) -> requests.Session:
        session = self.get_session()
        return session

    def fetch(self, limit = 100):
        logging.info('start fetch API')
        session = self.get_session_custom()
        r = requests.get('https://jsonplaceholder.typicode.com/posts')
        text_data = r.text
        if r.status_code == 200:
            obj_data = json.loads(text_data)
        else:
            obj_data = {}
        return obj_data
