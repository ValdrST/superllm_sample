from flask import Flask, request, Blueprint, jsonify, render_template
from ..pipeline.Pipeline import Pipeline
import logging
from typing import List, Optional
from logging.handlers import RotatingFileHandler
rot_handler = RotatingFileHandler(filename='./log/superllm_sample.log', mode='a', maxBytes=10*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
logging.basicConfig(format='%(asctime)s|%(levelname)s|%(funcName)s|%(lineno)d|%(message)s', level=logging.INFO,handlers=[rot_handler])
superllm_sample_root = Blueprint('superllm_sample_root', __name__,url_prefix='/')
class Server():
    def __init__(self, name, *args, **kwargs):
        self.app = Flask(name)
        self.app.config['RESTPLUS_MASK_SWAGGER'] = True
        self.app.register_blueprint(superllm_sample_root)        

    @superllm_sample_root.route('/',methods=['GET'])
    def index():
        return jsonify({'message':'it works'}),200
    
    @superllm_sample_root.route('/run_pipeline',methods=['GET'])
    def startup_event():
        # Run pipeline at startup (idempotent)
        try:
            logging.info('Starting pipeline (startup)')
            pipeline = Pipeline()
            pipeline.run_pipeline(limit=100, enrich=True)
            return jsonify({'message':'pipeline done'}),200
        except Exception as e:
            logging.error('Pipeline error at startup: %s', e)
            return jsonify({'error':'error in pipeline','message':str(e)}),500

    @superllm_sample_root.route('/posts/<limit>',methods=['GET'])
    def get_posts(limit: int):
        pipeline = Pipeline()
        results = pipeline.load_results(limit=limit)
        if not results:
            return jsonify({'error':'No data available'}),404
        return jsonify({'data':results}),200
