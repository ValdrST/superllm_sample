import json
import logging
import pandas as pd
import time
from llama_cpp import Llama
import requests
import os

class Qwen():
    def __init__(self,context=2048, *args, **kwargs):
        self.model_path = './model/qwen2.5-0.5b-instruct-q4_0.gguf'
        self.n_ctx = context
        self.download_if_not_exists()
        self.llm = Llama(
            model_path = self.model_path,
            n_gpu_layers=-1,
            n_ctx = self.n_ctx
        )
    
    def download_if_not_exists(self):
        if not os.path.isfile(self.model_path):
            logging.info(f"{self.model_path} doesn't exists downloading")
            r = requests.get('https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_0.gguf', stream=True)
            with open(self.model_path,'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


    
    def get_llm_label(self,title, body):
        prompt = f'''
        Clasify next text in one of these words: News|Question|Announcement|Other return only one word
        text is:
        title: {title}
        body: {body}
        response:'''
        out = self.llm(
            prompt,
            max_tokens=16,
            temperature=0.0
        )
        text = out["choices"][0]["text"].strip()
        return text

