"""Validated inputs and model responses. Case facts and interpretations stay separate."""
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Money = Annotated[Decimal, Field(ge=0, le=Decimal("1000000000"), allow_inf_nan=False)]
Percent = Annotated[Decimal, Field(ge=0, le=100, allow_inf_nan=False)]
Multiple = Annotated[Decimal, Field(ge=0, le=1000, allow_inf_nan=False)]
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=650)]
EvidenceIDs = Annotated[list[str], Field(min_length=1, max_length=8)]
Notes = Annotated[list[Text], Field(min_length=1, max_length=4)]
Role = Literal["bull", "bear", "risk"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Scenario(StrictModel):
    revenue_eur_m: Money
    multiple: Multiple


class Scenarios(StrictModel):
    bear: Scenario
    base: Scenario
    bull: Scenario


class Case(StrictModel):
    case_id: Literal["auroragrid-2026-synthetic-v1"]
    company_name: Literal["AuroraGrid AI"]
    synthetic: Literal[True]
    currency: Literal["EUR"]
    unit: Literal["millions"]
    revenue_eur_m: Money
    revenue_growth_pct: Annotated[Decimal, Field(ge=-100, le=10000, allow_inf_nan=False)]
    gross_margin_pct: Annotated[Decimal, Field(ge=-1000, le=100, allow_inf_nan=False)]
    net_revenue_retention_pct: Annotated[Decimal, Field(ge=0, le=1000, allow_inf_nan=False)]
    annual_fcf_eur_m: Annotated[Decimal, Field(ge=-1000000000, le=1000000000, allow_inf_nan=False)]
    ev_sales_multiple: Multiple
    cash_eur_m: Money
    debt_eur_m: Money
    largest_customer_share_pct: Percent
    scenario_assumptions: Scenarios


class Claim(StrictModel):
    statement: Text
    evidence_field_ids: EvidenceIDs
    assumptions: Notes
    limitations: Notes


class Specialist(StrictModel):
    role: Role
    thesis: Text
    claims: Annotated[list[Claim], Field(min_length=3, max_length=3)]
    key_risks_or_catalysts: Notes
    open_questions: Notes
    disconfirming_tests: Notes


class Disagreement(StrictModel):
    topic: Text
    bull_view: Text
    bear_view: Text
    risk_view: Text
    resolution: Text
    evidence_field_ids: EvidenceIDs


class Chair(StrictModel):
    verdict: Literal["FURTHER_RESEARCH", "WATCHLIST", "AVOID"]
    summary: Text
    strongest_bull_argument: Text
    strongest_bear_argument: Text
    material_risks: Notes
    agreements: Notes
    disagreements: Annotated[list[Disagreement], Field(min_length=2, max_length=4)]
    decision_conditions: Notes
    research_next_steps: Notes
    evidence_field_ids: EvidenceIDs

