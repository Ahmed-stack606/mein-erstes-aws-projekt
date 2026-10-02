# FleetPulse AI 🚲⚡

**AI Fleet Operations Intelligence for Shared Micromobility**

FleetPulse is a production-style portfolio project inspired by public challenges in shared micromobility: real-time vehicle telemetry, fleet reliability, battery availability, geospatial operations, anomaly detection and data-driven rebalancing.

> **Important:** This project uses synthetic data only. It is not affiliated with, endorsed by, or based on proprietary Lime data.

## Why this project is relevant to Lime

Lime's public careers material highlights engineering work around real-time location services, vehicle connectivity, backend infrastructure, data systems, internal tools, dashboards and operational data. FleetPulse demonstrates those ideas in one cohesive system.

### What it demonstrates

- **Python + FastAPI** REST backend
- **AI anomaly detection** with Isolation Forest + deterministic safety rules
- **Geospatial fleet intelligence** using vehicle coordinates and city zones
- **Battery and reliability monitoring**
- **Fleet rebalancing recommendations**
- **Interactive Streamlit operations dashboard**
- **Automated tests with pytest**
- **Dockerized service**
- **GitHub Actions CI**
- Clean separation between API, domain logic and data generation

## Architecture

```
Synthetic telemetry
      │
      ▼
Feature engineering
      │
      ├──────────────► AI anomaly scoring
      │                    │
      │                    ▼
      │              Priority queue
      │
      └──────────────► Zone demand/supply analysis
                           │
                           ▼
                    Rebalancing actions
                           │
                           ▼
             FastAPI ─────► Dashboard
```

## Run locally

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Generate telemetry

```bash
python -m fleetpulse.cli generate-data --vehicles 250 --hours 24
```

### 3. Start API

```uvicorn fleetpulse.api:app --reload
```

API docs: http://127.0.0.1:8000/docs

### 4. Start dashboard

In another terminal:

```bash
streamlit run dashboard/app.py
```

Dashboard: http://127.0.0.1:8501

### 5. Run tests

```bash
pytest
```

## Docker

```bash
docker build -t fleetpulse .
docker run -p 8000:8000 fleetpulse
```

## Example API calls

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/vehicles
curl http://127.0.0.1:8000/anomalies?limit=10
curl http://127.0.0.1:8000/rebalancing/recommendations
```

## Key engineering decisions

### 1. Safety before optimization

A vehicle with a possible safety issue receives a higher operational priority than a vehicle that only needs charging.

### 2. Hybrid anomaly detection

The system combines:

- deterministic safety rules for explainability
- Isolation Forest for unusual telemetry patterns

This makes alerts easier for operations teams to understand than a black-box score alone.

### 3. Geospatial operations

The fleet is divided into service zones. The recommender compares estimated demand against available vehicles and suggests where field teams should rebalance the fleet.

### 4. Explainable alerts

Every anomaly returns human-readable reasons such as:

- low battery
- abnormal temperature
- GPS degradation
- repeated brake events
- unusual telemetry pattern

## Example output

```json
{
  "vehicle_id": "LFP-0042",
  "severity": "critical",
  "priority_score": 0.91,
  "reasons": [
    "battery below 15%",
    "abnormal brake event frequency"
  ],
  "recommended_action": "collect_and_inspect"
}
```

## AWS extension

A natural production deployment would be:

**API Gateway / ALB → ECS Fargate → PostgreSQL/RDS → S3 → CloudWatch**

For real-time telemetry, the ingestion layer could be extended with:

**IoT Core / Kinesis → stream processing → feature store → anomaly service**

This repository intentionally keeps the local demo lightweight while documenting a scalable AWS path.

## Project structure

```
fleetpulse/
├── api.py
├── cli.py
├── config.py
├── models.py
├── services/
│   ├── anomaly_detection.py
│   ├── rebalancing.py
│   └── telemetry.py
tests/
├── test_anomaly_detection.py
├── test_rebalancing.py
└── test_api.py
dashboard/
└── app.py
.github/workflows/
└── ci.yml
infra/
└── aws-architecture.md
```

## Public references

- Lime Careers: https://www.li.me/about/careers
- Lime Innovation: https://www.li.me/why/innovation

## Portfolio goal

This project is designed to show that I can turn a real operational problem into an end-to-end software and AI system — from data generation and modeling to APIs, tests, deployment and an operations dashboard.
