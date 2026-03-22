"""
Shared CSS, data, and helpers — imported by home.py and analyse.py
"""
import streamlit as st
import anthropic
import pandas as pd
import pathlib


# ── Shared CSS injection ──────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,300&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

html, body, [class*="css"], [data-testid] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #ffffff; }
[data-testid="stMain"] > .block-container {
  padding-top: 8px !important; padding-left: 2rem !important;
  padding-right: 2rem !important; max-width: 1214px; margin: 0 auto;
}
[data-testid="stSidebar"] { display: none !important; }

/* ─── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
  background-color: #232425 !important; color: #fff !important;
  border: none !important; border-radius: 2px !important;
  font-weight: 500 !important; font-size: 0.875rem !important;
  padding: 0.65rem 1.75rem !important; transition: background-color 0.3s ease !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover { background-color: #460f28 !important; }
.stButton > button:not([kind="primary"]) {
  border: 1.5px solid #232425 !important; color: #232425 !important;
  border-radius: 2px !important; font-weight: 500 !important;
  background: transparent !important; transition: all 0.3s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
  background-color: #232425 !important; color: #fff !important;
}

/* ─── Inputs ──────────────────────────────────────────────────────────────── */
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div {
  border-radius: 2px !important; border-color: #c3c3c4 !important;
}
[data-baseweb="input"] > div:focus-within,
[data-baseweb="textarea"] > div:focus-within {
  border-color: #460f28 !important; box-shadow: 0 0 0 2px rgba(70,15,40,0.12) !important;
}

