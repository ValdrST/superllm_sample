FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

WORKDIR /opt/superllm_sample

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv python3-psycopg2 curl htop git && \
    apt-get clean

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install waitress \
               paramiko \
               python-socketio \
               sqlalchemy \
               flask \
               pexpect \
               pandas \
               PyMySQL \
               rake-nltk \
               bs4 \
               flask-restx 

RUN apt-get update && apt-get install -y python3-dev build-essential python3-setuptools python3-wheel wget
ENV CMAKE_ARGS="-DGGML_CUDA=on -DGGML_CUDA_NO_PEER_COPY=on -DGGML_CUDA_F16=on -DGGML_CUDA_DMMV=on"
ENV FORCE_CMAKE=1
RUN pip install llama-cpp-python --no-cache-dir --force-reinstall --no-binary=llama-cpp-python llama-cpp-python
COPY src/ /opt/superllm_sample_build/
RUN pip install /opt/superllm_sample_build

ENTRYPOINT ["superllm_sampleWSGI"]