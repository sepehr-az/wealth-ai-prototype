"""
LIQID | Silent Portfolio Intelligence
AI-Native Lead Qualification Engine — Track A: Growth & Acquisition

Core concept: User uploads a brokerage screenshot. The AI simultaneously extracts
their holdings AND silently scores them for wealth tier, sophistication, and
LIQID product fit. The gap analysis is identical for everyone; the CTA diverges
invisibly based on the silent score.
"""

import streamlit as st
import anthropic
import pandas as pd
import json
import base64

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Portfolio Intelligence | LIQID",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

html, body, [class*="css"], [data-testid] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background-color: #ffffff;
}
[data-testid="stMain"] > .block-container {
  padding-top: 8px !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
  max-width: 1214px;
  margin: 0 auto;
}

/* ─── Sidebar (collapsed) ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] { background-color: #460f28 !important; top: 0 !important; }
[data-testid="stSidebar"] * { color: #ffffff !important; }

/* ─── Typography ──────────────────────────────────────────────────────────── */
h1, h2, h3, h4 {
  color: #232425 !important; font-weight: 500 !important;
  letter-spacing: -0.02em; text-wrap: balance;
}
p, li, label { color: #232425; font-weight: 400; line-height: 1.6; }

/* ─── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
  background-color: #232425 !important; color: #ffffff !important;
  border: none !important; border-radius: 2px !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  letter-spacing: 0.01em !important; padding: 0.65rem 1.75rem !important;
  transition: background-color 0.3s ease, transform 0.15s ease !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
  background-color: #460f28 !important; transform: translateY(-1px);
}
.stButton > button:not([kind="primary"]) {
  border: 1.5px solid #232425 !important; color: #232425 !important;
  border-radius: 2px !important; font-weight: 500 !important;
  background: transparent !important; transition: all 0.3s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
  background-color: #232425 !important; color: #ffffff !important;
}

/* ─── Inputs ──────────────────────────────────────────────────────────────── */
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div {
  border-radius: 2px !important; border-color: #c3c3c4 !important;
  transition: border-color 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
[data-baseweb="input"] > div:focus-within,
[data-baseweb="textarea"] > div:focus-within {
  border-color: #460f28 !important;
  box-shadow: 0 0 0 2px rgba(70,15,40,0.12) !important;
}

/* ─── File uploader ───────────────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
  border: 2px dashed #c3c3c4 !important; border-radius: 2px !important;
  background: #f9f9f9 !important; transition: border-color 0.3s ease !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #460f28 !important;
}

/* ─── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: #f9f9f9; border: 1px solid #ececec;
  border-radius: 2px; padding: 1rem 1.25rem;
}
[data-testid="stMetricLabel"] {
  font-size: 0.7rem !important; font-weight: 500 !important;
  color: #787878 !important; letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}
[data-testid="stMetricValue"] { color: #232425 !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] > div {
  color: #460f28 !important; font-size: 0.75rem !important; font-weight: 500 !important;
}

/* ─── Alerts / dividers ───────────────────────────────────────────────────── */
hr { border-color: #ececec !important; }
[data-testid="stAlert"] { border-radius: 2px !important; border-left-width: 3px !important; }

/* ─── Spinner ─────────────────────────────────────────────────────────────── */
[data-testid="stSpinner"] > div { border-top-color: #460f28 !important; }

/* ─── Caption ─────────────────────────────────────────────────────────────── */
small, .stCaption, [data-testid="stCaptionContainer"] {
  color: #787878 !important; font-size: 0.75rem !important;
}

/* ─── LIQID Announcement bar ──────────────────────────────────────────────── */
.liqid-bar {
  background-color: #460f28; color: #fff; text-align: center;
  font-size: 0.72rem; font-weight: 500; letter-spacing: 0.06em;
  padding: 0.5rem 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  overflow: hidden;
}
.liqid-bar-shine {
  position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  animation: shineMove 3.5s linear infinite;
}
@keyframes shineMove { to { left: 160%; } }

/* ─── LIQID Navbar ────────────────────────────────────────────────────────── */
.liqid-nav {
  position: fixed; top: 36px; left: 0; right: 0; z-index: 9998;
  background: #ffffff; border-bottom: 1px solid #ececec;
  box-shadow: 0px 15px 10px -15px rgba(0,0,0,0.08);
}
.liqid-nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  max-width: 1214px; margin: 0 auto; padding: 0 2rem; height: 64px;
}
.liqid-logo {
  font-size: 1.2rem; font-weight: 700; letter-spacing: 0.15em;
  color: #460f28 !important; text-decoration: none;
}
.liqid-nav-links { display: flex; gap: 2rem; list-style: none; margin: 0; padding: 0; }
.liqid-nav-links a {
  font-size: 0.875rem; font-weight: 400; color: #232425;
  text-decoration: none; transition: color 0.2s ease;
}
.liqid-nav-links a:hover { color: #460f28; }
.liqid-nav-buttons { display: flex; gap: 0.75rem; align-items: center; }
.liqid-btn-secondary {
  font-size: 0.8rem; font-weight: 500; border: 1.5px solid #232425; color: #232425;
  padding: 0.45rem 1.1rem; border-radius: 2px; text-decoration: none; transition: all 0.25s ease;
}
.liqid-btn-secondary:hover { background: #232425; color: #fff; }
.liqid-btn-primary {
  font-size: 0.8rem; font-weight: 500; background: #232425; color: #fff;
  padding: 0.45rem 1.1rem; border-radius: 2px; text-decoration: none; transition: background 0.25s ease;
}
.liqid-btn-primary:hover { background: #460f28; }

/* ─── Content offset ──────────────────────────────────────────────────────── */
.liqid-spacer { height: 100px; }

/* ─── Hero ────────────────────────────────────────────────────────────────── */
.liqid-hero {
  padding: 3rem 0 2rem; border-bottom: 1px solid #ececec; margin-bottom: 2.5rem;
}
.liqid-hero-eyebrow {
  font-size: 0.7rem; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.75rem;
}
.liqid-hero h1 {
  font-size: clamp(2rem, 3.5vw, 3rem) !important; font-weight: 500 !important;
  line-height: 1.15; letter-spacing: -0.03em; color: #232425 !important; margin: 0 0 1.25rem;
}
.liqid-hero-sub {
  font-size: 1.05rem; color: #2f3030; line-height: 1.7; max-width: 560px; margin-bottom: 2rem;
}
.liqid-hero-disclaimer {
  font-size: 0.7rem; color: #787878; margin-top: 1.5rem;
  padding-top: 1rem; border-top: 1px solid #ececec;
}

/* ─── Upload zone label ───────────────────────────────────────────────────── */
.liqid-upload-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.5rem;
}

/* ─── Demo persona cards ──────────────────────────────────────────────────── */
.demo-card {
  border: 1px solid #ececec; border-radius: 2px; padding: 1rem;
  margin-bottom: 0.75rem; transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: #fff;
}
.demo-card:hover { border-color: #460f28; box-shadow: 0 2px 12px rgba(70,15,40,0.08); }
.demo-card-eyebrow {
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.25rem;
}
.demo-card-name { font-size: 0.95rem; font-weight: 500; color: #232425; margin-bottom: 0.2rem; }
.demo-card-sub  { font-size: 0.75rem; color: #787878; line-height: 1.4; }

/* ─── Section headings ────────────────────────────────────────────────────── */
.liqid-section-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.4rem;
}
.liqid-section-title {
  font-size: 1.4rem; font-weight: 500; color: #232425;
  letter-spacing: -0.02em; margin-bottom: 0.5rem;
}
.liqid-section-sub { font-size: 0.875rem; color: #787878; margin-bottom: 1.75rem; }

/* ─── Gap cards ───────────────────────────────────────────────────────────── */
.liqid-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.liqid-card {
  border: 1px solid #ececec; border-radius: 2px; padding: 1.25rem;
  transition: box-shadow 0.3s ease, transform 0.2s ease; background: #fff;
}
.liqid-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.06); transform: translateY(-2px); }
.liqid-card-badge {
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
  color: #787878; background: #f4f4f4; display: inline-block;
  padding: 0.2rem 0.5rem; border-radius: 1px; margin-bottom: 0.75rem;
}
.liqid-card-badge.increase { background: #edf7f0; color: #1a7340; }
.liqid-card-badge.reduce   { background: #fdf0f0; color: #c0392b; }
.liqid-card-badge.ontarget { background: #f0f4ff; color: #2c4ab5; }
.liqid-card-asset  { font-size: 1rem; font-weight: 500; color: #232425; margin-bottom: 0.4rem; }
.liqid-card-gap    { font-size: 1.6rem; font-weight: 300; letter-spacing: -0.02em; }
.liqid-card-gap.pos  { color: #1a7340; }
.liqid-card-gap.neg  { color: #c0392b; }
.liqid-card-gap.zero { color: #2c4ab5; }
.liqid-card-meta   { font-size: 0.75rem; color: #787878; margin-top: 0.5rem; }

/* ─── AI narrative quote ──────────────────────────────────────────────────── */
.liqid-quote {
  background: #460f28; color: #fff; padding: 2.5rem; border-radius: 2px; margin: 2rem 0;
}
.liqid-quote-text {
  font-size: clamp(1rem, 2.2vw, 1.5rem); font-weight: 300; font-style: italic;
  line-height: 1.5; color: #fff;
}
.liqid-quote-source { font-size: 0.75rem; color: rgba(255,255,255,0.6); margin-top: 1rem; }

/* ─── Lead capture card ───────────────────────────────────────────────────── */
.liqid-lead-card {
  border: 1px solid #ececec; border-radius: 2px;
  padding: 2rem; background: #f9f9f9; margin-top: 1.5rem;
}
.liqid-lead-title { font-size: 1.1rem; font-weight: 500; color: #232425; margin-bottom: 0.4rem; }
.liqid-lead-sub   { font-size: 0.875rem; color: #787878; margin-bottom: 1.25rem; line-height: 1.6; }

/* ─── RM path — elevated CTA ──────────────────────────────────────────────── */
.liqid-lead-card.rm-path {
  border-color: #232425; background: #fff;
}
.liqid-rm-badge {
  display: inline-block; background: #232425; color: #fff;
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; padding: 0.2rem 0.6rem; border-radius: 1px; margin-bottom: 1rem;
}

/* ─── Internal scoring panel ──────────────────────────────────────────────── */
.liqid-funnel-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 1rem;
  padding-bottom: 0.5rem; border-bottom: 1px solid #ececec;
}
.score-badge {
  display: inline-block; padding: 0.3rem 0.75rem; border-radius: 2px;
  font-size: 0.8rem; font-weight: 500; color: #fff; margin-bottom: 0.25rem;
}
.score-note {
  font-size: 0.7rem; color: #787878; line-height: 1.5; font-style: italic;
}

/* ─── Streaming preview ───────────────────────────────────────────────────── */
.stream-preview {
  padding: 1.25rem; background: #f9f9f9; border-radius: 2px;
  color: #232425; font-size: 0.9rem; line-height: 1.7; min-height: 60px;
}

/* ─── Footer ──────────────────────────────────────────────────────────────── */
.liqid-footer {
  margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #ececec;
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;
}
.liqid-footer-logo { font-size: 0.9rem; font-weight: 700; letter-spacing: 0.15em; color: #460f28; }
.liqid-footer-text { font-size: 0.7rem; color: #787878; }
</style>

<!-- Announcement bar -->
<div class="liqid-bar">
  <div class="liqid-bar-shine"></div>
  Smart Minds. Smart Money. — KI-gestützte Portfolio-Analyse für anspruchsvolle Anleger &rarr;
</div>

<!-- Navbar -->
<nav class="liqid-nav">
  <div class="liqid-nav-inner">
    <a class="liqid-logo" href="#">LIQID</a>
    <ul class="liqid-nav-links">
      <li><a href="#">Lösungen</a></li>
      <li><a href="#">Über uns</a></li>
      <li><a href="#">Wissen</a></li>
      <li><a href="#">Kontakt</a></li>
    </ul>
    <div class="liqid-nav-buttons">
      <a class="liqid-btn-secondary" href="#">Einloggen</a>
      <a class="liqid-btn-primary" href="#">Jetzt investieren</a>
    </div>
  </div>
</nav>

<div class="liqid-spacer"></div>
""", unsafe_allow_html=True)

# ── Demo personas — rich, plausible HNW profiles ──────────────────────────────
DEMO_PERSONAS = {
    "Marcus K.": {
        "subtitle": "Tech-Gründer · €1.85M · Post-Exit, konzentriert",
        "description": "SAP-Aktienoptionen + Krypto-Allocation + Cash-Überhang nach IPO-Exit",
        "holdings": {"Aktien": 58, "Anleihen": 3, "Alternatives": 12, "Liquidität": 27},
        "estimated_value": 1_850_000,
        "holding_names": "SAP SE 28% · NVIDIA Corp 18% · Bitcoin via Coinbase 12% · iShares MSCI World 15% · Barvermögen DKB 27%",
        "sophistication": "HIGH",
        "wealth_tier": "HNW",
        "risk_inferred": "Aggressive",
    },
    "Sabine M.": {
        "subtitle": "Chefärztin · €380K · Konservativ, ETF-fokussiert",
        "description": "Solide Basis, aber 45% Tagesgeld — klassischer Kaufkraftverlust-Fall",
        "holdings": {"Aktien": 30, "Anleihen": 20, "Alternatives": 5, "Liquidität": 45},
        "estimated_value": 380_000,
        "holding_names": "iShares Core MSCI Europe 30% · Bundesanleihen 2031 20% · Gold ETC Xetra 5% · Tagesgeld ING 45%",
        "sophistication": "MEDIUM",
        "wealth_tier": "EMERGING_HNW",
        "risk_inferred": "Conservative",
    },
    "Klaus B.": {
        "subtitle": "Beamter i.R. · €155K · Weltportfolio-Strategie",
        "description": "Disziplinierter ETF-Anleger, kein Alternatives-Zugang, Standardallokation",
        "holdings": {"Aktien": 80, "Anleihen": 0, "Alternatives": 0, "Liquidität": 20},
        "estimated_value": 155_000,
        "holding_names": "iShares MSCI World ETF 60% · iShares EM IMI ETF 20% · Tagesgeld Scalable Capital 20%",
        "sophistication": "LOW",
        "wealth_tier": "EMERGING_HNW",
        "risk_inferred": "Aggressive",
    },
}

# ── Peer benchmarks by wealth tier + risk ─────────────────────────────────────
# Key insight: HNW/UHNW peers hold far more alternatives (private markets).
# This is LIQID's core value prop — and the gap that makes the analysis compelling.
BENCHMARKS = {
    "EMERGING_HNW": {
        "Conservative": {"Aktien": 30, "Anleihen": 40, "Alternatives": 12, "Liquidität": 18},
        "Balanced":     {"Aktien": 52, "Anleihen": 25, "Alternatives": 15, "Liquidität": 8},
        "Aggressive":   {"Aktien": 70, "Anleihen": 8,  "Alternatives": 15, "Liquidität": 7},
    },
    "HNW": {
        "Conservative": {"Aktien": 25, "Anleihen": 30, "Alternatives": 35, "Liquidität": 10},
        "Balanced":     {"Aktien": 45, "Anleihen": 15, "Alternatives": 35, "Liquidität": 5},
        "Aggressive":   {"Aktien": 58, "Anleihen": 5,  "Alternatives": 33, "Liquidität": 4},
    },
    "UHNW": {
        "Conservative": {"Aktien": 20, "Anleihen": 20, "Alternatives": 50, "Liquidität": 10},
        "Balanced":     {"Aktien": 38, "Anleihen": 10, "Alternatives": 48, "Liquidität": 4},
        "Aggressive":   {"Aktien": 50, "Anleihen": 3,  "Alternatives": 44, "Liquidität": 3},
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def compute_cta_path(sophistication: str, wealth_tier: str) -> str:
    """Silent routing logic — never exposed to the user."""
    if sophistication == "HIGH" or wealth_tier in ("HNW", "UHNW"):
        return "rm"       # Direct RM handoff — pre-qualified, high-value
    return "nurture"      # Automated nurture sequence — protect RM capacity


def build_gap_df(holdings: dict, benchmark: dict) -> pd.DataFrame:
    rows = []
    for ac in ["Aktien", "Anleihen", "Alternatives", "Liquidität"]:
        cur = holdings.get(ac, 0)
        tgt = benchmark.get(ac, 0)
        gap = tgt - cur
        rows.append({
            "Asset-Klasse": ac,
            "Ihr Portfolio (%)": cur,
            "Peer-Benchmark (%)": tgt,
            "Gap (pp)": gap,
        })
    return pd.DataFrame(rows)


def format_value(val: int) -> str:
    if not val:
        return "—"
    if val >= 1_000_000:
        return f"€{val / 1_000_000:.2f}M"
    return f"€{val / 1_000:.0f}K"


def get_client() -> anthropic.Anthropic:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    return anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()


def build_narrative_prompt(portfolio: dict, gap_df: pd.DataFrame) -> str:
    obs_lines = []
    for _, row in gap_df.iterrows():
        ac = row["Asset-Klasse"]
        gap = row["Gap (pp)"]
        cur = row["Ihr Portfolio (%)"]
        tgt = row["Peer-Benchmark (%)"]
        if abs(gap) > 2:
            direction = "untergewichtet" if gap > 0 else "übergewichtet"
            obs_lines.append(
                f"{ac}: Sie {cur:.0f}% vs. Peers {tgt:.0f}% → {direction} um {abs(gap):.0f}pp"
            )
    observations = "\n".join(obs_lines) if obs_lines else "Portfolio weitgehend im Zielbereich."

    return f"""Du bist Senior Wealth Advisor bei LIQID, einer digitalen Privatbank für vermögende Anleger im DACH-Raum.

Schreibe eine personalisierte Portfolio-Gap-Analyse auf Deutsch für einen Kunden mit folgendem Profil:

Positionen: {portfolio["holding_names"]}
Geschätzter Portfoliowert: {format_value(portfolio["estimated_value"])}
Vermögenstier: {portfolio["wealth_tier"]}
Inferred Risikoprofil: {portfolio["risk_inferred"]}
Sophistication: {portfolio["sophistication"]}

Gap-Analyse vs. Peer-Benchmark ({portfolio["wealth_tier"]}, {portfolio["risk_inferred"]}):
{observations}

Schreibe genau 3 prägnante Absätze:
1. Was der Kunde richtig macht — ehrlich, nicht schmeichelhaft
2. Den bedeutendsten Gap vs. Peers dieser Vermögensklasse. Falls Alternatives untergewichtet sind: erkläre, dass institutionelle Investoren und Private-Bank-Kunden diesen Zugang systematisch nutzen, während er Retailanlegern typischerweise verschlossen bleibt.
3. Was die Schließung dieses Gaps langfristig für die Vermögensentwicklung bedeuten könnte — konkret, nicht vage

Ton: sophisticated, respektvoll, direkt. Wie ein vertrauenswürdiger Advisor, dem das Ergebnis des Kunden am Herzen liegt.
Kein Markdown, keine Aufzählungszeichen, nur Fließtext. Keine Werbung für LIQID namentlich."""


# ── Session state ─────────────────────────────────────────────────────────────
_defaults = {
    "analyzed": False,
    "portfolio": None,       # dict: holdings, estimated_value, holding_names, sophistication, wealth_tier, risk_inferred
    "gap_df": None,
    "narrative": "",
    "cta_path": None,        # "rm" | "nurture"
    "email": "",
    "lead_captured": False,
    "source": None,          # "demo" | "upload"
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Layout ────────────────────────────────────────────────────────────────────
col_main, col_funnel = st.columns([3, 1])

# ════════════════════════════════════════════════════════════════════════════
# MAIN COLUMN
# ════════════════════════════════════════════════════════════════════════════
with col_main:

    # ── PHASE 1: Upload / Demo selection ──────────────────────────────────────
    if not st.session_state.analyzed:

        st.markdown("""
        <div class="liqid-hero">
          <div class="liqid-hero-eyebrow">KI-gestützte Portfolio-Analyse</div>
          <h1>Ihr Portfolio.<br>Verglichen mit Ihren Peers.</h1>
          <p class="liqid-hero-sub">
            Laden Sie Ihren Depotauszug hoch. In Sekunden analysiert unsere KI Ihre Allokation
            und vergleicht sie mit dem Benchmark institutioneller Investoren Ihrer Vermögensklasse —
            ganz ohne Formular.
          </p>
          <p class="liqid-hero-disclaimer">
            <strong>MiFID II:</strong> Dies ist keine Anlageberatung. Alle Inhalte dienen
            ausschließlich zu Informationszwecken und stellen keine individuelle
            Anlageempfehlung dar.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Real upload ────────────────────────────────────────────────────────
        st.markdown('<div class="liqid-upload-label">Depotauszug hochladen</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Depotauszug hochladen (PNG, JPG)",
            type=["png", "jpg", "jpeg"],
            help="Unterstützte Broker: Trade Republic · Scalable Capital · DKB · Deutsche Bank · Comdirect · ING",
            label_visibility="collapsed",
        )

        st.markdown(
            '<p style="font-size:0.75rem;color:#787878;margin-top:0.5rem">'
            'Ihr Screenshot verlässt nicht Ihren Browser — die Analyse läuft on-demand über eine '
            'verschlüsselte API-Verbindung.</p>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Demo personas ──────────────────────────────────────────────────────
        st.markdown("""
        <div class="liqid-section-label">Demo-Portfolios</div>
        <div class="liqid-section-title" style="margin-bottom:0.25rem">
          Oder wählen Sie ein Beispielprofil
        </div>
        <p class="liqid-section-sub">
          Drei reale Investorentypen aus dem DACH-Markt — unterschiedliche Vermögenstiers,
          unterschiedliche Gaps.
        </p>
        """, unsafe_allow_html=True)

        demo_cols = st.columns(3)
        for i, (name, data) in enumerate(DEMO_PERSONAS.items()):
            with demo_cols[i]:
                st.markdown(f"""
                <div class="demo-card">
                  <div class="demo-card-eyebrow">Demo · {data["wealth_tier"]}</div>
                  <div class="demo-card-name">{name}</div>
                  <div class="demo-card-sub">{data["subtitle"]}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Analysieren →", key=f"demo_{name}", use_container_width=True):
                    st.session_state.portfolio = data
                    st.session_state.source = "demo"
                    st.session_state.analyzed = True
                    st.rerun()

        # ── Process real upload ────────────────────────────────────────────────
        if uploaded:
            with st.spinner("Portfolio wird eingelesen — Claude AI analysiert Ihren Depotauszug…"):
                try:
                    img_bytes = uploaded.read()
                    img_b64 = base64.b64encode(img_bytes).decode()
                    media_type = uploaded.type or "image/jpeg"

                    extraction_prompt = """Du bist ein Portfolio-Intelligenz-System für eine Wealth-Management-Plattform.

Analysiere diesen Broker-Screenshot und extrahiere die Portfoliodaten.
Antworte NUR mit gültigem JSON (kein Markdown, keine Erklärungen):

{
  "holdings": {
    "Aktien": <Prozent 0-100, Integer>,
    "Anleihen": <Prozent 0-100, Integer>,
    "Alternatives": <Prozent 0-100, Integer>,
    "Liquidität": <Prozent 0-100, Integer>
  },
  "estimated_value": <Gesamtwert in EUR als Integer, oder null falls nicht erkennbar>,
  "holding_names": "<kommaseparierte Liste sichtbarer Positionen mit ca. %-Anteil>",
  "sophistication": "<LOW|MEDIUM|HIGH>",
  "wealth_tier": "<EMERGING_HNW|HNW|UHNW>",
  "risk_inferred": "<Conservative|Balanced|Aggressive>"
}

Sophistication-Kriterien:
- HIGH: Alternatives vorhanden (PE, Hedge Funds, Zertifikate), Einzelaktien-Mix
- MEDIUM: ETFs + Einzelaktien ODER ETFs + Anleihen
- LOW: Nur ETFs, oder überwiegend Cash/Tagesgeld

Wealth-Tier (aus sichtbarem Portfoliowert):
- UHNW: >€2M  |  HNW: €500K–€2M  |  EMERGING_HNW: €100K–€500K

Holdings müssen sich zu 100 addieren. Fehlende Kategorien → 0."""

                    response = get_client().messages.create(
                        model="claude-opus-4-6",
                        max_tokens=1024,
                        messages=[{
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": img_b64,
                                    },
                                },
                                {"type": "text", "text": extraction_prompt},
                            ],
                        }],
                    )

                    raw = response.content[0].text.strip()
                    # Strip markdown code fences if present
                    if "```" in raw:
                        parts = raw.split("```")
                        raw = parts[1] if len(parts) > 1 else parts[0]
                        if raw.startswith("json"):
                            raw = raw[4:]

                    data = json.loads(raw.strip())

                    # Validate holdings sum — normalize if Claude drifted from 100
                    raw_holdings = data.get("holdings", {})
                    total = sum(raw_holdings.values()) if raw_holdings else 0

                    if total < 10:
                        # Claude couldn't identify a portfolio — not a brokerage screenshot
                        st.error(
                            "Kein Depot erkannt. Das Bild enthält keine lesbaren Portfolio-Daten. "
                            "Bitte laden Sie einen Depotauszug (z.B. Trade Republic, Scalable) hoch "
                            "oder wählen Sie ein Demo-Portfolio."
                        )
                        st.stop()

                    # Normalize to 100% if sum is off
                    if total > 0 and abs(total - 100) > 2:
                        raw_holdings = {k: round(v / total * 100) for k, v in raw_holdings.items()}

                    portfolio = {
                        "holdings": raw_holdings,
                        "estimated_value": data.get("estimated_value") or 300_000,
                        "holding_names": data.get("holding_names", "Erkannte Positionen"),
                        "sophistication": data.get("sophistication", "MEDIUM"),
                        "wealth_tier": data.get("wealth_tier", "EMERGING_HNW"),
                        "risk_inferred": data.get("risk_inferred", "Balanced"),
                        "subtitle": "Hochgeladener Depotauszug",
                        "description": "Live-Analyse via Claude Vision",
                    }

                    st.session_state.portfolio = portfolio
                    st.session_state.source = "upload"
                    st.session_state.analyzed = True
                    st.rerun()

                except anthropic.AuthenticationError:
                    st.error("API-Key fehlt oder ungültig. Bitte in `.streamlit/secrets.toml` konfigurieren.")
                except json.JSONDecodeError:
                    st.error(
                        "Das Portfolio konnte nicht automatisch eingelesen werden. "
                        "Bitte versuchen Sie einen klareren Screenshot oder wählen Sie ein Demo-Portfolio."
                    )
                except Exception as e:
                    st.error(f"Fehler bei der Analyse: {e}")

    # ── PHASE 2: Results ───────────────────────────────────────────────────────
    else:
        portfolio = st.session_state.portfolio

        # Compute gap df on first results render
        if st.session_state.gap_df is None:
            tier_benchmarks = BENCHMARKS.get(
                portfolio.get("wealth_tier", "EMERGING_HNW"),
                BENCHMARKS["EMERGING_HNW"],
            )
            benchmark = tier_benchmarks.get(
                portfolio.get("risk_inferred", "Balanced"),
                tier_benchmarks["Balanced"],
            )
            gap_df = build_gap_df(portfolio["holdings"], benchmark)
            st.session_state.gap_df = gap_df
            st.session_state.cta_path = compute_cta_path(
                portfolio.get("sophistication", "MEDIUM"),
                portfolio.get("wealth_tier", "EMERGING_HNW"),
            )

        gap_df = st.session_state.gap_df

        # ── Portfolio header ───────────────────────────────────────────────────
        source_badge = "Live-Analyse" if st.session_state.source == "upload" else "Demo"
        st.markdown(f"""
        <div class="liqid-section-label">Portfolio-Analyse · {source_badge}</div>
        <div class="liqid-section-title">
          {format_value(portfolio["estimated_value"])} &nbsp;·&nbsp;
          {portfolio.get("risk_inferred", "—")} &nbsp;·&nbsp;
          Benchmark: {portfolio.get("wealth_tier", "—")}-Peers
        </div>
        <p class="liqid-section-sub">{portfolio["holding_names"]}</p>
        """, unsafe_allow_html=True)

        # ── Gap cards ──────────────────────────────────────────────────────────
        cards_html = '<div class="liqid-cards">'
        for _, row in gap_df.iterrows():
            gap = row["Gap (pp)"]
            cur = row["Ihr Portfolio (%)"]
            tgt = row["Peer-Benchmark (%)"]

            if gap > 2:
                badge_cls, badge_txt, gap_cls = "increase", "Untergewichtet", "pos"
            elif gap < -2:
                badge_cls, badge_txt, gap_cls = "reduce", "Übergewichtet", "neg"
            else:
                badge_cls, badge_txt, gap_cls = "ontarget", "Im Zielbereich", "zero"

            cards_html += f"""
            <div class="liqid-card">
              <div class="liqid-card-badge {badge_cls}">{badge_txt}</div>
              <div class="liqid-card-asset">{row['Asset-Klasse']}</div>
              <div class="liqid-card-gap {gap_cls}">{gap:+.0f} pp</div>
              <div class="liqid-card-meta">Sie {cur:.0f}% &nbsp;·&nbsp; Peers {tgt:.0f}%</div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        with st.expander("Detailtabelle anzeigen"):
            styled = (
                gap_df.style
                .map(
                    lambda v: "color:#1a7340;font-weight:600" if isinstance(v, (int, float)) and v > 0
                    else ("color:#c0392b;font-weight:600" if isinstance(v, (int, float)) and v < 0 else ""),
                    subset=["Gap (pp)"],
                )
                .format({
                    "Ihr Portfolio (%)": "{:.0f}%",
                    "Peer-Benchmark (%)": "{:.0f}%",
                    "Gap (pp)": "{:+.0f}pp",
                })
            )
            st.dataframe(styled, use_container_width=True, hide_index=True)

        # ── AI narrative (streaming) ───────────────────────────────────────────
        if not st.session_state.narrative:
            try:
                prompt = build_narrative_prompt(portfolio, gap_df)
                narrative_ph = st.empty()
                full_text = ""

                with get_client().messages.stream(
                    model="claude-sonnet-4-6",
                    max_tokens=900,
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    for text in stream.text_stream:
                        full_text += text
                        narrative_ph.markdown(
                            f'<div class="stream-preview">{full_text}▌</div>',
                            unsafe_allow_html=True,
                        )

                narrative_ph.empty()
                st.session_state.narrative = full_text

            except anthropic.AuthenticationError:
                st.error("API-Key ungültig. Narrative-Generierung nicht möglich.")
            except Exception as e:
                st.error(f"Fehler: {e}")

        if st.session_state.narrative:
            st.markdown(f"""
            <div class="liqid-quote">
              <div class="liqid-quote-text">„{st.session_state.narrative}"</div>
              <div class="liqid-quote-source">Claude AI · LIQID Portfolio Intelligence</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # ── Forked CTA ─────────────────────────────────────────────────────
            # The user never sees the routing decision — they only see the CTA.
            # The two CTAs feel natural and contextually appropriate for their profile.

            if not st.session_state.lead_captured:
                cta = st.session_state.cta_path

                if cta == "rm":
                    # Path A: High sophistication or HNW/UHNW — direct RM routing
                    st.markdown("""
                    <div class="liqid-lead-card rm-path">
                      <div class="liqid-rm-badge">Private Markets Zugang</div>
                      <div class="liqid-lead-title">
                        Ihr Portfolio qualifiziert für institutionelle Investmentstrategien
                      </div>
                      <div class="liqid-lead-sub">
                        Basierend auf Ihrer Allokation sehen wir konkrete Optimierungspotenziale —
                        insbesondere im Bereich Private Equity und alternative Anlageklassen, zu
                        denen Sie über LIQID Zugang erhalten können. Ein Senior Advisor zeigt Ihnen,
                        was Investoren Ihrer Größenordnung heute anders machen.
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.form("rm_form"):
                        fc1, fc2 = st.columns(2)
                        with fc1:
                            name_in = st.text_input("Ihr Name", placeholder="Dr. Max Mustermann")
                        with fc2:
                            email_in = st.text_input("E-Mail", placeholder="max@example.com")
                        phone_in = st.text_input(
                            "Telefon (optional)", placeholder="+49 30 …",
                            help="Für eine schnellere Terminvereinbarung",
                        )
                        submitted = st.form_submit_button(
                            "Beratungsgespräch vereinbaren",
                            type="primary", use_container_width=True,
                        )
                        if submitted:
                            if "@" in email_in and "." in email_in:
                                st.session_state.email = email_in
                                st.session_state.lead_captured = True
                                st.rerun()
                            else:
                                st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")

                    st.caption("Ein Senior LIQID Advisor meldet sich innerhalb von 1 Werktag persönlich.")

                else:
                    # Path B: Earlier-stage lead — soft CTA, automated nurture
                    st.markdown("""
                    <div class="liqid-lead-card">
                      <div class="liqid-lead-title">Vollständigen Portfolio-Report erhalten</div>
                      <div class="liqid-lead-sub">
                        Ihre detaillierte Analyse inklusive Benchmark-Vergleich, Asset-Klassen-Breakdown
                        und konkreter Optimierungsszenarien — direkt in Ihr Postfach.
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.form("nurture_form"):
                        email_in = st.text_input("Ihre E-Mail-Adresse", placeholder="name@example.com")
                        submitted = st.form_submit_button(
                            "Report anfordern",
                            type="primary", use_container_width=True,
                        )
                        if submitted:
                            if "@" in email_in and "." in email_in:
                                st.session_state.email = email_in
                                st.session_state.lead_captured = True
                                st.rerun()
                            else:
                                st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")

                    st.caption("Automatischer Versand innerhalb von 2 Minuten. Kein Verkaufsgespräch.")

            else:
                # Lead captured
                if st.session_state.cta_path == "rm":
                    st.success(
                        f"**Beratungstermin angefragt.** "
                        f"Ein Senior LIQID Advisor meldet sich innerhalb von 1 Werktag "
                        f"persönlich unter **{st.session_state.email}**."
                    )
                else:
                    st.success(
                        f"**Report wird zugestellt.** "
                        f"Ihre vollständige Portfolio-Analyse wurde an **{st.session_state.email}** gesendet."
                    )
                st.balloons()

        # ── Reset ──────────────────────────────────────────────────────────────
        st.markdown("---")
        if st.button("← Neues Portfolio analysieren"):
            for k, v in _defaults.items():
                st.session_state[k] = v
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# INTERNAL SCORING PANEL (right column — not part of user-facing experience)
# ════════════════════════════════════════════════════════════════════════════
with col_funnel:
    st.markdown('<div class="liqid-funnel-label">Internes Scoring</div>', unsafe_allow_html=True)

    if not st.session_state.analyzed:
        st.markdown("""
        <div class="score-note">
          Dieses Panel zeigt das stille Lead-Scoring, das dem Nutzer nicht angezeigt wird.<br><br>
          Wählen Sie ein Demo-Portfolio oder laden Sie einen Depotauszug hoch.
        </div>
        """, unsafe_allow_html=True)

    else:
        portfolio = st.session_state.portfolio or {}
        wt = portfolio.get("wealth_tier", "—")
        soph = portfolio.get("sophistication", "—")
        ev = portfolio.get("estimated_value", 0)
        cta = st.session_state.cta_path

        # Wealth tier badge
        wt_color = {"UHNW": "#460f28", "HNW": "#1a7340", "EMERGING_HNW": "#2c4ab5"}.get(wt, "#232425")
        st.markdown(f"""
        <div style="margin-bottom:1.25rem">
          <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.4rem">Vermögenstier</div>
          <div class="score-badge" style="background:{wt_color}">{wt}</div>
        </div>
        """, unsafe_allow_html=True)

        # Sophistication
        soph_color = {"HIGH": "#1a7340", "MEDIUM": "#b87c10", "LOW": "#787878"}.get(soph, "#232425")
        st.markdown(f"""
        <div style="margin-bottom:1.25rem">
          <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.4rem">Sophistication</div>
          <div class="score-badge" style="background:{soph_color}">{soph}</div>
        </div>
        """, unsafe_allow_html=True)

        if ev:
            st.metric("AUM (geschätzt)", format_value(ev))

        st.metric("Risikoprofil", portfolio.get("risk_inferred", "—"))

        if cta:
            st.markdown("---")
            cta_label = "RM Direct" if cta == "rm" else "Nurture-Sequenz"
            cta_icon  = "🎯" if cta == "rm" else "📧"
            cta_color = "#1a7340" if cta == "rm" else "#2c4ab5"
            st.markdown(f"""
            <div style="margin-bottom:0.75rem">
              <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.4rem">CTA-Routing</div>
              <div class="score-badge" style="background:{cta_color}">{cta_icon} {cta_label}</div>
            </div>
            <div class="score-note">
              Der Nutzer sieht keine Routing-Entscheidung — nur ein CTA, das zu seinem Profil passt.
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.narrative:
            st.markdown("---")
            st.markdown(
                '<div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.75rem">Pipeline</div>',
                unsafe_allow_html=True,
            )
            st.metric("Extraktion", "✓")
            st.metric("Narrative", "✓ Streaming")
            lead_status = "✓ Konvertiert" if st.session_state.lead_captured else "○ Ausstehend"
            lead_delta  = "Lead captured" if st.session_state.lead_captured else None
            st.metric("Lead", lead_status, delta=lead_delta)

            gap_df = st.session_state.gap_df
            if gap_df is not None:
                st.markdown("---")
                biggest = gap_df.loc[gap_df["Gap (pp)"].abs().idxmax()]
                st.caption("**Größter Gap**")
                st.metric(biggest["Asset-Klasse"], f"{biggest['Gap (pp)']:+.0f}pp")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="liqid-footer">
  <div class="liqid-footer-logo">LIQID</div>
  <div class="liqid-footer-text">
    Smart Minds. Smart Money. &nbsp;·&nbsp; © 2026 LIQID Asset Management GmbH &nbsp;·&nbsp;
    Prototype — nicht für den öffentlichen Vertrieb bestimmt.
  </div>
</div>
""", unsafe_allow_html=True)
