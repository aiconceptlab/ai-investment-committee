"""Mechanical checks, not a proof of semantic truth."""
import re

from .schemas import Chair, Specialist

NUMERALS = re.compile(r"[\d%€$£]|(?:\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b[\w -]{0,25}\b(?:percent|per cent|million|billion|euros|times)\b)", re.I)
ADVICE = re.compile(r"\b(?:buy now|sell now|buy shares|sell shares|you should (?:buy|sell|invest)|allocate your|place (?:an?|the) order|probability of)\b", re.I)
FCF_CONTRADICTION = re.compile(r"\b(?:free cash flow|fcf)\s+(?:is|remains|was)\s+(?:(?:currently|already)\s+)?(?:positive|not negative)\b|\b(?:currently|already)\s+(?:generates?|reports?|has)\s+positive\s+(?:annual\s+)?(?:free cash flow|fcf)\b", re.I)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in ("evidence_field_ids", "role", "verdict"):
                yield from strings(item)


def validate_response(role, raw, ledger):
    result = (Chair if role == "chair" else Specialist).model_validate_json(raw)
    if isinstance(result, Specialist):
        if result.role != role:
            raise ValueError("Output role does not match the requested specialist.")
        claims = result.claims
        if len({c.statement.casefold() for c in claims}) != 3:
            raise ValueError("Claims must be distinct.")
        ids = [i for c in claims for i in c.evidence_field_ids]
    else:
        if len({d.topic.casefold() for d in result.disagreements}) != len(result.disagreements):
            raise ValueError("Disagreement topics must be distinct.")
        if any(d.bull_view.casefold() == d.bear_view.casefold() for d in result.disagreements):
            raise ValueError("Disagreements must represent differing perspectives.")
        ids = result.evidence_field_ids + [i for d in result.disagreements for i in d.evidence_field_ids]
    unknown = sorted(set(ids) - set(ledger))
    if unknown:
        raise ValueError("Unknown evidence IDs: " + ", ".join(unknown)[:240])
    for prose in strings(result.model_dump()):
        if NUMERALS.search(prose):
            raise ValueError("Numerical narrative is unsupported. Cite field IDs instead; code renders all values.")
        if ADVICE.search(prose):
            raise ValueError("Trade instructions and unsupported probabilities are prohibited.")
        if ledger["annual_fcf_eur_m"]["value"].startswith("-") and FCF_CONTRADICTION.search(prose):
            raise ValueError("Inconsistent with the source: annual free cash flow is negative.")
    return result.model_dump(mode="json")

