"""
AI Investment Outlook Generator — Wealth Management Lead Gen Demo
LIQID-faithful redesign: announcement bar · navbar · hero · pillars · cards
"""

import streamlit as st
import anthropic
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Minds. Smart Money. | LIQID",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles + LIQID chrome ─────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Fonts ─────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

html, body, [class*="css"], [data-testid] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ─── Hide Streamlit chrome ─────────────────────────────────────────────── */
#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ─── App background ────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background-color: #ffffff;
}
/* Push content below fixed navbar (announcement 36px + nav 64px) */
[data-testid="stMain"] > .block-container {
  padding-top: 8px !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
  max-width: 1214px;
  margin: 0 auto;
}

/* ─── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background-color: #460f28 !important;
  top: 0 !important;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background-color: rgba(255,255,255,0.12) !important;
  border-color: rgba(255,255,255,0.25) !important;
}
[data-testid="stSidebar"] [data-baseweb="popover"] { background-color: #5c1535 !important; }
[data-testid="stSidebar"] [role="option"] { color: #ffffff !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
  background-color: #ffffff !important;
}

/* ─── Typography ─────────────────────────────────────────────────────────── */
h1, h2, h3, h4 {
  color: #232425 !important;
  font-weight: 500 !important;
  letter-spacing: -0.02em;
  text-wrap: balance;
}
p, li, label { color: #232425; font-weight: 400; line-height: 1.6; }

/* ─── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
  background-color: #232425 !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 2px !important;
  font-weight: 500 !important;
  font-size: 0.875rem !important;
  letter-spacing: 0.01em !important;
  padding: 0.65rem 1.75rem !important;
  transition: background-color 0.3s ease, transform 0.15s ease !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
  background-color: #460f28 !important;
  transform: translateY(-1px);
}
.stButton > button[kind="primary"]:disabled {
  background-color: #c3c3c4 !important;
  color: #787878 !important;
  transform: none !important;
}
.stButton > button:not([kind="primary"]) {
  border: 1.5px solid #232425 !important;
  color: #232425 !important;
  border-radius: 2px !important;
  font-weight: 500 !important;
  background: transparent !important;
  transition: all 0.3s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
  background-color: #232425 !important;
  color: #ffffff !important;
}

/* ─── Inputs ─────────────────────────────────────────────────────────────── */
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div {
  border-radius: 2px !important;
  border-color: #c3c3c4 !important;
  transition: border-color 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
[data-baseweb="input"] > div:focus-within,
[data-baseweb="textarea"] > div:focus-within {
  border-color: #460f28 !important;
  box-shadow: 0 0 0 2px rgba(70,15,40,0.12) !important;
}

/* ─── Metrics ────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: #f9f9f9;
  border: 1px solid #ececec;
  border-radius: 2px;
  padding: 1rem 1.25rem;
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

/* ─── Alerts / dividers ──────────────────────────────────────────────────── */
hr { border-color: #ececec !important; }
[data-testid="stAlert"] { border-radius: 2px !important; border-left-width: 3px !important; }

/* ─── DataFrame ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border: 1px solid #ececec !important; border-radius: 2px !important; }

/* ─── Spinner ────────────────────────────────────────────────────────────── */
[data-testid="stSpinner"] > div { border-top-color: #460f28 !important; }

/* ─── Caption ────────────────────────────────────────────────────────────── */
small, .stCaption, [data-testid="stCaptionContainer"] {
  color: #787878 !important; font-size: 0.75rem !important;
}

/* ─── LIQID Announcement bar ─────────────────────────────────────────────── */
.liqid-bar {
  background-color: #460f28;
  color: #fff;
  text-align: center;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  padding: 0.5rem 1rem;
  position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
  overflow: hidden;
}
.liqid-bar a { color: #fff; text-decoration: underline; }
.liqid-bar-shine {
  position: absolute; top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  animation: shineMove 3.5s linear infinite;
}
@keyframes shineMove { to { left: 160%; } }

/* ─── LIQID Navbar ───────────────────────────────────────────────────────── */
.liqid-nav {
  position: fixed; top: 36px; left: 0; right: 0; z-index: 9998;
  background: #ffffff;
  border-bottom: 1px solid #ececec;
  box-shadow: 0px 15px 10px -15px rgba(0,0,0,0.08);
}
.liqid-nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  max-width: 1214px; margin: 0 auto;
  padding: 0 2rem; height: 64px;
}
.liqid-logo {
  font-size: 1.2rem; font-weight: 700; letter-spacing: 0.15em;
  color: #460f28 !important; text-decoration: none;
}
.liqid-nav-links {
  display: flex; gap: 2rem; list-style: none; margin: 0; padding: 0;
}
.liqid-nav-links a {
  font-size: 0.875rem; font-weight: 400; color: #232425;
  text-decoration: none; transition: color 0.2s ease;
}
.liqid-nav-links a:hover { color: #460f28; }
.liqid-nav-buttons { display: flex; gap: 0.75rem; align-items: center; }
.liqid-btn-secondary {
  font-size: 0.8rem; font-weight: 500;
  border: 1.5px solid #232425; color: #232425;
  padding: 0.45rem 1.1rem; border-radius: 2px;
  text-decoration: none; transition: all 0.25s ease;
}
.liqid-btn-secondary:hover { background: #232425; color: #fff; }
.liqid-btn-primary {
  font-size: 0.8rem; font-weight: 500;
  background: #232425; color: #fff;
  padding: 0.45rem 1.1rem; border-radius: 2px;
  text-decoration: none; transition: background 0.25s ease;
}
.liqid-btn-primary:hover { background: #460f28; }

/* ─── Content offset below fixed bars ────────────────────────────────────── */
.liqid-spacer { height: 100px; }

/* ─── Hero section ───────────────────────────────────────────────────────── */
.liqid-hero {
  padding: 4rem 0 2.5rem;
  border-bottom: 1px solid #ececec;
  margin-bottom: 3rem;
}
.liqid-hero-eyebrow {
  font-size: 0.7rem; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.75rem;
}
.liqid-hero h1 {
  font-size: clamp(2rem, 3.5vw, 3rem) !important;
  font-weight: 500 !important; line-height: 1.15; letter-spacing: -0.03em;
  color: #232425 !important; margin: 0 0 1.25rem;
}
.liqid-hero-sub {
  font-size: 1.05rem; color: #2f3030; line-height: 1.7;
  max-width: 560px; margin-bottom: 2rem;
}
.liqid-hero-disclaimer {
  font-size: 0.7rem; color: #787878; margin-top: 1.5rem;
  padding-top: 1rem; border-top: 1px solid #ececec;
}

/* ─── Three pillars ──────────────────────────────────────────────────────── */
.liqid-pillars {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem; padding: 2.5rem 0; border-bottom: 1px solid #ececec;
  margin-bottom: 2.5rem;
}
.liqid-pillar-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.5rem;
}
.liqid-pillar-title {
  font-size: 1.1rem; font-weight: 500; color: #232425;
  margin-bottom: 0.5rem;
}
.liqid-pillar-text { font-size: 0.875rem; color: #2f3030; line-height: 1.6; }

/* ─── Section heading ────────────────────────────────────────────────────── */
.liqid-section-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.4rem;
}
.liqid-section-title {
  font-size: 1.4rem; font-weight: 500; color: #232425;
  letter-spacing: -0.02em; margin-bottom: 1.75rem;
}

/* ─── Result cards ───────────────────────────────────────────────────────── */
.liqid-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.liqid-card {
  border: 1px solid #ececec; border-radius: 2px; padding: 1.25rem;
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  background: #fff;
}
.liqid-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.06); transform: translateY(-2px); }
.liqid-card-badge {
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878;
  background: #f4f4f4; display: inline-block;
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

/* ─── Quote / dark section ───────────────────────────────────────────────── */
.liqid-quote {
  background: #460f28; color: #fff;
  padding: 2.5rem; border-radius: 2px;
  margin: 2rem 0;
}
.liqid-quote-text {
  font-size: clamp(1.2rem, 2.5vw, 1.75rem);
  font-weight: 300; font-style: italic;
  line-height: 1.4; color: #fff;
}
.liqid-quote-source { font-size: 0.75rem; color: rgba(255,255,255,0.6); margin-top: 1rem; }

/* ─── Lead capture card ──────────────────────────────────────────────────── */
.liqid-lead-card {
  border: 1px solid #ececec; border-radius: 2px;
  padding: 2rem; background: #f9f9f9; margin-top: 1.5rem;
}
.liqid-lead-title { font-size: 1.1rem; font-weight: 500; color: #232425; margin-bottom: 0.4rem; }
.liqid-lead-sub   { font-size: 0.875rem; color: #787878; margin-bottom: 1.25rem; }

/* ─── Funnel panel ───────────────────────────────────────────────────────── */
.liqid-funnel-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 1rem;
  padding-bottom: 0.5rem; border-bottom: 1px solid #ececec;
}

/* ─── Footer ─────────────────────────────────────────────────────────────── */
.liqid-footer {
  margin-top: 4rem; padding: 2rem 0;
  border-top: 1px solid #ececec;
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 1rem;
}
.liqid-footer-logo { font-size: 0.9rem; font-weight: 700; letter-spacing: 0.15em; color: #460f28; }
.liqid-footer-text { font-size: 0.7rem; color: #787878; }
</style>

<!-- ─── Announcement bar ─────────────────────────────────────────────────── -->
<div class="liqid-bar">
  <div class="liqid-bar-shine"></div>
  Ruhe statt Börsenrauschen: Unsere Performance im Vergleich &rarr;
</div>

<!-- ─── Navbar ────────────────────────────────────────────────────────────── -->
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

<!-- ─── Spacer for fixed bars ─────────────────────────────────────────────── -->
<div class="liqid-spacer"></div>

<!-- ─── Hero ──────────────────────────────────────────────────────────────── -->
<div class="liqid-hero">
  <div class="liqid-hero-eyebrow">KI-gestützte Portfolio-Analyse</div>
  <h1>Noise Cancelling<br>für Ihr Portfolio</h1>
  <p class="liqid-hero-sub">
    Ausgezeichnete Analysen für anspruchsvolle Anleger, die ihr Vermögen professionell
    schützen und ausbauen möchten – powered by Claude AI.
  </p>
  <p class="liqid-hero-disclaimer">
    <strong>MiFID II:</strong> Dies ist keine Anlageberatung. Alle Inhalte dienen ausschließlich
    zu Informationszwecken und stellen keine individuelle Anlageempfehlung dar.
  </p>
</div>

<!-- ─── Three pillars ────────────────────────────────────────────────────── -->
<div class="liqid-pillars">
  <div>
    <div class="liqid-pillar-label">Qualität</div>
    <div class="liqid-pillar-title">Professionell</div>
    <p class="liqid-pillar-text">Sie profitieren von Analysen, die höchste Anforderungen erfüllen – und bisher nur sehr großen Vermögen offen standen.</p>
  </div>
  <div>
    <div class="liqid-pillar-label">Beratung</div>
    <div class="liqid-pillar-title">Persönlich</div>
    <p class="liqid-pillar-text">Ihr Profil wird individuell und ohne Verkaufsdruck ausgewertet – abgestimmt auf Ihre Ziele und Ihren Anlagehorizont.</p>
  </div>
  <div>
    <div class="liqid-pillar-label">Technologie</div>
    <div class="liqid-pillar-title">Smart</div>
    <p class="liqid-pillar-text">Sie erhalten Ihre Analyse in Sekunden – kostenlos, datengestützt und direkt umsetzbar.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "inputs_submitted": False,
    "report_generated": False,
    "qualified_lead": False,
    "gap_df": None,
    "narrative": "",
    "email": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar — Investor profile ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Ihr Investor-Profil")
    st.markdown("---")

    assets = st.slider(
        "Investierbare Assets",
        min_value=100_000,
        max_value=5_000_000,
        value=500_000,
        step=50_000,
        format="€%,d",
    )

    risk = st.selectbox(
        "Risikoprofil",
        ["Konservativ", "Ausgewogen", "Wachstumsorientiert"],
        index=1,
    )
    # Map German labels to internal keys
    RISK_MAP = {"Konservativ": "Conservative", "Ausgewogen": "Balanced", "Wachstumsorientiert": "Aggressive"}

    goals = st.multiselect(
        "Anlageziele",
        ["Wachstum", "Einkommen", "Kapitalerhalt", "ESG / Nachhaltigkeit", "Liquidität"],
        default=["Wachstum", "Kapitalerhalt"],
    )

    st.markdown("---")
    st.caption("Powered by Claude AI · Nur zu Demonstrationszwecken")

# ── Data ──────────────────────────────────────────────────────────────────────
MOCK_CURRENT = {
    "Aktien":         {"Conservative": 20, "Balanced": 45, "Aggressive": 70},
    "Anleihen":       {"Conservative": 55, "Balanced": 35, "Aggressive": 10},
    "Alternatives":   {"Conservative": 10, "Balanced": 10, "Aggressive": 12},
    "Liquidität":     {"Conservative": 15, "Balanced": 10, "Aggressive":  8},
}
TARGET_RANGES = {
    "Conservative": {"Aktien": 25, "Anleihen": 50, "Alternatives": 15, "Liquidität": 10},
    "Balanced":     {"Aktien": 55, "Anleihen": 28, "Alternatives": 12, "Liquidität":  5},
    "Aggressive":   {"Aktien": 75, "Anleihen":  8, "Alternatives": 12, "Liquidität":  5},
}

def build_gap_df(risk_key: str) -> pd.DataFrame:
    rows = []
    for ac in ["Aktien", "Anleihen", "Alternatives", "Liquidität"]:
        cur = MOCK_CURRENT[ac][risk_key]
        tgt = TARGET_RANGES[risk_key][ac]
        gap = tgt - cur
        rows.append({
            "Asset-Klasse": ac,
            "Aktuell (%)": cur,
            "Ziel (%)": tgt,
            "Gap (pp)": gap,
            "Empfehlung": "Erhöhen ▲" if gap > 0 else ("Reduzieren ▼" if gap < 0 else "On target ✓"),
        })
    return pd.DataFrame(rows)

def style_gap(val):
    if isinstance(val, (int, float)):
        if val > 0: return "color:#1a7340;font-weight:600"
        if val < 0: return "color:#c0392b;font-weight:600"
    return ""

# ── Layout: main + funnel sidebar ────────────────────────────────────────────
col_main, col_funnel = st.columns([3, 1])

with col_main:
    # Section heading
    st.markdown("""
    <div class="liqid-section-label">Portfolio-Analyse</div>
    <div class="liqid-section-title">Ihr persönlicher Gap-Report</div>
    """, unsafe_allow_html=True)

    generate_clicked = st.button(
        "Analyse starten",
        type="primary",
        use_container_width=True,
        disabled=len(goals) == 0,
    )

    if len(goals) == 0:
        st.info("Bitte wählen Sie mindestens ein Anlageziel in der Seitenleiste.")

    if generate_clicked:
        st.session_state.inputs_submitted = True
        st.session_state.report_generated = False
        st.session_state.gap_df = None
        st.session_state.narrative = ""

        risk_key = RISK_MAP[risk]
        gap_df = build_gap_df(risk_key)
        st.session_state.gap_df = gap_df

        goals_str = ", ".join(goals)
        assets_fmt = f"€{assets:,.0f}"

        prompt = f"""You are a senior wealth management advisor generating a concise portfolio gap analysis.

Client profile:
- Investable assets: {assets_fmt}
- Risk appetite: {risk} ({risk_key})
- Investment goals: {goals_str}

The following allocation gap data has been calculated (use EXACTLY these numbers — do not invent different figures):

{gap_df.to_string(index=False)}

Tasks:
1. Write a 2-3 sentence executive summary of the current vs. target allocation gap.
2. For each asset class with a non-zero gap, give one specific, actionable recommendation (1 sentence each).
3. Close with one sentence on how these adjustments align with the client's stated goals.

Keep the tone professional but accessible. Respond in German. Do not add disclaimers.
Do NOT use markdown formatting, headers (#, ##), or bullet points. Write in plain paragraphs only."""

        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
            client_ai = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

            with st.spinner("Claude AI analysiert Ihr Portfolio…"):
                narrative_ph = st.empty()
                full_text = ""

                with client_ai.messages.stream(
                    model="claude-opus-4-6",
                    max_tokens=1024,
                    thinking={"type": "adaptive"},
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    for text in stream.text_stream:
                        full_text += text
                        narrative_ph.markdown(full_text + "▌")

                narrative_ph.empty()
                st.session_state.narrative = full_text
                st.session_state.report_generated = True

        except anthropic.AuthenticationError:
            st.error("API-Key ungültig oder fehlend. Bitte in `.streamlit/secrets.toml` hinterlegen.")
        except Exception as e:
            st.error(f"Fehler beim Aufruf der Claude API: {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.report_generated and st.session_state.gap_df is not None:
        gap_df = st.session_state.gap_df

        # Card grid for gap results
        cards_html = '<div class="liqid-cards">'
        for _, row in gap_df.iterrows():
            gap = row["Gap (pp)"]
            if gap > 0:
                badge_cls, badge_txt, gap_cls = "increase", "Erhöhen", "pos"
            elif gap < 0:
                badge_cls, badge_txt, gap_cls = "reduce", "Reduzieren", "neg"
            else:
                badge_cls, badge_txt, gap_cls = "ontarget", "On target", "zero"

            cards_html += f"""
            <div class="liqid-card">
              <div class="liqid-card-badge {badge_cls}">{badge_txt}</div>
              <div class="liqid-card-asset">{row['Asset-Klasse']}</div>
              <div class="liqid-card-gap {gap_cls}">{gap:+.0f} pp</div>
              <div class="liqid-card-meta">Aktuell {row['Aktuell (%)']:.0f}% → Ziel {row['Ziel (%)']:.0f}%</div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        # Full table (collapsed detail)
        with st.expander("Detailtabelle anzeigen"):
            styled = (
                gap_df.style
                .applymap(style_gap, subset=["Gap (pp)"])
                .format({"Aktuell (%)": "{:.0f}%", "Ziel (%)": "{:.0f}%", "Gap (pp)": "{:+.0f}pp"})
            )
            st.dataframe(styled, use_container_width=True, hide_index=True)

        # AI narrative in quote style
        if st.session_state.narrative:
            st.markdown(f"""
            <div class="liqid-quote">
              <div class="liqid-quote-text">„{st.session_state.narrative}"</div>
              <div class="liqid-quote-source">Claude AI · Wealth Management Advisor</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Lead capture
        if not st.session_state.qualified_lead:
            st.markdown("""
            <div class="liqid-lead-card">
              <div class="liqid-lead-title">Vollständigen Report erhalten</div>
              <div class="liqid-lead-sub">Ein persönlicher Berater meldet sich innerhalb von 24 Stunden.</div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("lead_form"):
                email_input = st.text_input("Ihre E-Mail-Adresse", placeholder="name@example.com")
                if st.form_submit_button("Report zusenden", type="primary", use_container_width=True):
                    if "@" in email_input and "." in email_input:
                        st.session_state.email = email_input
                        st.session_state.qualified_lead = True
                        st.rerun()
                    else:
                        st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")
        else:
            st.success(
                f"**Lead qualifiziert.** Report wird an **{st.session_state.email}** gesendet. "
                "Ein Berater meldet sich innerhalb von 24 Stunden."
            )
            st.balloons()

# ── Funnel metrics column ─────────────────────────────────────────────────────
with col_funnel:
    st.markdown('<div class="liqid-funnel-label">Lead-Funnel</div>', unsafe_allow_html=True)
    st.metric("Views", 1)
    st.metric("Eingaben", 1 if st.session_state.inputs_submitted else 0,
              delta="Aktiv" if st.session_state.inputs_submitted else None)
    st.metric("Reports", 1 if st.session_state.report_generated else 0,
              delta="Erstellt" if st.session_state.report_generated else None)
    st.metric("Leads", 1 if st.session_state.qualified_lead else 0,
              delta="Qualifiziert" if st.session_state.qualified_lead else None)

    if st.session_state.report_generated and st.session_state.gap_df is not None:
        gap_df = st.session_state.gap_df
        top = gap_df.loc[gap_df["Gap (pp)"].abs().idxmax()]
        st.markdown("---")
        st.caption("**Größter Gap**")
        st.metric(top["Asset-Klasse"], f"{top['Gap (pp)']:+.0f}pp")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="liqid-footer">
  <div class="liqid-footer-logo">LIQID</div>
  <div class="liqid-footer-text">
    Smart Minds. Smart Money. · © 2026 LIQID Asset Management GmbH ·
    Dies ist kein echtes LIQID-Produkt – nur eine Demonstrationsanwendung.
  </div>
</div>
""", unsafe_allow_html=True)
