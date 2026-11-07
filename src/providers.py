"""Opt-in model providers. The default live provider stays on the local machine."""
import os
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

from .valuation import ROOT

load_dotenv(ROOT / ".env", override=False)


class ProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class Completion:
    text: str
    model: str
    usage: dict
    finish: str


def foundry_schema(node):
    if isinstance(node, dict):
        remove = {"minLength", "maxLength", "minItems", "maxItems", "title"}
        return {k: foundry_schema(v) for k, v in node.items() if k not in remove}
    if isinstance(node, list):
        return [foundry_schema(v) for v in node]
    return node


class Provider:
    def __init__(self, name, model=None, transport=None):
        self.name = name
        self.transport = transport
        self.timeout = min(300, max(5, int(os.getenv("MODEL_TIMEOUT_SECONDS", "150"))))
        if name == "ollama":
            self.model = model or os.getenv("OLLAMA_MODEL", "gemma4:e4b")
            base = urlparse(os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"))
            if (base.scheme != "http" or base.hostname not in ("localhost", "127.0.0.1", "::1")
                    or base.username or base.password or base.query or base.fragment or base.path not in ("", "/")):
                raise ProviderError("Ollama URL must be a plain loopback HTTP origin.")
            if "cloud" in self.model.casefold():
                raise ProviderError("Cloud model tags are not accepted in the local Ollama mode.")
            self.url = base.geturl().rstrip("/") + "/api/chat"
            self.headers = {}
        elif name == "foundry":
            self.model = model or os.getenv("FOUNDRY_MODEL", "")
            base = urlparse(os.getenv("FOUNDRY_BASE_URL", ""))
            key = os.getenv("FOUNDRY_API_KEY", "")
            valid_host = (base.hostname or "").endswith((".openai.azure.com", ".services.ai.azure.com"))
            if not (self.model and key and base.scheme == "https" and valid_host
                    and base.path.rstrip("/") == "/openai/v1" and not base.username
                    and not base.password and not base.query and not base.fragment):
                raise ProviderError("Set Foundry model, API key and an Azure /openai/v1 base URL.")
            self.url = base.geturl().rstrip("/") + "/chat/completions"
            self.headers = {"api-key": key}
        else:
            raise ProviderError("Choose ollama or foundry.")

    async def complete(self, messages, schema):
        if self.name == "ollama":
            payload = {"model": self.model, "messages": messages, "stream": False, "format": schema,
                       "think": False, "options": {"temperature": 0.15, "num_predict": 1800, "num_ctx": 8192}}
        else:
            payload = {"model": self.model, "messages": messages, "stream": False,
                       "max_completion_tokens": 2400,
                       "response_format": {"type": "json_schema", "json_schema": {
                           "name": "committee_response", "strict": True, "schema": foundry_schema(schema)}}}
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=False, trust_env=False,
                                         transport=self.transport) as client:
                response = await client.post(self.url, headers=self.headers, json=payload)
                if response.status_code != 200:
                    raise ProviderError(f"{self.name} returned HTTP {response.status_code}; check model and configuration.")
                data = response.json()
            if self.name == "ollama":
                if not data.get("done"):
                    raise ProviderError("Ollama returned an unfinished response.")
                return Completion(data["message"]["content"], data.get("model", self.model),
                                  {k: data[k] for k in ("prompt_eval_count", "eval_count") if k in data},
                                  data.get("done_reason", "unknown"))
            choice = data["choices"][0]
            if choice["message"].get("refusal"):
                raise ProviderError("Foundry returned a refusal.")
            return Completion(choice["message"]["content"], data.get("model", self.model),
                              data.get("usage") or {}, choice.get("finish_reason", "unknown"))
        except httpx.TimeoutException as exc:
            raise ProviderError("Model request timed out.") from exc
        except httpx.HTTPError as exc:
            raise ProviderError(f"Could not reach {self.name}.") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError("Provider returned an unexpected response envelope.") from exc

