"""Streamlit interface for the synthetic committee lab."""
import asyncio
import hashlib
import json
import os

import pandas as pd
import streamlit as st

from src.committee import convene, canonical
from src.example import example
from src.guardrails import validate_response
from src.providers import Provider, ProviderError
from src.report import markdown, save
from src.review import review_flags
from src.valuation import ROOT, calculate, evidence_ledger, load_case

st.set_page_config(page_title="AI Investment Committee | AI Concept Lab", page_icon="◈", layout="wide")
st.html("""
<style>
.block-container {max-width:1330px;padding-top:2.2rem;padding-bottom:4rem}
div[data-testid="stMetric"]{background:#19212a;border:1px solid #353a40;border-radius:14px;padding:14px 18px}
.lab-tag{font-size:12px;letter-spacing:.17em;color:#d6b777;font-weight:700}
.lab-hero{background:radial-gradient(ellipse at top right,#413727 0,#19212a 42%,#131a21 75%);border:1px solid #4b4436;border-radius:20px;padding:32px 34px;margin-bottom:18px}
.lab-hero h1{font-size:clamp(32px,4vw,57px);font-weight:730;letter-spacing:-.045em;line-height:1.12;margin:12px 0;color:#f0ece0}
.lab-hero p{max-width:760px;color:#bfc6cb;margin:0;line-height:1.6}
.lab-synthetic{display:inline-block;background:#393225;color:#f1ce84;border:1px solid #6c5831;border-radius:6px;padding:5px 9px;margin-top:15px;font-size:11px;letter-spacing:.08em;font-weight:750}
[data-testid="stHorizontalBlock"]{gap:.85rem}
</style>
<div class="lab-hero"><div class="lab-tag">AI CONCEPT LAB &nbsp; // &nbsp; RESEARCH</div>
<h1>AI Investment Committee</h1><p>Four model roles. One fictional company. A verdict with evidence you can inspect.</p>
<div class="lab-synthetic">SYNTHETIC DATA · EDUCATIONAL RESEARCH</div></div>
""")

try:
    case = load_case()
    metrics = calculate(case)
except (ValueError, OSError) as exc:
    st.error("The synthetic case cannot be valued: " + str(exc))
    st.stop()

ledger = evidence_ledger(case, metrics)
trail = ROOT / "trials" / "auroragrid-live.json"


def replay(path):
    run = json.loads(path.read_text(encoding="utf-8"))
    if run["mode"] != "live" or run["status"] != "complete" or run["synthetic"] is not True:
        raise ValueError("Recorded trial is not a completed synthetic model run.")
    if run["snapshot_sha256"] != hashlib.sha256(canonical(run["snapshot"]).encode()).hexdigest():
        raise ValueError("Snapshot hash mismatch.")
    expected = {"case": case.model_dump(mode="json"), "metrics": metrics, "evidence_ledger": ledger}
    if canonical(run["snapshot"]) != canonical(expected):
        raise ValueError("Recorded trial uses a different fixture or calculator.")
    for role in ("bull", "bear", "risk", "chair"):
        item = run["roles"][role]
        actual = validate_response(role, item["attempts"][-1]["raw_response"], ledger)
        if item["status"] != "complete" or actual != item["output"] or item["snapshot_sha256"] != run["snapshot_sha256"]:
            raise ValueError("Recorded response does not match the validated output.")
    hashes = {r: hashlib.sha256(canonical(run["roles"][r]["output"]).encode()).hexdigest()
              for r in ("bull", "bear", "risk")}
    if hashes != run["roles"]["chair"]["chair_input_role_hashes"]:
        raise ValueError("Recorded Chair inputs do not match the specialists.")
    return run


recorded = None
if trail.exists():
    try:
        recorded = replay(trail)
    except (ValueError, OSError, KeyError, IndexError):
        st.warning("The saved trial could not be verified. The offline example is still available.")

control, details = st.columns([1, 2])
with control:
    st.selectbox("Investment case", ["AuroraGrid AI · synthetic"])
    options = (["Replay recorded live trial"] if recorded else []) + [
        "Offline illustration", "Live local Ollama", "Live Microsoft Foundry"]
    choice = st.selectbox("Execution mode", options, help="Replay and offline illustration never call a model.")
    live = choice.startswith("Live")
    foundry = choice.endswith("Foundry")
    allowed = st.checkbox("Use my configured Foundry deployment for this run") if foundry else True
    start = st.button("Convene Committee", type="primary", width="stretch", disabled=not allowed) if live else False
