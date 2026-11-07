# Build and evidence record

## Execution

Validated Case JSON → Decimal calculation and evidence ledger → independent Bull/Bear/Risk requests → validated submissions → sequential Chair → report and audit.

This implementation uses Python asyncio fan-out, a permitted alternative to Microsoft Agent Framework in the brief. One model serves all four roles. Distinct system prompts share the exact same canonical specialist input. The Chair receives the source snapshot plus all validated submissions. A single run ID, snapshot SHA-256, role prompt hashes, timestamps, attempt durations, response envelopes, raw response text and provider token counts are retained when available. Chair input hashes link the outputs it received to the specialist records.

Inputs and outputs are Pydantic validated. Unknown evidence references, numerical narrative and obvious conflicting present-tense positive-FCF claims are rejected. Schema or validation failures get one repair attempt. Transport errors stop that role. If a specialist fails, Chair is skipped and the result is explicitly incomplete. No fabricated substitute is inserted. Offline illustration cannot masquerade as a model run.

Qualitative “Needs evidence” cues are narrow heuristics, not semantic fact-checking. For example, retention alone does not prove switching costs or customer satisfaction, and a supplied multiple assumption does not show actual market sentiment. The saved trial preserves those model interpretations unchanged and the report annotates selected leaps separately. Readers should inspect citations and unknowns. There is no second-round rebuttal; the Chair synthesizes independently produced submissions.

## Live trial

7 November 2026 · Local Ollama · Gemma 4 e4b.

- Case: auroragrid-2026-synthetic-v1.
- Recorded run: **7ea79f54-1167-455b-acde-7ef333f9c4f6**.
- Four actual model calls, all accepted on their first attempt in this run.
- Three specialist submissions and the Chair validated; **Further Research** was the actual educational verdict.
- Chair recorded disagreements about valuation versus cash flow/growth and about customer concentration.
- A separate live run through the Streamlit **Convene Committee** button also completed. Slide 04 shows the real progress of that browser run; slides 05–07 use the primary recorded CLI run. No timings, reach, confidence or performance claims are fabricated.

An earlier live run was incomplete because a cash-flow rule incorrectly matched hypothetical questions about positive FCF. The rule was narrowed to factual present-state contradictions, and regression tests cover both cases. The failed run was retained locally but is not represented as a successful trial.

## Acceptance and validation

- **30 automated checks**: expected Decimal values, required debt, unit/currency validation, invalid ranges, extra/injected fields, numerical hallucination, evidence IDs, false positive/negative FCF cases, role schema, disagreement count, independence, Chair sequencing, timeout, one validation retry, provider configuration, Foundry mocked contract, and Streamlit modes.
- Browser checked desktop and 390px width, recorded replay, real verdict, audit download, and real live execution. All page checks passed.
- Foundry is implemented but only mock-tested here. No Entra authentication or Microsoft Agent Framework deployment is claimed.
- All eight Instagram images are **1080×1350**. The cover is labelled concept artwork. The other visuals use actual app evidence or deterministic chart drawing.
- The original DOCX, any private .env file, local logs and virtual environments are excluded from release assets.

## Model limits

The fixture is one fictional SaaS company; company identifier, units and synthetic flag are fixed. No user uploads, browsing, RAG, external filings, live market inputs, trading actions or personal financial data. No probabilities, discounting, dilution, financing effects or duration/runway claims. Role diversity does not imply independent models or verified expert opinions.

