# SuperLLM Sample (CPU Edition)

This project provides a local LLM inference service using `llama-cpp-python` running **entirely inside Docker**, using **CPU only**.  
It is compatible with **Windows**, **Linux**, and **macOS**, as long as Docker Desktop is installed.

## Requirements

- Docker Desktop (Windows / Linux / macOS)
- Docker Compose v2
- At least **8 GB RAM**
- A GGUF model placed in the `models/` directory

## Project Structure

```
│   config.json
│   docker-compose.yml
│   Dockerfile
│   pyproject.toml
│   readme.md
│
├───log
│       superllm_sample.log
│
├───model
│       qwen2.5-0.5b-instruct-q4_0.gguf
│
├───output
├───postgres
│       Dockerfile
│
└───src
    │   readme.md
    │   requirements.txt
    │   setup.py
    │
    ├───cache
    ├───live
    ├───log
    ├───model
    ├───output
    └───superllm_sample
        │   main.py
        │   wsgi.py
        │   __init__.py
        │
        ├───core
        │       Crawler.py
        │       Server.py
        │       SQLResolver.py
        │       __init__.py
        │
        ├───fetch
        │       FetchPostHolder.py
        │       __init__.py
        │
        ├───models
        │       Qwen.py
        │       __init__.py
        │
        └───pipeline
                Pipeline.py
                __init__.py
```

## Model Setup

Place your `.gguf` model into `models/`, for example:

```
models/model.gguf
```

Recommended CPU models:
- LLaMA-3.1 8B Instruct (Q4_K_M)
- Mistral-7B v0.3 Instruct (Q4_K_M)

## Running with Docker Compose

### 1. Build the image

```
docker-compose --build
```

### 2. Start the service

```
docker-compose up
```

The API will be available at:

```
http://localhost:3003
```

To run in the background:

```
docker compose up -d
```

To stop:

```
docker-compose down
```

## Internal Architecture

```
Docker Container
│
├── Flask Server
├── llama-cpp-python (CPU mode)
└── GGUF Model
```

## Environment Variables

| Variable     | Description                     | Example              |
|--------------|---------------------------------|----------------------|
| MODEL_PATH   | Path to the GGUF model          | /models/model.gguf   |
| N_THREADS    | Number of CPU threads           | 4                    |
| MAX_TOKENS   | Max output tokens               | 2048                 |
| HOST         | Bind address                    | 0.0.0.0              |
| PORT         | API port                        | 3003                 |


## Performance Tips (CPU Only)

- Use quantized models (Q4_K_M)
- Increase CPU threads in docker-compose.yml
- Prefer models < 8B for laptops or small servers

## Cleaning Up

```
docker compose down
docker rmi superllm_sample
```


## Running & Testing the Pipeline

Once the containers are up, you can run and test the pipeline using the following endpoints:

### ▶️ Run the Pipeline
Trigger the full ETL + LLM enrichment pipeline:

```
http://localhost:3002/run_pipeline
```

### 📥 Fetch Processed Results
Retrieve enriched and validated records.  
For example, to fetch the record with ID=10:

```
http://localhost:3002/posts/10
```

## Credits

Built with:
- llama-cpp-python
- Python 3
- Docker
- PostgreSQL
