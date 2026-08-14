# Snabbit Zero-to-One Platform Control Plane

A Snabbit-specific proof-of-work for a high-ownership Platform / Cloud Engineering role: building the platform from first principles rather than maintaining a mature internal platform.

The design focuses on the responsibilities highlighted in Snabbit's Platform Engineer opening: cloud infrastructure from scratch, platform architecture, observability, service onboarding, IaC and CI/CD, resilience and recovery, security, cost efficiency, canary delivery, and developer self-service.

## Core idea

**Make the safe production path the easiest path for every service team.**

Instead of a collection of scripts and tribal knowledge, this repository models a small platform control plane that evaluates whether a service is production-ready before it is onboarded.

```text
Developer change
    |
    v
Service contract
    |
    v
Platform readiness gate
    |-- infrastructure & ownership
    |-- observability & SLOs
    |-- deployment safety
    |-- resilience & recovery
    |-- security
    |-- cost controls
    v
IaC / CI-CD / Kubernetes deployment
    |
    v
Runtime telemetry + incident response
```

## What this POC demonstrates

- cloud and service ownership metadata
- Terraform/IaC enforcement
- CI/CD and immutable artifact requirements
- Kubernetes workload readiness
- logs, metrics, traces, dashboards, and alerting
- explicit SLOs and error budgets
- canary/progressive delivery with automated rollback
- autoscaling and resource limits
- multi-AZ readiness
- backup and disaster-recovery objectives
- secrets and workload identity
- least-privilege access
- cost ownership and budget attribution
- production and deliberately unsafe service contracts

## Repository layout

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   └── 30-60-90.md
├── examples/
│   ├── production-service.json
│   └── unsafe-service.json
├── src/snabbit_platform/
│   └── gate.py
└── tests/
    └── test_gate.py
```

## Production-readiness contract

The platform gate expects a service to declare its runtime and operational contract. This shifts infrastructure from ticket-driven work toward a repeatable internal platform interface.

A production service should declare:

- owner/team
- IaC source
- deployment strategy
- observability signals
- alert ownership
- SLO target
- autoscaling
- high-availability topology
- backup and recovery objectives
- workload identity / secrets handling
- cost attribution

The gate returns concrete violations rather than a generic pass/fail.

## Why this matters for Snabbit

A zero-to-one platform team has two competing pressures:

1. move quickly enough that product engineers are not blocked;
2. avoid creating infrastructure debt that compounds as traffic, teams, and services grow.

The control-plane approach provides a small number of opinionated defaults and makes exceptions visible. It creates a path for self-service onboarding while preserving reliability and security standards.

## Platform architecture

### 1. Service onboarding

A new service enters through a versioned service contract. The platform can translate that contract into:

- Terraform modules
- Kubernetes namespaces / workloads
- CI/CD templates
- dashboards and alerts
- secrets bindings
- autoscaling policy
- ownership metadata

### 2. Infrastructure as Code

No production infrastructure should be hand-created. Terraform plans go through review and policy checks before apply.

Recommended model:

```text
service repo -> reusable platform module -> plan -> policy gate -> apply
```

### 3. Delivery safety

Production releases should support:

- immutable artifacts
- health checks
- progressive rollout / canary
- automated rollback on SLO or error-rate breach
- deployment audit trail

### 4. Observability

Every service should emit:

- logs
- metrics
- traces

The service contract also carries the owning team and alert route, so an alert is actionable rather than merely visible.

Useful platform-level views include:

- request rate / latency / errors
- pod and node saturation
- deployment health
- queue depth
- downstream dependency errors
- cost by service/team/environment

### 5. Reliability and recovery

The gate treats resilience as an explicit contract:

- multi-AZ workloads where needed
- autoscaling
- defined RPO/RTO
- backup coverage
- restore testing
- runbook ownership

### 6. Security

The paved road favors:

- workload identity instead of static credentials
- least-privilege IAM
- secret manager integration
- namespace/network boundaries
- immutable images
- controlled production access

### 7. Cost as a platform signal

Every production workload should have ownership and cost attribution. Platform teams can then optimize the biggest cost/performance opportunities without turning optimization into guesswork.

## Run locally

```bash
python -m pytest -q
```

Example usage:

```python
import json
from src.snabbit_platform.gate import evaluate

contract = json.load(open("examples/production-service.json"))
result = evaluate(contract)
print(result.allowed)
print(result.findings)
```

## Extension path

A production implementation could extend this prototype with:

- Terraform modules for AWS/GCP foundations
- Kubernetes admission policies via OPA / Kyverno
- Argo CD or Flux GitOps
- Argo Rollouts / service-mesh canaries
- Prometheus / Grafana / OpenTelemetry
- Datadog integration
- Karpenter or cluster autoscaler
- SLO evaluation and error-budget policies
- automated DR exercises
- cloud-cost dashboards and anomaly detection
- developer portal / service catalog
- ephemeral environments
- policy-driven service onboarding

## 30 / 60 / 90 day direction

**0-30 days:** map current infra, deployment flow, incidents, cloud spend, ownership gaps, and critical service dependencies. Define the smallest paved-road contract.

**31-60 days:** ship reusable IaC, service onboarding templates, standard telemetry, alerting, and progressive-delivery defaults. Establish SLOs and recovery expectations for critical services.

**61-90 days:** add self-service workflows, cost visibility, automated policy enforcement, recovery drills, and platform SLOs. Reduce time-to-production for a new service while tightening reliability.

## Candidate

Rahul H Bhatia — Cloud / Platform / SRE Engineering

- LinkedIn: https://www.linkedin.com/in/rahul-h-bhatia/
- Portfolio: https://rahulhbhatia.vercel.app
- AWS badges: https://www.credly.com/users/rahul-h-bhatia/badges

## Disclaimer

This is an independent proof-of-work created from publicly available information about Snabbit's platform engineering requirements. It does not represent Snabbit's private architecture.
