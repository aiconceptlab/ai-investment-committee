# LAB // 001 — AI Investment Committee

**Four model roles. One fictional company. A verdict you can audit.**

A Streamlit research demo. Bull, Bear and Risk independently evaluate the same immutable AuroraGrid AI case. The Chair reads their validated submissions and the verified scenario calculations, then explains the disagreements and issues a conditional educational verdict.

**Synthetic data only.** No real securities, live quotes, broker access, trade instructions, personal portfolios or investment advice.

## Start without a model or API key

Requires Python **3.12**. From a fresh clone:

~~~sh
git clone https://github.com/aiconceptlab/lab-001-ai-investment-committee.git
cd lab-001-ai-investment-committee
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
~~~

Open **http://127.0.0.1:8504**. The default is a replay of the recorded live Ollama trial. Open **Committee & verdict** for the roles and disagreements, or **Audit & downloads** for raw responses and JSON/Markdown downloads. **Offline illustration** is separately labelled, hand-authored and makes no model calls.

- [Recorded live audit](trials/auroragrid-live.json)
- [Recorded live report](trials/auroragrid-live.md)
- [Build, test evidence and limitations](BUILD.md)
- [Eight Instagram slides and caption](marketing/README.md)

## Run the four roles locally

1. Install [Ollama](https://ollama.com/) and start the local service on port 11434.
2. Install a local model: **ollama pull gemma4:e4b**. The recorded trial used this model. Model downloads and hardware requirements vary.
3. Select **Live local Ollama**, then **Convene Committee**. Progress is visible. The three specialist requests are dispatched concurrently; the service may queue them.
4. Download the resulting audit. By default new runs are saved under the ignored **runs/** directory.

For a CLI trial:

~~~sh
python -m src.trial --provider ollama --model gemma4:e4b
~~~

The offline example and replay require neither Ollama nor a network after installing dependencies. No paid API is used in the recorded run. A different local model can be selected through **OLLAMA_MODEL** in **.env** or the CLI model flag. Outputs can differ across calls.

## Optional Microsoft Foundry

The source includes an opt-in adapter for a compatible **chat completions deployment with structured outputs** on Microsoft Foundry. Copy **.env.example** to **.env** and set:

- **FOUNDRY_BASE_URL**: Azure resource URL ending in **/openai/v1** (not the project API URL).
- **FOUNDRY_MODEL**: model deployment name.
- **FOUNDRY_API_KEY**: resource API key, server-side only.

Choose **Live Microsoft Foundry**, acknowledge use of your configured deployment, then convene. A hosted call can consume your Azure quota. No cloud credentials or billing are needed to replay the included run. The Foundry request contract was tested with a mock transport; no Azure deployment was available for a real trial. The live evidence in this release is from local Ollama.

See [Microsoft Foundry v1](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle), [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) and [Streamlit documentation](https://docs.streamlit.io/).

## Verified calculator

All amounts are EUR millions. Reference EV is **€900M**, net cash **€55M**, and illustrative starting equity **€955M**.

| Scenario | Revenue | EV / sales | Equity | Change vs start |
| --- | ---: | ---: | ---: | ---: |
| Bear | 96 | 4.0× | 439 | −54.0% |
| Base | 150 | 6.0× | 955 | 0.0% |
| Bull | 162 | 7.5× | 1,270 | +33.0% |

Equity = Revenue × EV/Sales + (Cash − Debt). Change = Scenario Equity / Starting Equity − 1. Cash and debt are frozen. These are sensitivity cases, not forecasts, probabilities or target share prices. Largest-customer revenue exposure is **€37.2M**; it does not imply an equivalent equity loss.

Python uses Decimal. Model prose does not supply numeric values to the chart. A ledger maps accepted evidence IDs to source inputs or calculated fields. The model can still draw unsupported qualitative inferences, so the UI flags selected review cues and leaves raw responses available.

## Test and reproduce

~~~sh
python -m pytest -q
python -m compileall -q app.py src tests
~~~

The app binds to loopback by default; this release is a local POC, not a public multi-user service. No attachment, credentials or local run logs are included in the source. The one shared trial is expressly synthetic and contains the actual model outputs.

