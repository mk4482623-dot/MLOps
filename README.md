# MLOps Batch Pipeline

## Overview

This project implements a minimal MLOps-style batch processing pipeline designed for reproducibility, observability, and deployment readiness.

The pipeline processes OHLCV data to generate a simple trading signal based on rolling mean comparison.

---

## Features

* Config-driven execution using YAML
* Deterministic results using random seed
* Robust data validation and error handling
* Rolling mean computation on `close` price
* Binary signal generation
* Structured metrics output(JSON)
* Detailed logging for observability
* Docker-ready deployment

---

## Project Structure

```
mlops-task/
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── metrics.json
├── run.log
└── README.md
```

---

## Local Execution

```bash
pip install -r requirements.txt
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Docker Execution

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

---

## Docker Execution Problem

Due to system-level permission constraints, Docker Desktop could not be executed locally. However, the Dockerfile follows standard practices and should run correctly in any Docker-enabled environment.

---

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

---

## Design Decisions

* Rolling mean uses window from config for flexibility
* Initial NaN rows are dropped to maintain signal consistency
* Logging added at each stage for observability
* Metrics written even in failure cases for reliability

---

## How This Reflects MLOps Principles

* **Reproducibility** → config + seed
* **Observability** → logs + structured metrics
* **Deployment Ready** → Dockerized execution


