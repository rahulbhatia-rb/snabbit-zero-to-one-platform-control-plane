from dataclasses import dataclass


@dataclass
class Result:
    allowed: bool
    findings: list[str]


def evaluate(spec: dict) -> Result:
    findings: list[str] = []

    checks = [
        (spec.get("owner"), "service owner is required"),
        (spec.get("iac") is True, "production infrastructure must be managed as code"),
        (spec.get("cicd") is True, "CI/CD automation is required"),
        (spec.get("immutable_artifacts") is True, "release artifacts must be immutable"),
        (set(["logs", "metrics", "traces"]).issubset(set(spec.get("observability", []))), "logs, metrics, and traces are required"),
        (spec.get("slo", {}).get("availability", 0) >= 99.9, "availability SLO must be at least 99.9%"),
        (spec.get("alert_owner") is not None, "alerts need an explicit owning team"),
        (spec.get("autoscaling") is True, "autoscaling is required"),
        (spec.get("multi_az") is True, "multi-AZ readiness is required"),
        (spec.get("rpo_minutes", 9999) <= 60, "RPO must be 60 minutes or less"),
        (spec.get("rto_minutes", 9999) <= 120, "RTO must be 120 minutes or less"),
        (spec.get("backup_restore_tested") is True, "backup restore must be tested"),
        (spec.get("workload_identity") is True, "workload identity is required"),
        (spec.get("least_privilege") is True, "least-privilege access is required"),
        (spec.get("secrets_managed") is True, "managed secrets are required"),
        (spec.get("progressive_delivery") is True, "progressive delivery is required"),
        (spec.get("automatic_rollback") is True, "automatic rollback is required"),
        (spec.get("cost_owner") is not None, "cost ownership is required"),
    ]

    for ok, message in checks:
        if not ok:
            findings.append(message)

    return Result(allowed=not findings, findings=findings)
