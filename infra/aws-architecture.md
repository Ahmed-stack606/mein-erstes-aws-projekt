# AWS production architecture

## Target architecture

1. **Telemetry ingestion** — AWS IoT Core or Kinesis Data Streams
2. **Stream processing** — Lambda / ECS service for validation and enrichment
3. **Feature storage** — S3 for raw telemetry; RDS PostgreSQL for operational state
4. **AI service** — ECS Fargate running the FastAPI anomaly/rebalancing service
5. **API edge** — Application Load Balancer + HTTPS
6. **Observability** — CloudWatch metrics, logs and alarms
7. **CI/CD** — GitHub Actions → container build → Amazon ECR → ECS deployment

## Design principles

- Stateless API containers for horizontal scaling
- S3 as durable raw-data storage
- PostgreSQL for queryable fleet state
- Separate ingestion from customer-facing APIs
- Explicit monitoring and alerting for operations-critical services

## Interview discussion points

A strong next step would be replacing generated telemetry with a streaming contract and adding idempotent event processing, data retention policies, authentication, rate limiting and infrastructure-as-code.
