import json

import pytest
from pydantic import ValidationError

from src.example import example
from src.guardrails import validate_response
from src.valuation import calculate, evidence_ledger, load_case


def setup():
    case = load_case()
    return example(case), evidence_ledger(case, calculate(case))


@pytest.mark.parametrize("text,match", [
    ("The margin is 90%.", "Numerical narrative"),
    ("The margin is ninety percent.", "Numerical narrative"),
    ("The free cash flow is currently positive.", "negative"),
    ("The company currently generates positive free cash flow.", "negative"),
    ("You should buy shares now.", "Trade instructions"),
])
def test_bad_model_claims_are_rejected(text, match):
    run, ledger = setup()
    data = run["roles"]["bull"]["output"]
    data["claims"][0]["statement"] = text
    with pytest.raises(ValueError, match=match):
        validate_response("bull", json.dumps(data), ledger)


def test_future_positive_fcf_question_is_not_a_contradiction():
    run, ledger = setup()
    data = run["roles"]["bull"]["output"]
    data["open_questions"] = ["What would it take to achieve positive free cash flow?"]
    assert validate_response("bull", json.dumps(data), ledger) == data


def test_fake_evidence_ids_are_rejected():
    run, ledger = setup()
    data = run["roles"]["risk"]["output"]
    data["claims"][0]["evidence_field_ids"] = ["made_up_margin"]
    with pytest.raises(ValueError, match="Unknown evidence IDs"):
        validate_response("risk", json.dumps(data), ledger)


def test_wrong_role_and_missing_disagreement():
    run, ledger = setup()
    with pytest.raises(ValueError, match="role does not match"):
        validate_response("bear", json.dumps(run["roles"]["bull"]["output"]), ledger)
    chair = run["roles"]["chair"]["output"]
    chair["disagreements"].pop()
    with pytest.raises(ValidationError):
        validate_response("chair", json.dumps(chair), ledger)


def test_offline_example_cannot_be_confused_with_a_live_run():
    run, _ = setup()
    assert run["mode"] == "offline_example"
    assert run["provider"] == "none"
    assert all(not r["attempts"] for r in run["roles"].values())

