"""Pure Decimal valuation; all percentages are scenario changes, not probabilities."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from .schemas import Case

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "data" / "auroragrid_case.json"


def load_case(path=CASE_FILE):
    return Case.model_validate_json(Path(path).read_text(encoding="utf-8"))


def rounded(value):
    return value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def calculate(case):
    net_cash = case.cash_eur_m - case.debt_eur_m
    ev = case.revenue_eur_m * case.ev_sales_multiple
    equity = ev + net_cash
    if equity <= 0:
        raise ValueError("Starting equity must be positive to calculate a relative change.")
    rows = {}
    for name in ("bear", "base", "bull"):
        assumptions = getattr(case.scenario_assumptions, name)
        scenario_ev = assumptions.revenue_eur_m * assumptions.multiple
        scenario_equity = scenario_ev + net_cash
        rows[name] = {
            "revenue_eur_m": assumptions.revenue_eur_m,
            "multiple": assumptions.multiple,
            "ev_eur_m": scenario_ev,
            "equity_eur_m": scenario_equity,
            "change_pct": rounded((scenario_equity / equity - 1) * 100),
        }
    return {
        "net_cash_eur_m": net_cash,
        "reference_ev_eur_m": ev,
        "reference_equity_eur_m": equity,
        "customer_revenue_exposure_eur_m": rounded(
            case.revenue_eur_m * case.largest_customer_share_pct / 100
        ),
        "scenarios": rows,
    }


def evidence_ledger(case, metrics):
    ledger = {}
    for name, value in case.model_dump().items():
        if isinstance(value, Decimal):
            ledger[name] = {"value": str(value), "source": "synthetic input"}
    for name, value in metrics.items():
        if isinstance(value, Decimal):
            ledger[name] = {"value": str(value), "source": "deterministic calculation"}
    for role, row in metrics["scenarios"].items():
        for name, value in row.items():
            ledger[f"scenario_{role}.{name}"] = {
                "value": str(value),
                "source": "synthetic assumption" if name in ("revenue_eur_m", "multiple")
                else "deterministic calculation",
            }
    return ledger

