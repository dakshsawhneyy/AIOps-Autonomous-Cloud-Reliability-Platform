# The core mission of this autonomous AIOps platform
Build an autonomous cloud reliability platform that detects failures early, predicts load, heals services without human involvement, prevents outages, and keeps applications within SLOs across multi-region infrastructure.

# Identifying 12 Failure Scenarios
### Application Failures
- Pod CrashLoopBackoff
- Sudden spike in 5xx errors
- Memory leak increasing container RSS
- API latency crossing p95 threshold

### Infrastructure Failures
- Node goes NotReady
- High disk pressure on node
- RDS/DynamoDB read latency spike
- Network packet loss between services

### Traffic / Load Failures
- Incoming traffic spike (3× in minutes)
- Kafka consumer lag increasing abnormally
- SQS queue depth suddenly rising
- Upstream API throttling your service

# Core Metrics Needed:
- Pod health, restart count
- CPU/memory per pod
- p95/p99 latency
- 5xx rate
- Node health events
- DB query latency
- Kafka lag
- Queue depth
- Network error rate

### Healing Actions
- Restart pod
- Kill stuck container
- Scale deployment
- Cordon + drain unhealthy node
- Trigger ArgoCD auto-rollback
- Increase HPA targets
- Switch read/write to secondary DB
- Add Kafka consumers
- Reduce traffic via rate limiting
- Recreate problematic pod on new node
- Clear queue or reroute traffic
- Trigger failover to second region

# SLOs / SLIs
### SLO 1 — Latency
- SLO: p95 < 150ms
- SLI: API latency
- Error Budget: 0.1% slow requests

### SLO 2 — Availability
- SLO: 99.9%
- SLI: success rate
- Error Budget: 0.1% errors

### SLO 3 — Reliability
- SLO: < 5 auto-heal failures per week
- SLI: auto-heal success rate
- Error Budget: 5 failures/week

### Success Criteria
- Anomalies detected before user impact
- Auto-healing resolves issues without human
- Chaos tests pass (pod kill, latency injection)
- Predictive autoscaling triggers correctly
- Model versioning & rollback working
- Multi-region failover works
- Observability dashboards show correct RCA
- Zero manual intervention for common issues