with details:
    st.subheader("AuroraGrid AI")
    st.caption("Fictional enterprise energy-optimization SaaS · all monetary amounts in EUR millions.")
    a, b, c, d = st.columns(4)
    a.metric("Revenue", f"€{case.revenue_eur_m:g}M")
    b.metric("YoY growth", f"{case.revenue_growth_pct:g}%")
    c.metric("Annual FCF", ("−" if case.annual_fcf_eur_m < 0 else "") + f"€{abs(case.annual_fcf_eur_m):g}M")
    d.metric("Starting equity", f"€{metrics['reference_equity_eur_m']:.0f}M")

if start and live:
    st.session_state.pop("live_result", None)
    st.session_state["live_choice"] = choice
    status = st.status("Convene Committee · SYNTHETIC DATA", expanded=True)
    states = {r: "waiting" for r in ("bull", "bear", "risk", "chair")}
    line = status.empty()

    def progress(role, phase):
        states[role] = phase
        line.caption(" · ".join(f"{r.title()}: {s}" for r, s in states.items()))
    try:
        provider = Provider("foundry" if foundry else "ollama")
        run = asyncio.run(convene(case, provider, progress))
        st.session_state["live_result"] = run
        status.update(label=f"Committee {run['status']} · SYNTHETIC DATA",
                      state="complete" if run["status"] == "complete" else "error", expanded=False)
        if os.getenv("SAVE_RUN_OUTPUT", "true").lower() == "true":
            try:
                save(run, ROOT / "runs")
            except OSError:
                st.warning("The local audit file could not be saved. Downloads remain available.")
    except (ProviderError, ValueError) as exc:
        status.update(label="Model configuration unavailable", state="error", expanded=True)
        status.write(str(exc))

if choice.startswith("Replay"):
    run = recorded
    st.info(f"Recorded live {recorded['provider']} trial. Replaying the logged output; no model request was made for this view.")
elif not live:
    run = example(case)
    st.info("Hand-authored offline illustration. No agents were invoked.")
else:
    run = st.session_state.get("live_result") if st.session_state.get("live_choice") == choice else None
    if run is None:
        st.caption("Press Convene Committee to make separate specialist calls, then run the Chair if all three pass.")

def plain(value):
    # Escape model prose as plain text in Markdown; never allow model HTML or links.
    escaped = str(value).replace("\\", "\\\\")
    for mark in ("*", "_", "[", "]", "<", ">", "\u0060", "#", "|"):
        escaped = escaped.replace(mark, "\\" + mark)
    st.markdown(escaped)

def items(label, values):
    st.markdown("**" + label + "**")
    for value in values:
        plain("• " + value)

def refs(ids, source):
    st.dataframe([{"Evidence field": i, **source[i]} for i in ids],
                 hide_index=True, width="stretch")

tab_case, tab_committee, tab_audit = st.tabs(["Case & scenarios", "Committee & verdict", "Audit & downloads"])
with tab_case:
    st.markdown("### Deterministic scenario valuation")
    st.caption("SYNTHETIC DATA · Equity = Revenue × EV/Sales + (Cash − Debt). Cash and debt are frozen.")
    scenarios = [{"Scenario": name.title(), "Revenue €M": float(row["revenue_eur_m"]),
                  "EV / sales": float(row["multiple"]), "Equity €M": float(row["equity_eur_m"]),
                  "Change vs start": f"{row['change_pct']:+.1f}%"} for name, row in metrics["scenarios"].items()]
    chart, table = st.columns([1, 1.2])
    with chart:
        st.bar_chart(pd.DataFrame(scenarios), x="Scenario", y="Equity €M", color="#d6b777",
                     height=265, horizontal=True)
    with table:
        st.dataframe(scenarios, hide_index=True, width="stretch")
        st.write(f"Reference EV **€{metrics['reference_ev_eur_m']:.0f}M** · Net cash **€{metrics['net_cash_eur_m']:.0f}M**")
        st.caption("Change = scenario equity / starting equity − 1. Sensitivities, not forecasts; no probabilities, dilution, financing effects or target price.")
    with st.expander("Raw case facts and calculation ledger"):
        refs(list(ledger), ledger)
        st.json(case.model_dump(mode="json"))

