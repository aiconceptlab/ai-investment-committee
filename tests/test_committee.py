import asyncio
import json

import httpx
import pytest

from src.committee import convene
from src.example import example
from src.providers import Completion, Provider, ProviderError
from src.report import markdown, save
from src.valuation import load_case


class FakeProvider:
    name = "test-double"
    model = "fixture"

    def __init__(self, fail=False, invalid=False):
        self.outputs = example(load_case())["roles"]
        self.calls = []
        self.fail = fail
        self.invalid = invalid

    async def complete(self, messages, schema):
        role = messages[0]["content"].splitlines()[0].split()[-1].rstrip(".")
        self.calls.append((role, messages))
        await asyncio.sleep(0)
        if self.fail and role == "risk":
            raise ProviderError("Model request timed out.")
        if self.invalid and role == "bull" and sum(r == "bull" for r, _ in self.calls) == 1:
            return Completion("not-json", self.model, {}, "stop")
        return Completion(json.dumps(self.outputs[role]["output"]), self.model, {"test_tokens": 10}, "stop")


def test_independent_fanout_then_chair_and_export(tmp_path):
    provider = FakeProvider()
    run = asyncio.run(convene(load_case(), provider))
    assert run["status"] == "complete"
    assert [r for r, _ in provider.calls] == ["bull", "bear", "risk", "chair"]
    assert len({m[1]["content"] for _, m in provider.calls[:3]}) == 1
    assert len({m[0]["content"] for _, m in provider.calls[:3]}) == 3
    payload = json.loads(provider.calls[3][1][1]["content"])
    assert set(payload["validated_specialists"]) == {"bull", "bear", "risk"}
    assert len(set(a["snapshot_sha256"] for a in run["roles"].values())) == 1
    output = save(run, tmp_path)
    assert json.loads(output.read_text(encoding="utf-8")) == run
    assert "SYNTHETIC DATA" in markdown(run)


def test_timeout_does_not_manufacture_a_verdict():
    provider = FakeProvider(fail=True)
    run = asyncio.run(convene(load_case(), provider))
    assert run["status"] == "incomplete"
    assert run["roles"]["risk"]["status"] == "failed"
    assert run["roles"]["chair"]["status"] == "skipped"
    assert "output" not in run["roles"]["chair"]
    assert len(provider.calls) == 3


def test_validation_failure_retries_once():
    provider = FakeProvider(invalid=True)
    run = asyncio.run(convene(load_case(), provider))
    assert run["status"] == "complete"
    assert len(run["roles"]["bull"]["attempts"]) == 2
    assert "error" in run["roles"]["bull"]["attempts"][0]


def test_no_foundry_credentials_does_not_disable_offline(monkeypatch):
    for k in ("FOUNDRY_BASE_URL", "FOUNDRY_MODEL", "FOUNDRY_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(ProviderError, match="Set Foundry"):
        Provider("foundry")
    assert example(load_case())["status"] == "illustration"


def test_local_provider_rejects_external_host_and_cloud_tag(monkeypatch):
    monkeypatch.setenv("OLLAMA_URL", "https://example.test")
    with pytest.raises(ProviderError, match="loopback"):
        Provider("ollama")
    monkeypatch.setenv("OLLAMA_URL", "http://127.0.0.1:11434")
    with pytest.raises(ProviderError, match="Cloud"):
        Provider("ollama", "test-cloud")


def test_foundry_adapter_contract_with_mock_transport(monkeypatch):
    monkeypatch.setenv("FOUNDRY_BASE_URL", "https://fixture.openai.azure.com/openai/v1")
    monkeypatch.setenv("FOUNDRY_MODEL", "fixture-deployment")
    monkeypatch.setenv("FOUNDRY_API_KEY", "mock-credential-not-a-real-key")
    def handler(request):
        assert request.url.path == "/openai/v1/chat/completions"
        assert request.headers["api-key"] == "mock-credential-not-a-real-key"
        payload = json.loads(request.content)
        assert payload["model"] == "fixture-deployment"
        assert payload["response_format"]["json_schema"]["strict"] is True
        return httpx.Response(200, json={"model": "fixture-model", "choices": [
            {"message": {"content": "{}"}, "finish_reason": "stop"}], "usage": {"total_tokens": 11}})
    provider = Provider("foundry", transport=httpx.MockTransport(handler))
    result = asyncio.run(provider.complete([{"role": "user", "content": "test"}], {"type": "object"}))
    assert result.text == "{}"
    assert result.usage == {"total_tokens": 11}

