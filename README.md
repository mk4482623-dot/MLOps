# MLOps Batch Pipeline

## Overview

This project implements a reproducible batch data processing pipeline with logging, metrics tracking, and Docker support.

## Local Execution

```bash
pip install -r requirements.txt
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Docker Execution

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

## Problem on Docker Execution

Due to local system-level permission constraints, Docker Desktop could not be fully configured on machine.

However, the Dockerfile is implemented following standard practices and has been verified logically. The container should build and run successfully in any standard Docker-enabled environment.

## Features

* Config-driven pipeline(YAML)
* Deterministic execution using seed
* Rolling mean computation
* Binary signal generation
* Structured metrics output(JSON)
* Detailed logging for observability
* Docker-ready deployment

## Example Output

```json
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.5,
  "latency_ms": 59,
  "seed": 42,
  "status": "success"
}
```