with tab_committee:
    st.caption("SYNTHETIC DATA · The same model can be prompted into different roles. It is not four independent sources.")
    roles = (("bull", "Bull", "Growth & upside"), ("bear", "Bear", "Valuation & downside"),
             ("risk", "Risk", "Exposure & missing evidence"), ("chair", "Chair", "Decision & conditions"))
    cols = st.columns(4)
    for col, (role, name, mandate) in zip(cols, roles):
        item = (run or {}).get("roles", {}).get(role, {})
        output = item.get("output")
        with col.container(border=True):
            st.markdown(f"**{name}**")
            st.caption(f"{mandate} · {item.get('status', 'waiting').upper()}")
            if output:
                plain(output.get("thesis", output.get("summary")))
            elif item.get("status") in ("failed", "skipped"):
                st.warning(item.get("reason", "No validated output. See audit."))
    if run:
        flags = review_flags(run)
        if flags:
            with st.expander(f"Needs evidence · {len(flags)} qualitative review cues"):
                st.caption("These interpretations go beyond what the fixture can establish.")
                for flag in flags:
                    plain(f"{flag['role'].title()} / {flag['field']}: {flag['excerpt']}")
                    st.caption(flag["reason"])
        for role, name, _ in roles[:3]:
            output = run["roles"][role].get("output")
            if not output:
                continue
            with st.expander(name + " · claims and evidence"):
                for claim in output["claims"]:
                    plain(claim["statement"])
                    refs(claim["evidence_field_ids"], ledger)
                    items("Assumptions", claim["assumptions"])
                    items("Limitations", claim["limitations"])
                items("Risks or catalysts", output["key_risks_or_catalysts"])
                items("Open questions", output["open_questions"])
                items("Disconfirming tests", output["disconfirming_tests"])
        chair = run["roles"]["chair"].get("output")
        if chair:
            st.markdown("### " + chair["verdict"].replace("_", " ").title())
            st.caption("Educational verdict · " + ("illustrative" if run["mode"] == "offline_example" else "model generated"))
            plain(chair["summary"])
            items("Strongest case for", [chair["strongest_bull_argument"]])
            items("Strongest case against", [chair["strongest_bear_argument"]])
            for dispute in chair["disagreements"]:
                with st.container(border=True):
                    plain(dispute["topic"])
                    for key, title in (("bull_view", "Bull"), ("bear_view", "Bear"),
                                       ("risk_view", "Risk"), ("resolution", "Chair")):
                        plain(f"{title}: {dispute[key]}")
                    refs(dispute["evidence_field_ids"], ledger)
            items("Agreements", chair["agreements"])
            items("Material risks", chair["material_risks"])
            items("Conditions that change the verdict", chair["decision_conditions"])
            items("Research checklist", chair["research_next_steps"])
        else:
            st.error("Incomplete committee. No verdict was generated.")

with tab_audit:
    st.caption("SYNTHETIC DATA · Schema and citation checks do not prove the truth of qualitative inferences.")
    if run:
        st.write(f"Run ID: **{run['run_id']}** · Provider: **{run['provider']}** · Model: **{run['deployment']}**")
        st.code(run["snapshot_sha256"], language=None)
        for role, record in run["roles"].items():
            with st.expander(f"{role.title()} · View raw agent response"):
                if not record.get("attempts"):
                    st.caption("No model request in this role record.")
                for attempt in record.get("attempts", []):
                    st.json({k: v for k, v in attempt.items() if k != "raw_response"})
                    if "error" in attempt:
                        st.warning("Needs evidence / validation failure: " + attempt["error"])
                    if "raw_response" in attempt:
                        st.code(attempt["raw_response"], language="json")
                if record.get("prompt_sha256"):
                    st.caption("Prompt SHA-256")
                    st.code(record["prompt_sha256"], language=None)
        left, right = st.columns(2)
        left.download_button("Download Markdown report", markdown(run), "committee-report.md", "text/markdown")
        right.download_button("Download JSON audit", json.dumps(run, indent=2, ensure_ascii=False),
                              "committee-audit.json", "application/json")
    else:
        st.caption("Load an illustration or run the committee to export an audit.")
st.caption("AI Concept Lab · Fictional case, educational research only · No trading, live prices or personal recommendations.")

