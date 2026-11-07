"""Run the real trial without opening the UI."""
import argparse
import asyncio
from pathlib import Path

from .committee import convene
from .providers import Provider, ProviderError
from .report import save
from .valuation import load_case

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--provider", choices=("ollama", "foundry"), default="ollama")
    p.add_argument("--model")
    p.add_argument("--out", type=Path, default=Path("runs"))
    args = p.parse_args()
    try:
        provider = Provider(args.provider, args.model)
    except ProviderError as exc:
        p.exit(2, str(exc) + "\n")
    run = asyncio.run(convene(load_case(), provider, lambda role, status: print(f"{role}: {status}", flush=True)))
    print(f"{run['status']}: {save(run, args.out)}", flush=True)
    raise SystemExit(0 if run["status"] == "complete" else 1)

if __name__ == "__main__":
    main()

