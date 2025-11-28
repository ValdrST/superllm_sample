import os
import requests
import hashlib
import logging
import time
import gzip
import cloudscraper

class RequestsChromium():
    def __init__(self, *args, **kwargs):
        self.status_code = 200
        self.content = None
        self.text = None


class Crawler():
    def __init__(self, *args, **kwargs):
        self.cache_dir = self.create_cache_dir()
        self.current_cache_proc = None
        self.session = None

    
    def create_cache_dir(self, cache_dir = './cache'):
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return cache_dir
    
    def validate_input_data(self,origin='csv',name_path='input.csv'):
        if origin == 'csv':
            if os.path.exists(name_path):
                return True
        return False

    def get_session(self,cookies={},headers={},proxies={}, *args,**kwargs) -> requests.Session:
        self.session = cloudscraper.create_scraper()
        #session = requests.session()
        self.session.headers = headers
        #session.cookies = cookies
        self.session.proxies = proxies
        self.session.cookies.update(cookies)
        return self.session

    def delete_cache(self):
        if os.path.exists(self.current_cache_proc):
            logging.info('deleting {}'.format(self.current_cache_proc))
            os.remove(self.current_cache_proc)
        else:
            logging.info('not deleting {}'.format(self.current_cache_proc))
    
    def get_cache(self,session=None,data=None,json=None,url=None,method='get',cache=True,stream=False):
        hash_value = hashlib.sha1(str([url,data,json,method]).encode('utf-8')).hexdigest()+'.gz'
        path_cache = os.path.join(self.cache_dir,hash_value)
        self.current_cache_proc = path_cache
        logging.info('making request url:{} data: {} json:{} method:{} path cache:{}'.format(url,data,json,method,path_cache))
        if not os.path.exists(path_cache) or not cache:
            logging.info('no cache found or deactivated')
            error = True
            error_count = 0
            while error:
                try:
                    if method == 'post':
                        r = self.session.post(data=data,json=json,url=url,timeout=360)
                    elif method == 'get':
                        r = self.session.get(data=data,json=json,url=url,timeout=360)
                    elif method == 'put':
                        r = self.session.put(data=data,json=json,url=url,timeout=360)
                    elif method == 'headless':
                        r = self.make_headless_get(url=url)
                        #r = self.make_headless_get(url=url)
                    else:
                        r = self.session.get(data=data,json=json,url=url,timeout=360)
                    error = False
                except TypeError as e:
                    logging.error(e)
                    time.sleep(1)
                    error_count += 1
                    if error_count >= 10:
                        logging.error('max error counts')
                        return 0,''
                    error = True
            with gzip.open(path_cache,'wb') as f:
                logging.info('writting cache in: {}'.format(path_cache))
                f.write(('{}\n'.format(r.status_code)).encode(encoding='utf-8'))
                #f.write(r.text.encode(encoding='utf-8'))
                f.write(r.content)
            if stream:
                return r.status_code, r.content
            else:
                return r.status_code, r.text
        else:
            logging.info('getting cache {}'.format(path_cache))
            if stream:
                with gzip.open(path_cache,'rb') as f:
                    data_read = f.read()
                    status_code = data_read[:4]
                    content_text = data_read[4:]
                return int(status_code.decode('utf-8')),content_text
            else:
                try:
                    with gzip.open(path_cache,'r') as f:
                        data_read = f.read().decode(encoding='utf-8').split('\n')
                        status_code = data_read[0]
                        content_text = '\n'.join(data_read[1:])
                    return int(status_code),content_text
                except:
                    return 500,'Error aplicativo'
