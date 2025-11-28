#!/usr/bin/env python
#from .shared.infraestructura import Console
from superllm_sample.core import Server

application = Server("somch_api_market").app
def main():
  application.run(debug=True,port=3000,host='0.0.0.0')