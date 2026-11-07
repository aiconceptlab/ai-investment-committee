"""Render eight Instagram slides from the audited trial and actual UI screenshots."""
import json
from decimal import Decimal
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "marketing"
OUT = M / "instagram-4x5"
OUT.mkdir(parents=True, exist_ok=True)
RUN = json.loads((ROOT / "trials" / "auroragrid-live.json").read_text(encoding="utf-8"))
assert RUN["mode"] == "live" and RUN["status"] == "complete"
C = {"bg": "#111920", "ink": "#f5f0e2", "muted": "#afbac2", "gold": "#e0bf7e",
     "line": "#495055", "card": "#202b35", "bull": "#90cfb8", "bear": "#df9e95"}
W, H = 1080, 1350
SLIDES = []


def font(size, bold=False):
    candidates = (
        ("C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf") if bold
        else ("C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf")
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    raise RuntimeError("Install Arial or DejaVu Sans to render the carousel.")


def frame(index):
    im = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(im)
    put(d, (72, 60), "AI CONCEPT LAB", 23, "ink", True)
    put(d, (835, 60), "LAB // 001", 23, "gold", True)
    d.line((72, 107, 1008, 107), fill=C["line"])
    d.line((72, 1242, 1008, 1242), fill=C["line"])
    put(d, (72, 1269), "AI INVESTMENT COMMITTEE  /  SYNTHETIC CASE", 17, "muted")
    put(d, (912, 1266), f"{index:02} / 08", 22, "ink", True)
    return im, d


def put(d, xy, text, size=28, color="ink", bold=False):
    f = font(size, bold)
    if xy[0] + d.textlength(text, font=f) > 1009:
        raise ValueError(f"Text overflow: {text}")
    d.text(xy, text, font=f, fill=C.get(color, color))


def para(d, xy, text, size=28, color="ink", bold=False, width=845, limit=4):
    f = font(size, bold)
    lines, line = [], ""
    for word in text.split():
        candidate = (line + " " + word).strip()
        if d.textlength(candidate, font=f) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    if len(lines) > limit:
        raise ValueError(f"Too many lines: {text}")
    for i, line in enumerate(lines):
        put(d, (xy[0], xy[1] + i * (size + 9)), line, size, color, bold)


def heading(d, first, second, size=80):
    put(d, (72, 172), first, size, "ink", True)
    put(d, (72, 172 + size + 15), second, size, "ink", True)


def card(d, y, h, fill="card"):
    d.rounded_rectangle((72, y, 1008, y + h), radius=17, fill=C.get(fill, fill))


def keep(name, im):
    path = OUT / (name + ".png")
    im.save(path)
    SLIDES.append(im)


def short_quote(text, words):
    parts = text.split()
    return "“" + " ".join(parts[:words]).rstrip(",.;") + ("…”" if len(parts) > words else "”")


im, d = frame(1)
photo = ImageOps.fit(Image.open(M / "cover-photo.png").convert("RGB"), (W, H))
im.paste(photo.crop((0, 108, W, 1241)), (0, 108))
shade = Image.new("RGBA", (W, 560))
sd = ImageDraw.Draw(shade)
for y in range(560):
    sd.line((0, y, W, y), fill=(17, 25, 32, int(247 * (1 - y / 560))))
im.paste(shade, (0, 108), shade)
heading(d, "I built an AI", "investment committee.", 78)
put(d, (72, 387), "BULL. BEAR. RISK. CHAIR.", 26, "gold", True)
card(d, 1070, 124, "#101820")
put(d, (105, 1095), "Same evidence. Different conclusions.", 34, "ink", True)
put(d, (105, 1149), "CONCEPT ARTWORK  ·  REAL TRIAL INSIDE", 18, "muted", True)
keep("01-cover", im)

im, d = frame(2)
heading(d, "Four roles.", "Different mandates.")
put(d, (72, 406), "ONE MODEL. SEPARATE ROLE PROMPTS.", 24, "gold", True)
roles = [
    ("BULL", "Build the strongest supportable upside thesis.", "bull"),
    ("BEAR", "Challenge valuation and expose failure modes.", "bear"),
    ("RISK", "Test downside and identify missing inputs.", "gold"),
    ("CHAIR", "Compare the submissions and explain dissent.", "ink"),
]
for i, (title, body, color) in enumerate(roles):
    y = 472 + i * 170
    card(d, y, 145)
    put(d, (108, y + 25), title, 24, color, True)
    put(d, (108, y + 69), body, 31)
put(d, (72, 1188), "Distinct prompts do not make independent sources of truth.", 23, "muted")
keep("02-roles", im)

im, d = frame(3)
heading(d, "Meet AuroraGrid AI.", "A fictional company.", 74)
put(d, (72, 397), "SYNTHETIC DATA  /  ENTERPRISE ENERGY SOFTWARE", 22, "gold", True)
case = RUN["snapshot"]["case"]
cells = [
    ("Annual revenue", f"€{case['revenue_eur_m']}M"),
    ("Revenue growth", f"{case['revenue_growth_pct']}%"),
    ("Gross margin", f"{case['gross_margin_pct']}%"),
    ("Net revenue retention", f"{case['net_revenue_retention_pct']}%"),
    ("Annual free cash flow", f"−€{abs(Decimal(case['annual_fcf_eur_m']))}M"),
    ("Largest customer share", f"{case['largest_customer_share_pct']}%"),
]
for i, (label, value) in enumerate(cells):
    x, y = 72 + (i % 2) * 478, 469 + (i // 2) * 202
    d.rounded_rectangle((x, y, x + 458, y + 170), 16, fill=C["card"])
    put(d, (x + 27, y + 26), label, 22, "muted")
    put(d, (x + 27, y + 70), value, 54, "gold", True)
put(d, (72, 1133), "Identical snapshot for every specialist.", 29, "ink", True)
put(d, (72, 1184), "No live quotes, market feeds or real companies.", 23, "muted")
keep("03-case", im)

im, d = frame(4)
heading(d, "Convene", "the committee.", 86)
put(d, (72, 416), "ACTUAL STREAMLIT SCREEN  /  LIVE EXECUTION", 24, "gold", True)
shot = Image.open(M / "live-progress.png").convert("RGB").crop((135, 60, 1306, 635))
shot.thumbnail((936, 570), Image.Resampling.LANCZOS)
im.paste(shot, (72, 475))
card(d, 974, 168)
put(d, (102, 1003), "Three separate specialist requests.", 34, "ink", True)
put(d, (102, 1063), "The Chair starts after all three validate.", 29, "muted")
put(d, (72, 1185), "Local Ollama · Gemma 4 · Python orchestration", 24, "gold")
keep("04-live-run", im)

im, d = frame(5)
heading(d, "Same facts.", "Different theses.", 81)
put(d, (72, 406), "VERBATIM EXCERPTS FROM THE RECORDED RUN", 24, "gold", True)
quotes = [
    ("BULL", RUN["roles"]["bull"]["output"]["thesis"], "bull"),
    ("BEAR", RUN["roles"]["bear"]["output"]["thesis"], "bear"),
    ("RISK", RUN["roles"]["risk"]["output"]["key_risks_or_catalysts"][1], "gold"),
]
for i, (title, quote, color) in enumerate(quotes):
    y = 467 + i * 227
    card(d, y, 201)
    put(d, (105, y + 24), title, 23, color, True)
    para(d, (105, y + 65), short_quote(quote, 22), 29, width=854, limit=3)
put(d, (72, 1178), "Model interpretations. The audit flags claims needing evidence.", 23, "muted")
keep("05-disagreement", im)

im, d = frame(6)
heading(d, "Three scenarios.", "Checked arithmetic.", 77)
metrics = RUN["snapshot"]["metrics"]
put(d, (72, 407), f"STARTING ILLUSTRATIVE EQUITY  €{Decimal(metrics['reference_equity_eur_m']):.0f}M", 24, "gold", True)
maximum = max(Decimal(v["equity_eur_m"]) for v in metrics["scenarios"].values())
for i, (name, color) in enumerate((("bear", "bear"), ("base", "gold"), ("bull", "bull"))):
    row = metrics["scenarios"][name]
    y = 500 + 179 * i
    change = Decimal(row["change_pct"])
    label = f"{change:+.1f}%" if change else "0.0%"
    put(d, (72, y), f"{name.title()}  ·  €{Decimal(row['equity_eur_m']):,.0f}M", 40, "ink", True)
    put(d, (836, y + 7), label, 35, color, True)
    d.rounded_rectangle((72, y + 71, 1008, y + 99), 9, fill=C["card"])
    d.rounded_rectangle((72, y + 71, 72 + int(936 * Decimal(row["equity_eur_m"]) / maximum), y + 99), 9, fill=C[color])
put(d, (72, 1080), "Equity = revenue × EV/sales + net cash", 30, "ink", True)
put(d, (72, 1133), "Cash and debt held constant. No probability weighting.", 24, "muted")
put(d, (72, 1180), "HYPOTHETICAL SENSITIVITIES, NOT FORECASTS", 22, "gold", True)
keep("06-scenarios", im)

im, d = frame(7)
chair = RUN["roles"]["chair"]["output"]
heading(d, "Chair verdict:", chair["verdict"].replace("_", " ").title() + ".", 76)
put(d, (72, 404), "RECORDED MODEL VERDICT  /  FICTIONAL CASE", 24, "gold", True)
card(d, 470, 294)
put(d, (105, 498), "WHERE THEY DISAGREED", 24, "gold", True)
for i, item in enumerate(chair["disagreements"][:2]):
    para(d, (105, 554 + i * 89), "• " + item["topic"], 31, width=840, limit=2)
card(d, 792, 331)
put(d, (105, 820), "WHAT TO INVESTIGATE NEXT", 24, "gold", True)
for i, label in enumerate(("Free cash flow trajectory", "Largest customer contract terms", "Cash burn versus available liquidity")):
    put(d, (105, 883 + i * 62), "• " + label, 31)
put(d, (72, 1180), "Educational research only. No personal recommendation.", 23, "muted")
keep("07-verdict", im)

im, d = frame(8)
heading(d, "Run it.", "Audit it yourself.", 88)
put(d, (72, 425), "FREE SOURCE  /  REPRODUCIBLE SYNTHETIC CASE", 24, "gold", True)
for i, (title, body) in enumerate((
    ("REPLAY THE RECORDED TRIAL", "Read the raw role outputs and the Chair verdict."),
    ("CHECK THE NUMBERS", "Trace scenarios to Decimal formulas and inputs."),
    ("RUN THE LAB LOCALLY", "Streamlit + Ollama. Optional Foundry adapter."),
)):
    y = 490 + i * 175
    card(d, y, 145)
    put(d, (104, y + 25), title, 25, "gold", True)
    put(d, (104, y + 70), body, 29)
card(d, 1099, 111, "gold")
put(d, (107, 1131), "Comment “CODE” to get the link. →", 36, "bg", True)
keep("08-code", im)

preview = Image.new("RGB", (1080, 676), C["bg"])
for i, im in enumerate(SLIDES):
    assert im.size == (1080, 1350)
    preview.paste(im.resize((270, 338), Image.Resampling.LANCZOS), ((i % 4) * 270, (i // 4) * 338))
preview.save(M / "carousel-preview.png")
print("Eight 1080x1350 slides verified; preview saved.")

