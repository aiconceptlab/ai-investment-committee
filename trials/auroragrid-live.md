# AI Investment Committee

**SYNTHETIC DATA · Educational research only. No investment advice.**

Case: AuroraGrid AI (auroragrid-2026-synthetic-v1)  
Run: 7ea79f54-1167-455b-acde-7ef333f9c4f6  
Mode: live · Status: complete  
Provider / deployment: ollama / gemma4:e4b  
Snapshot SHA-256: dcb9178012e38603e857cce8fadf7b81a952fc778f5b71507a78a5e0f815726c

## Verified scenarios

All amounts in EUR millions. Cash and debt are held constant.

Equity = revenue × EV/sales + (cash − debt). Change = scenario equity / starting equity − 1.

| Scenario | Revenue | EV / sales | Equity | Change |
| --- | ---: | ---: | ---: | ---: |
| Bear | 96 | 4× | 439 | -54.0% |
| Base | 150 | 6× | 955 | 0.0% |
| Bull | 162 | 7.5× | 1270.0 | 33.0% |

Hypothetical sensitivities; no probabilities, discounting, dilution or forecast.

## Bull · complete

AuroraGrid AI's strong recurring revenue profile and high gross margins suggest significant untapped growth potential, justifying a premium valuation multiple.

- The high net revenue retention indicates strong product stickiness and customer satisfaction, underpinning continued revenue growth. — Evidence: net_revenue_retention_pct = 118
  - Assumptions: The current net revenue retention rate will persist across various market cycles.; Customer satisfaction remains high enough to support the observed retention rate.
  - Limits: This metric does not account for potential customer churn due to competitive pressures.; It assumes the revenue base is stable enough to support high retention figures.
- The robust gross margin suggests pricing power and operational efficiency, allowing for reinvestment into growth initiatives. — Evidence: gross_margin_pct = 72
  - Assumptions: The company can maintain its current cost structure as revenue scales.; Input costs will not rise disproportionately to revenue growth.
  - Limits: This margin is historical and may not reflect costs associated with accelerated growth.; It does not account for potential margin compression from increased competition.
- The high revenue growth rate points to successful market penetration and increasing demand for the company's solutions. — Evidence: revenue_growth_pct = 35
  - Assumptions: The current growth trajectory can be sustained through the near term.; Market demand for the company's offerings will continue to expand.
  - Limits: Rapid growth can strain operational capacity and lead to unforeseen costs.; The growth rate might decelerate as the company matures in its addressable market.

**Key Risks Or Catalysts**
- A catalyst could be the successful expansion into new, high-growth vertical markets.
- A key risk is the concentration of revenue with a single large customer.
- The negative annual free cash flow requires careful monitoring against growth expectations.

**Open Questions**
- What is the expected trajectory of the largest customer's spending?
- How will the company manage its negative free cash flow while funding aggressive growth?

**Disconfirming Tests**
- A significant decline in net revenue retention would signal deteriorating customer relationships.
- A sharp drop in the gross margin percentage would indicate pricing pressure or cost inflation.
- Failure to meet the projected revenue growth in the next reporting period would challenge the growth thesis.

## Bear · complete

The valuation is overly optimistic given the operational risks, suggesting the current multiple is unsustainable when considering negative free cash flow and customer dependency.

- The high valuation multiple is unjustified because the company is currently generating negative free cash flow, indicating immediate operational strain. — Evidence: annual_fcf_eur_m = -12
  - Assumptions: The market values future earnings potential over current cash flow generation.
  - Limits: This analysis does not account for potential future operational improvements that could reverse the negative free cash flow trend.
- Significant revenue concentration poses a material risk that could severely depress future revenue and thus the valuation multiple. — Evidence: largest_customer_share_pct = 31; customer_revenue_exposure_eur_m = 37.2
  - Assumptions: The largest customer relationship is not immune to competitive pressures or changes in customer strategy.
  - Limits: The magnitude of the customer concentration risk is difficult to quantify without knowing the customer's switching costs.
- The negative free cash flow, combined with the high sales multiple, suggests the market is pricing in unsustainable growth that is not yet supported by cash generation. — Evidence: annual_fcf_eur_m = -12; ev_sales_multiple = 7.5
  - Assumptions: A sustainable business model requires positive free cash flow to support high valuation multiples.
  - Limits: The current negative free cash flow might be due to one-time, non-recurring investments rather than core operational weakness.

**Key Risks Or Catalysts**
- A material loss of revenue from the largest customer could trigger a significant downward revision of the sales multiple.
- The inability to convert revenue growth into positive free cash flow suggests underlying operational inefficiencies that could depress valuation multiples.
- Any indication that the market will discount the current high sales multiple due to cyclical downturns or increased competition.

**Open Questions**
- What is the expected trajectory of free cash flow over the next few reporting periods?
- How resilient is the revenue stream from the largest customer to competitive pricing actions?