/* ─── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: #f9f9f9; border: 1px solid #ececec; border-radius: 2px; padding: 1rem 1.25rem;
}
[data-testid="stMetricLabel"] {
  font-size: 0.7rem !important; font-weight: 500 !important; color: #787878 !important;
  letter-spacing: 0.08em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] { color: #232425 !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] > div {
  color: #460f28 !important; font-size: 0.75rem !important; font-weight: 500 !important;
}
hr { border-color: #ececec !important; }
[data-testid="stAlert"] { border-radius: 2px !important; border-left-width: 3px !important; }
[data-testid="stSpinner"] > div { border-top-color: #460f28 !important; }
small, .stCaption, [data-testid="stCaptionContainer"] {
  color: #787878 !important; font-size: 0.75rem !important;
}
[data-testid="stFileUploaderDropzone"] {
  border: 2px dashed #c3c3c4 !important; border-radius: 2px !important;
  background: #f9f9f9 !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: #460f28 !important; }

/* ─── Shared navbar ───────────────────────────────────────────────────────── */
.liqid-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  background: #fff; border-bottom: 1px solid #ececec;
  box-shadow: 0 1px 0 0 #ececec;
}
.liqid-nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  max-width: 1214px; margin: 0 auto; padding: 0 2rem; height: 68px;
}
.liqid-logo {
  font-size: 1.2rem; font-weight: 700; letter-spacing: 0.15em;
  color: #d0021b !important; text-decoration: none; flex-shrink: 0;
}
.liqid-nav-links {
  display: flex; gap: 1.75rem; list-style: none; margin: 0; padding: 0; align-items: center;
}
.liqid-nav-links a {
  font-size: 0.875rem; font-weight: 400; color: #232425;
  text-decoration: none; transition: color 0.2s; white-space: nowrap;
}
.liqid-nav-links a:hover { color: #d0021b; }
.liqid-nav-cta {
  font-size: 0.78rem; font-weight: 500; color: #460f28 !important;
  border: 1.5px solid #460f28; border-radius: 2px;
  padding: 0.35rem 0.85rem; text-decoration: none !important;
  transition: all 0.25s ease; white-space: nowrap; display: inline-block;
}
.liqid-nav-cta:hover { background: #460f28 !important; color: #fff !important; }
.liqid-nav-cta.active { background: #460f28; color: #fff !important; }
.liqid-nav-buttons { display: flex; gap: 0.75rem; align-items: center; flex-shrink: 0; }
.liqid-btn-secondary {
  font-size: 0.8rem; font-weight: 400; color: #232425;
  padding: 0.45rem 1rem; text-decoration: none; transition: color 0.2s;
}
.liqid-btn-secondary:hover { color: #460f28; }
.liqid-btn-primary {
  font-size: 0.8rem; font-weight: 500; background: #460f28; color: #fff !important;
  padding: 0.5rem 1.25rem; border-radius: 2px; text-decoration: none !important;
  transition: background 0.25s ease;
}
.liqid-btn-primary:hover { background: #6b1a3d; }

/* ─── Announcement bar (below navbar) ────────────────────────────────────── */
.liqid-bar {
  position: fixed; top: 68px; left: 0; right: 0; z-index: 9998;
  background-color: #460f28; color: #fff; text-align: center;
  font-size: 0.75rem; font-weight: 400; padding: 0.6rem 1rem;
  overflow: hidden;
}
.liqid-bar a { color: #fff; text-decoration: none; }
.liqid-bar a:hover { text-decoration: underline; }
.liqid-bar-shine {
  position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
  animation: shineMove 4s linear infinite;
}
@keyframes shineMove { to { left: 160%; } }

/* ─── Spacer (navbar 68 + bar 36 = 104px) ────────────────────────────────── */
.liqid-spacer { height: 104px; }

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
.liqid-card-asset { font-size: 1rem; font-weight: 500; color: #232425; margin-bottom: 0.4rem; }
.liqid-card-gap   { font-size: 1.6rem; font-weight: 300; letter-spacing: -0.02em; }
.liqid-card-gap.pos  { color: #1a7340; }
.liqid-card-gap.neg  { color: #c0392b; }
.liqid-card-gap.zero { color: #2c4ab5; }
.liqid-card-meta  { font-size: 0.75rem; color: #787878; margin-top: 0.5rem; }

/* ─── Quote block ─────────────────────────────────────────────────────────── */
.liqid-quote {
  background: #460f28; color: #fff; padding: 2.5rem; border-radius: 2px; margin: 2rem 0;
}
.liqid-quote-text {
  font-size: clamp(1rem, 2.2vw, 1.5rem); font-weight: 300; font-style: italic;
  line-height: 1.55; color: #fff;
}
.liqid-quote-source { font-size: 0.75rem; color: rgba(255,255,255,0.55); margin-top: 1rem; }

/* ─── Lead card ───────────────────────────────────────────────────────────── */
.liqid-lead-card {
  border: 1px solid #ececec; border-radius: 2px; padding: 2rem;
  background: #f9f9f9; margin-top: 1.5rem;
}
.liqid-lead-card.rm-path { border-color: #232425; background: #fff; }
.liqid-rm-badge {
  display: inline-block; background: #232425; color: #fff;
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
  padding: 0.2rem 0.6rem; border-radius: 1px; margin-bottom: 1rem;
}
.liqid-lead-title { font-size: 1.1rem; font-weight: 500; color: #232425; margin-bottom: 0.4rem; }
.liqid-lead-sub   { font-size: 0.875rem; color: #787878; margin-bottom: 1.25rem; line-height: 1.6; }

/* ─── Section labels ──────────────────────────────────────────────────────── */
.liqid-section-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.4rem;
}
.liqid-section-title {
  font-size: 1.4rem; font-weight: 500; color: #232425;
  letter-spacing: -0.02em; margin-bottom: 0.5rem;
}
.liqid-section-sub { font-size: 0.875rem; color: #787878; margin-bottom: 1.75rem; }

/* ─── Stream preview ──────────────────────────────────────────────────────── */
.stream-preview {
  padding: 1.25rem; background: #f9f9f9; border-radius: 2px;
  color: #232425; font-size: 0.9rem; line-height: 1.7; min-height: 60px;
}

/* ─── Internal scoring ────────────────────────────────────────────────────── */
.liqid-funnel-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
  color: #787878; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #ececec;
}
.score-badge {
  display: inline-block; padding: 0.3rem 0.75rem; border-radius: 2px;
  font-size: 0.8rem; font-weight: 500; color: #fff; margin-bottom: 0.25rem;
}
.score-note { font-size: 0.7rem; color: #787878; line-height: 1.5; font-style: italic; }

/* ─── Footer ──────────────────────────────────────────────────────────────── */
.liqid-footer {
  margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #ececec;
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 1rem;
}
.liqid-footer-logo { font-size: 0.9rem; font-weight: 700; letter-spacing: 0.15em; color: #d0021b; }
.liqid-footer-text { font-size: 0.7rem; color: #787878; }
</style>
""", unsafe_allow_html=True)


def inject_chrome(active: str = "home"):
    """Render the fixed navbar + announcement bar. active = 'home' | 'analyse'"""
    cta_class = "liqid-nav-cta active" if active == "analyse" else "liqid-nav-cta"
    st.markdown(f"""
<nav class="liqid-nav">
  <div class="liqid-nav-inner">
    <a class="liqid-logo" href="/">LIQID</a>
    <ul class="liqid-nav-links">
      <li><a href="#">Lösungen</a></li>
      <li><a href="#">Über uns</a></li>
      <li><a href="#">Wissen</a></li>
      <li><a href="#">Kontakt</a></li>
      <li>
        <a href="/portfolio-analyse" class="{cta_class}">
          Vergleich dich mit bestehenden LIQID Kunden
        </a>
      </li>
    </ul>
    <div class="liqid-nav-buttons">
      <a class="liqid-btn-secondary" href="#">Einloggen</a>
      <a class="liqid-btn-primary" href="#">Jetzt investieren</a>
    </div>
  </div>
</nav>

<div class="liqid-bar">
  <div class="liqid-bar-shine"></div>
  Ruhe statt Börsenrauschen: Unsere Performance im Vergleich &rarr;
</div>

<div class="liqid-spacer"></div>
""", unsafe_allow_html=True)


# ── Shared data ───────────────────────────────────────────────────────────────
DEMO_PERSONAS = {
    "Marcus K.": {
        "subtitle": "Tech-Gründer · €1.85M · Post-Exit, konzentriert",
        "description": "SAP-Aktienoptionen + Krypto-Allocation + Cash-Überhang nach IPO-Exit",
        "holdings": {"Aktien": 58, "Anleihen": 3, "Alternatives": 12, "Liquidität": 27},
        "estimated_value": 1_850_000,
        "holding_names": "SAP SE 28% · NVIDIA Corp 18% · Bitcoin via Coinbase 12% · iShares MSCI World 15% · Barvermögen DKB 27%",
        "sophistication": "HIGH",
        "wealth_tier": "HNW",
        "risk_inferred": "Ambitioniert",
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
        "risk_inferred": "Ambitioniert",
    },
}

BENCHMARKS = {
    "EMERGING_HNW": {
        "Conservative": {"Aktien": 30, "Anleihen": 40, "Alternatives": 12, "Liquidität": 18},
        "Balanced":     {"Aktien": 52, "Anleihen": 25, "Alternatives": 15, "Liquidität": 8},
        "Ambitioniert":   {"Aktien": 70, "Anleihen": 8,  "Alternatives": 15, "Liquidität": 7},
    },
    "HNW": {
        "Conservative": {"Aktien": 25, "Anleihen": 30, "Alternatives": 35, "Liquidität": 10},
        "Balanced":     {"Aktien": 45, "Anleihen": 15, "Alternatives": 35, "Liquidität": 5},
        "Ambitioniert":   {"Aktien": 58, "Anleihen": 5,  "Alternatives": 33, "Liquidität": 4},
    },
    "UHNW": {
        "Conservative": {"Aktien": 20, "Anleihen": 20, "Alternatives": 50, "Liquidität": 10},
        "Balanced":     {"Aktien": 38, "Anleihen": 10, "Alternatives": 48, "Liquidität": 4},
        "Ambitioniert":   {"Aktien": 50, "Anleihen": 3,  "Alternatives": 44, "Liquidität": 3},
    },
}


# ── Shared helpers ────────────────────────────────────────────────────────────
def compute_cta_path(sophistication: str, wealth_tier: str) -> str:
    if sophistication == "HIGH" or wealth_tier in ("HNW", "UHNW"):
        return "rm"
    return "nurture"


def build_gap_df(holdings: dict, benchmark: dict) -> pd.DataFrame:
    rows = []
    for ac in ["Aktien", "Anleihen", "Alternatives", "Liquidität"]:
        cur = holdings.get(ac, 0)
        tgt = benchmark.get(ac, 0)
        rows.append({
            "Asset-Klasse": ac,
            "Ihr Portfolio (%)": cur,
            "Peer-Benchmark (%)": tgt,
            "Gap (pp)": tgt - cur,
        })
    return pd.DataFrame(rows)


def format_value(val: int) -> str:
    if not val:
        return "—"
    if val >= 1_000_000:
        return f"€{val / 1_000_000:.2f}M"
    return f"€{val / 1_000:.0f}K"


def get_client() -> anthropic.Anthropic:
    # Primary: st.secrets (works when Streamlit loads secrets.toml correctly)
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
        if key:
            return anthropic.Anthropic(api_key=key)
    except Exception:
        pass
    # Fallback: read secrets.toml directly from project root
    import os, re
    for base in [os.getcwd(), pathlib.Path(__file__).parent.parent]:
        toml = pathlib.Path(base) / ".streamlit" / "secrets.toml"
        if toml.exists():
            m = re.search(r'ANTHROPIC_API_KEY\s*=\s*["\']([^"\']+)["\']', toml.read_text())
            if m:
                return anthropic.Anthropic(api_key=m.group(1))
    raise RuntimeError("ANTHROPIC_API_KEY nicht gefunden. Bitte in .streamlit/secrets.toml eintragen.")


def build_narrative_prompt(portfolio: dict, gap_df: pd.DataFrame) -> str:
    obs_lines = []
    for _, row in gap_df.iterrows():
        gap = row["Gap (pp)"]
        if abs(gap) > 2:
            direction = "untergewichtet" if gap > 0 else "übergewichtet"
            obs_lines.append(
                f"{row['Asset-Klasse']}: Sie {row['Ihr Portfolio (%)']:.0f}% "
                f"vs. Peers {row['Peer-Benchmark (%)']:.0f}% → {direction} um {abs(gap):.0f}pp"
            )
    observations = "\n".join(obs_lines) or "Portfolio weitgehend im Zielbereich."

    return f"""Du bist Senior Wealth Advisor bei LIQID.

Schreibe eine Portfolio-Gap-Analyse auf Deutsch. Kurz, direkt, auf den Punkt — wie ein erfahrener Advisor der keine Zeit verschwendet.

Portfolio: {portfolio["holding_names"]}
Wert: {format_value(portfolio["estimated_value"])}

Gap vs. Vergleichsgruppe:
{observations}

Schreibe genau 2 Sätze:
1. Der wichtigste Gap — was fehlt konkret und warum ist das relevant.
2. Was institutionelle Anleger dieser Größenordnung anders machen — und was das langfristig bedeutet.

Regeln: Kein "HNW", kein "UHNW", keine internen Begriffe. Kein Markdown. Keine Aufzählungen. Keine Floskeln. Kein LIQID erwähnen. Direkt, präzise, respektvoll."""
