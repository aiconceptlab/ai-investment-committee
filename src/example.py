"""Hand-authored baseline. It is never marked as a model run."""
import hashlib
import json

from .committee import canonical
from .guardrails import validate_response
from .valuation import calculate, evidence_ledger


def example(case):
    metrics = calculate(case)
    ledger = evidence_ledger(case, metrics)
    snap = json.loads(canonical({"case": case.model_dump(mode="json"), "metrics": metrics,
                                "evidence_ledger": ledger}))
    def claim(statement, evidence, assumption, limitation):
        return {"statement": statement, "evidence_field_ids": [evidence],
                "assumptions": [assumption], "limitations": [limitation]}
    def specialist(role, thesis, claims, drivers, questions, tests):
        return {"role": role, "thesis": thesis, "claims": claims, "key_risks_or_catalysts": [drivers],
                "open_questions": [questions], "disconfirming_tests": [tests]}
    outputs = {
        "bull": specialist("bull", "Growth and customer expansion support a conditional upside thesis.",
            [claim("Revenue growth gives the upside case a starting point.", "revenue_growth_pct",
                   "Recent demand persists.", "Historical growth does not establish future growth."),
             claim("Gross margin leaves room for an operating leverage thesis.", "gross_margin_pct",
                   "Incremental costs stay controlled.", "Operating cost detail is not provided."),
             claim("Retention suggests expansion within the existing customer base.", "net_revenue_retention_pct",
                   "Expansion is broadly distributed.", "Customer cohort detail is not provided.")],
            "Operating leverage is conditional; negative free cash flow and concentration remain material.",
            "Is retention durable across cohorts?", "Compare renewal and expansion by cohort."),
        "bear": specialist("bear", "The illustrative valuation depends on sustained growth and better cash conversion.",
            [claim("The reference multiple leaves the case sensitive to compression.", "ev_sales_multiple",
                   "Buyers could value growth less highly.", "Comparable companies are not provided."),
             claim("Negative free cash flow constrains the operating leverage thesis.", "annual_fcf_eur_m",
                   "Cash conversion does not improve quickly.", "The spending and cash flow bridge is not provided."),
             claim("Concentration makes the renewal of the largest customer important.", "largest_customer_share_pct",
                   "The contract is not readily replaceable.", "Contract terms are not provided.")],
            "A weaker renewal or multiple compression could challenge the thesis.",
            "What portion of spending is discretionary?", "Verify a credible cash conversion bridge."),
        "risk": specialist("risk", "Concentration and cash burn make downside sensitivity worth testing.",
            [claim("The bear sensitivity exposes the effect of lower revenue and multiple.", "scenario_bear.equity_eur_m",
                   "Cash and debt remain fixed.", "The sensitivity is not a forecast."),
             claim("Largest-customer revenue exposure is not an equity loss estimate.", "customer_revenue_exposure_eur_m",
                   "The exposure uses the supplied revenue share.", "Replacement demand and costs are not provided."),
             claim("Negative free cash flow merits a liquidity review.", "annual_fcf_eur_m",
                   "Cash conversion may vary with growth.", "Debt maturities and a cash flow bridge are not provided.")],
            "Contract concentration and liquidity need separate analysis.",
            "When do debt obligations and material renewals occur?", "Stress test renewal and funding schedules.")
    }
    outputs["chair"] = {
        "verdict": "FURTHER_RESEARCH", "summary": "The growth case is plausible, but durability and cash conversion remain unresolved.",
        "strongest_bull_argument": "Growth and expansion support a conditional operating leverage thesis.",
        "strongest_bear_argument": "The reference valuation is exposed to compression while free cash flow is negative.",
        "material_risks": ["Concentration and an unverified path to cash generation."],
        "agreements": ["The supplied historical growth is relevant and is not a forecast."],
        "disagreements": [
            {"topic": "Growth and valuation", "bull_view": "Expansion could support a premium.",
             "bear_view": "The reference multiple leaves little room for slower growth.",
             "risk_view": "The bear sensitivity shows the effect of simultaneous compression.",
             "resolution": "Compare retention cohorts and valuation comparables.",
             "evidence_field_ids": ["revenue_growth_pct", "ev_sales_multiple", "scenario_bear.equity_eur_m"]},
            {"topic": "Cash conversion", "bull_view": "Scaling could improve cash conversion.",
             "bear_view": "Negative free cash flow weakens the case for operating leverage.",
             "risk_view": "Liquidity and debt maturity evidence is not provided.",
             "resolution": "Obtain a cash flow bridge and maturity schedule.",
             "evidence_field_ids": ["annual_fcf_eur_m", "net_cash_eur_m"]}
        ],
        "decision_conditions": ["Reassess if cohort retention and cash conversion are supported by additional evidence."],
        "research_next_steps": ["Review customer contracts, cohort economics, the cash flow bridge and comparables."],
        "evidence_field_ids": ["revenue_growth_pct", "ev_sales_multiple", "annual_fcf_eur_m", "largest_customer_share_pct"]
    }
    return {"schema_version": 1, "synthetic": True, "mode": "offline_example", "provider": "none",
            "deployment": "not invoked", "run_id": "offline-illustration", "case_id": case.case_id,
            "snapshot_sha256": hashlib.sha256(canonical(snap).encode()).hexdigest(), "snapshot": snap,
            "roles": {role: {"role": role, "status": "example", "attempts": [],
                              "output": validate_response(role, json.dumps(out), ledger)}
                      for role, out in outputs.items()}, "status": "illustration"}