**Disconfirming Tests**
- If the company can demonstrate a clear path to positive free cash flow that supports the current sales multiple, the bearish thesis weakens.
- If the largest customer relationship is secured by long-term, non-cancellable contracts, the concentration risk is mitigated.
- If comparable companies with similar negative free cash flow are trading at higher multiples, the valuation objection may be flawed.

## Risk · complete

The downside risk assessment must focus on the structural vulnerabilities indicated by customer concentration and the negative free cash flow profile, rather than solely on the implied valuation multiple contraction.

- The company exhibits significant downside risk due to high revenue concentration with a single customer. — Evidence: largest_customer_share_pct = 31
  - Assumptions: The largest customer represents a non-diversifiable portion of the revenue base.; The customer relationship is not subject to immediate, unforeseen changes.
  - Limits: The evidence only provides the current share percentage and does not detail the contractual nature or duration of the relationship.
- The negative annual free cash flow suggests ongoing operational cash burn that must be covered by existing liquidity. — Evidence: annual_fcf_eur_m = -12; cash_eur_m = 80
  - Assumptions: The current cash balance is sufficient to cover the negative free cash flow for a defined period.; No significant, unrecorded capital expenditures are required in the near term.
  - Limits: The evidence does not provide a time horizon for the negative free cash flow or the required capital expenditure schedule.
- The implied valuation multiple contraction in the bear case suggests a significant reduction in market confidence in future earnings power. — Evidence: scenario_bear.multiple = 4; ev_sales_multiple = 7.5
  - Assumptions: The market's perception of the company's quality is directly correlated with the implied multiple contraction.; The multiple contraction is not due to a temporary, non-recurring market event.
  - Limits: The evidence only presents the resulting multiple and does not explain the underlying drivers of the market's change in sentiment.

**Key Risks Or Catalysts**
- The primary risk is the dependence on a single major customer, which could lead to immediate revenue instability.
- The negative free cash flow requires continuous monitoring against the available cash reserves.
- A sharp decline in the implied valuation multiple suggests a fundamental reassessment of the business's earning potential.

**Open Questions**
- What is the contractual termination notice period or minimum commitment required from the largest customer?
- What is the expected capital expenditure profile needed to sustain operations given the negative free cash flow?
- Are there any alternative revenue streams or product lines that could mitigate the concentration risk?

**Disconfirming Tests**
- Test the sensitivity of the net cash position to a reduction in the largest customer's spend by a defined amount.
- Model the cash burn against the current cash balance using a rolling forecast period.
- Analyze the gross margin stability by testing the impact of input cost increases on the gross margin percentage.

## Chair · complete

**FURTHER RESEARCH** — The specialists present conflicting views regarding the sustainability of the current valuation multiple, particularly concerning the negative free cash flow and high customer concentration. The disagreement centers on whether strong retention and growth metrics outweigh the immediate cash burn and single-customer dependency. Further analysis is required to reconcile these structural risks with the implied premium valuation.

For: The robust gross margin and high net revenue retention suggest strong product stickiness and pricing power, which should justify a premium valuation multiple despite current cash flow issues. (Evidence: net_revenue_retention_pct, gross_margin_pct)
Against: The combination of negative annual free cash flow and significant revenue concentration creates an unsustainable valuation profile, suggesting the current multiple is overly optimistic. (Evidence: annual_fcf_eur_m, largest_customer_share_pct)

### Valuation Justification (Cash Flow vs. Growth)
- Bull: High revenue growth and strong retention metrics justify a premium multiple, implying future cash flow will support the current valuation. (Evidence: revenue_growth_pct, net_revenue_retention_pct)
- Bear: Negative free cash flow indicates immediate operational strain, making the current high sales multiple unsustainable regardless of growth potential. (Evidence: annual_fcf_eur_m, ev_sales_multiple)
- Risk: The valuation multiple contraction in the bear case suggests a fundamental reassessment of earning power, linking multiple changes to structural vulnerabilities. (Evidence: scenario_bear.multiple, ev_sales_multiple)
- Chair: The disagreement hinges on whether the market discounts current negative cash flow or discounts future growth potential. (Evidence: annual_fcf_eur_m, scenario_bull.multiple)
- Evidence: annual_fcf_eur_m, ev_sales_multiple, revenue_growth_pct, scenario_bear.multiple

### Impact of Customer Concentration
- Bull: The high net revenue retention suggests the customer base is sticky enough to absorb potential shocks from any single customer. (Evidence: net_revenue_retention_pct)
- Bear: Significant revenue concentration poses a material risk that could severely depress future revenue and thus the valuation multiple. (Evidence: largest_customer_share_pct, customer_revenue_exposure_eur_m)
- Risk: The primary risk is the dependence on a single major customer, which could lead to immediate revenue instability. (Evidence: largest_customer_share_pct)
- Chair: The specialists disagree on the resilience of the revenue stream given the large single-customer exposure. (Evidence: largest_customer_share_pct)
- Evidence: largest_customer_share_pct, customer_revenue_exposure_eur_m, net_revenue_retention_pct

