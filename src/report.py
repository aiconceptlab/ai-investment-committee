"""Portable, explicitly labelled report and evidence export."""
import json
import os
from pathlib import Path
from .review import review_flags


def markdown(run):
    snap = run["snapshot"]
    ledger = snap["evidence_ledger"]
    case = snap["case"]
    rows = ["# AI Investment Committee", "",
            "**SYNTHETIC DATA · Educational research only. No investment advice.**", "",
            f"Case: {case['company_name']} ({run['case_id']})  ",
            f"Run: {run['run_id']}  ",
            f"Mode: {run['mode']} · Status: {run['status']}  ",
            f"Provider / deployment: {run['provider']} / {run['deployment']}  ",
            f"Snapshot SHA-256: {run['snapshot_sha256']}", "",
            "## Verified scenarios", "",
            "All amounts in EUR millions. Cash and debt are held constant.", "",
            "Equity = revenue × EV/sales + (cash − debt). Change = scenario equity / starting equity − 1.", "",
            "| Scenario | Revenue | EV / sales | Equity | Change |", "| --- | ---: | ---: | ---: | ---: |"]
    for name in ("bear", "base", "bull"):
        m = snap["metrics"]["scenarios"][name]
        rows.append(f"| {name.title()} | {m['revenue_eur_m']} | {m['multiple']}× | {m['equity_eur_m']} | {m['change_pct']}% |")
    rows.extend(["", "Hypothetical sensitivities; no probabilities, discounting, dilution or forecast.", ""])
    for role in ("bull", "bear", "risk", "chair"):
        item = run["roles"].get(role, {})
        rows.extend([f"## {role.title()} · {item.get('status', 'waiting')}", ""])
        output = item.get("output")
        if not output:
            rows.extend([item.get("reason", "No accepted output. Inspect the JSON audit."), ""])
            continue
        if role != "chair":
            rows.extend([output["thesis"], ""])
            for claim in output["claims"]:
                evidence = "; ".join(f"{i} = {ledger[i]['value']}" for i in claim["evidence_field_ids"])
                rows.extend([f"- {claim['statement']} — Evidence: {evidence}",
                             f"  - Assumptions: {'; '.join(claim['assumptions'])}",
                             f"  - Limits: {'; '.join(claim['limitations'])}"])
            for key in ("key_risks_or_catalysts", "open_questions", "disconfirming_tests"):
                rows.extend(["", f"**{key.replace('_', ' ').title()}**",
                             *[f"- {v}" for v in output[key]]])
        else:
            rows.extend([f"**{output['verdict'].replace('_', ' ')}** — {output['summary']}",
                         "", f"For: {output['strongest_bull_argument']}",
                         f"Against: {output['strongest_bear_argument']}", ""])
            for d in output["disagreements"]:
                rows.extend([f"### {d['topic']}", f"- Bull: {d['bull_view']}", f"- Bear: {d['bear_view']}",
                             f"- Risk: {d['risk_view']}", f"- Chair: {d['resolution']}",
                             f"- Evidence: {', '.join(d['evidence_field_ids'])}", ""])
            for key in ("material_risks", "agreements", "decision_conditions", "research_next_steps"):
                rows.extend([f"**{key.replace('_', ' ').title()}**", *[f"- {v}" for v in output[key]], ""])
        rows.append("")
    flags = review_flags(run)
    if flags:
        rows.extend(["## Needs evidence", "", "These model interpretations are review cues, not established facts.", ""])
        rows.extend(f"- **{f['role'].title()} / {f['field']}**: {f['excerpt']} — {f['reason']}" for f in flags)
        rows.append("")
    rows.extend(["## Evidence ledger", "", "| Field ID | Value | Provenance |", "| --- | ---: | --- |"])
    rows.extend(f"| {i} | {v['value']} | {v['source']} |" for i, v in ledger.items())
    rows.extend(["", "The JSON export contains response attempts, prompt hashes, timestamps and provider token counts.", ""])
    return "\n".join(rows)


def save(run, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    name = run["run_id"]
    for suffix, data in (("json", json.dumps(run, indent=2, ensure_ascii=False)), ("md", markdown(run))):
        final = folder / f"{name}.{suffix}"
        temp = final.with_suffix(f".{suffix}.tmp")
        temp.write_text(data, encoding="utf-8")
        os.replace(temp, final)
    return folder / f"{name}.json"

