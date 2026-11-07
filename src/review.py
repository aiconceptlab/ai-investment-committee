"""Narrow review cues for qualitative leaps in this synthetic case."""
import re

CUES = (
    (re.compile(r"\b(?:pricing power|product stickiness|customer satisfaction|market penetration|switching costs)\b", re.I),
     "The fixture does not establish product quality, customer satisfaction or competitive advantage."),
    (re.compile(r"\b(?:market confidence|market perception|market is (?:already )?pricing|market.{0,12}sentiment)\b", re.I),
     "Scenario multiples are supplied assumptions. The case has no observations of market behavior."),
    (re.compile(r"\b(?:immediate operational strain|requires? (?:immediate|continuous|continued) (?:capital|external)|cash balance is insufficient)\b", re.I),
     "Cash flow alone does not establish financing needs or operating strain; funding and cost details are missing."),
)


def review_flags(run):
    flags = []
    for role, item in run["roles"].items():
        output = item.get("output")
        if not output:
            continue
        sections = [("thesis", output.get("thesis", output.get("summary", "")))]
        sections += [(f"claim {i}", c["statement"]) for i, c in enumerate(output.get("claims", []), 1)]
        for i, d in enumerate(output.get("disagreements", []), 1):
            sections += [(f"disagreement {i} / {k}", d[k]) for k in ("bull_view", "bear_view", "risk_view", "resolution")]
        for field, text in sections:
            for pattern, reason in CUES:
                if pattern.search(text):
                    flags.append({"role": role, "field": field, "excerpt": text, "reason": reason})
                    break
    return flags