**Material Risks**
- The primary risk is the dependence on a single major customer, which could lead to immediate revenue instability. (Evidence: largest_customer_share_pct)
- The negative free cash flow requires continuous monitoring against the available cash reserves. (Evidence: annual_fcf_eur_m)
- The market's perception of the company's quality is directly correlated with the implied multiple contraction. (Evidence: scenario_bear.multiple)

**Agreements**
- All parties acknowledge the existence of significant structural risks related to customer concentration and negative free cash flow. (Evidence: largest_customer_share_pct, annual_fcf_eur_m)
- The valuation multiple is a key point of contention among the specialists. (Evidence: ev_sales_multiple, scenario_bear.multiple, scenario_bull.multiple)

**Decision Conditions**
- Confirmation of a clear, funded path to positive free cash flow would significantly weaken the bearish argument. (Evidence: annual_fcf_eur_m)
- Evidence of long-term, non-cancellable contracts mitigating the single-customer risk would strengthen the bull case. (Evidence: largest_customer_share_pct)
- A comparison of comparable companies with similar negative free cash flow but higher multiples would challenge the bear's valuation objection. (Evidence: scenario_bear.multiple)

**Research Next Steps**
- Determine the expected trajectory of free cash flow over the next few reporting periods. (Evidence: annual_fcf_eur_m)
- Quantify the contractual termination notice period or minimum commitment required from the largest customer. (Evidence: largest_customer_share_pct)
- Model the cash burn against the current cash balance using a rolling forecast period. (Evidence: annual_fcf_eur_m, cash_eur_m)


## Needs evidence

These model interpretations are review cues, not established facts.

- **Bull / claim 1**: The high net revenue retention indicates strong product stickiness and customer satisfaction, underpinning continued revenue growth. — The fixture does not establish product quality, customer satisfaction or competitive advantage.
- **Bull / claim 2**: The robust gross margin suggests pricing power and operational efficiency, allowing for reinvestment into growth initiatives. — The fixture does not establish product quality, customer satisfaction or competitive advantage.
- **Bull / claim 3**: The high revenue growth rate points to successful market penetration and increasing demand for the company's solutions. — The fixture does not establish product quality, customer satisfaction or competitive advantage.
- **Bear / claim 1**: The high valuation multiple is unjustified because the company is currently generating negative free cash flow, indicating immediate operational strain. — Cash flow alone does not establish financing needs or operating strain; funding and cost details are missing.
- **Bear / claim 3**: The negative free cash flow, combined with the high sales multiple, suggests the market is pricing in unsustainable growth that is not yet supported by cash generation. — Scenario multiples are supplied assumptions. The case has no observations of market behavior.
- **Risk / claim 3**: The implied valuation multiple contraction in the bear case suggests a significant reduction in market confidence in future earnings power. — Scenario multiples are supplied assumptions. The case has no observations of market behavior.
- **Chair / disagreement 1 / bear_view**: Negative free cash flow indicates immediate operational strain, making the current high sales multiple unsustainable regardless of growth potential. (Evidence: annual_fcf_eur_m, ev_sales_multiple) — Cash flow alone does not establish financing needs or operating strain; funding and cost details are missing.

## Evidence ledger

| Field ID | Value | Provenance |
| --- | ---: | --- |
| annual_fcf_eur_m | -12 | synthetic input |
| cash_eur_m | 80 | synthetic input |
| customer_revenue_exposure_eur_m | 37.2 | deterministic calculation |
| debt_eur_m | 25 | synthetic input |
| ev_sales_multiple | 7.5 | synthetic input |
| gross_margin_pct | 72 | synthetic input |
| largest_customer_share_pct | 31 | synthetic input |
| net_cash_eur_m | 55 | deterministic calculation |
| net_revenue_retention_pct | 118 | synthetic input |
| reference_equity_eur_m | 955.0 | deterministic calculation |
| reference_ev_eur_m | 900.0 | deterministic calculation |
| revenue_eur_m | 120 | synthetic input |
| revenue_growth_pct | 35 | synthetic input |
| scenario_base.change_pct | 0.0 | deterministic calculation |
| scenario_base.equity_eur_m | 955 | deterministic calculation |
| scenario_base.ev_eur_m | 900 | deterministic calculation |
| scenario_base.multiple | 6 | synthetic assumption |
| scenario_base.revenue_eur_m | 150 | synthetic assumption |
| scenario_bear.change_pct | -54.0 | deterministic calculation |
| scenario_bear.equity_eur_m | 439 | deterministic calculation |
| scenario_bear.ev_eur_m | 384 | deterministic calculation |
| scenario_bear.multiple | 4 | synthetic assumption |
| scenario_bear.revenue_eur_m | 96 | synthetic assumption |
| scenario_bull.change_pct | 33.0 | deterministic calculation |
| scenario_bull.equity_eur_m | 1270.0 | deterministic calculation |
| scenario_bull.ev_eur_m | 1215.0 | deterministic calculation |
| scenario_bull.multiple | 7.5 | synthetic assumption |
| scenario_bull.revenue_eur_m | 162 | synthetic assumption |

The JSON export contains response attempts, prompt hashes, timestamps and provider token counts.
