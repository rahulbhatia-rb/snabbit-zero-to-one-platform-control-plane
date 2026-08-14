import json
from pathlib import Path

from src.snabbit_platform.gate import evaluate


def load(name: str) -> dict:
    return json.loads((Path(__file__).parents[1] / "examples" / name).read_text())


def test_production_service_passes():
    result = evaluate(load("production-service.json"))
    assert result.allowed
    assert result.findings == []


def test_unsafe_service_fails():
    result = evaluate(load("unsafe-service.json"))
    assert not result.allowed
    assert len(result.findings) >= 10
