"""
LIQID Landing Page — faithful recreation of liqid.com
"""
import streamlit as st
import pathlib
from shared import inject_styles, inject_chrome

inject_styles()
inject_chrome(active="home")

# ── Landing-page-specific styles ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

/* ─── Hero text side ──────────────────────────────────────────────────────── */
.lp-hero-text {
  padding: 4rem 3rem 4rem 0;
  display: flex; flex-direction: column; justify-content: center;
}
.lp-hero-eyebrow {
  font-size: 0.72rem; font-weight: 500; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 1.25rem;
}
.lp-hero-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.2rem, 4vw, 3.5rem); font-weight: 700;
  line-height: 1.1; color: #1a1a1a; margin: 0 0 1.5rem;
}
.lp-hero-sub {
  font-size: 1rem; color: #444; line-height: 1.7;
  margin-bottom: 2.25rem; max-width: 420px;
}
.lp-hero-cta {
  display: inline-block; background: #1a1a1a; color: #fff !important;
  font-size: 0.875rem; font-weight: 500; padding: 0.85rem 2rem;
  border-radius: 2px; text-decoration: none !important;
  transition: background 0.25s; margin-bottom: 2rem; align-self: flex-start;
}
.lp-hero-cta:hover { background: #460f28 !important; }
.lp-trustpilot { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
.lp-tp-label  { font-size: 0.875rem; font-weight: 600; color: #1a1a1a; }
.lp-tp-score  { font-size: 0.875rem; color: #444; }
.lp-tp-stars  { color: #00b67a; font-size: 1rem; }
.lp-tp-logo   { font-size: 0.75rem; font-weight: 700; color: #1a1a1a; }

/* ─── Stats cards (matching LIQID screenshot) ─────────────────────────────── */
.lp-stats {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 1rem; margin: 2.5rem 0 3.5rem;
}
.lp-stat-card {
  background: #f5f3f0; border-radius: 10px; padding: 1.75rem 1.5rem;
}
.lp-stat-value {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.9rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.4rem;
}
.lp-stat-label { font-size: 0.85rem; color: #555; line-height: 1.4; }

/* ─── Pillars (matching LIQID screenshot) ─────────────────────────────────── */
.lp-pillars {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 3rem; margin-bottom: 4rem;
  border-top: 1px solid #e5e5e5; padding-top: 2.5rem;
}
.lp-pillar-title {
  font-size: 1rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.75rem;
}
.lp-pillar-text { font-size: 0.875rem; color: #555; line-height: 1.7; }
.lp-pillar-footnote { font-size: 0.7rem; color: #888; vertical-align: super; }

/* ─── Dark CTA banner ─────────────────────────────────────────────────────── */
.lp-banner {
  background: #1a1a1a; padding: 4rem 3rem; border-radius: 4px; margin-bottom: 4rem;
  display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap;
}
.lp-banner-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 400;
  color: #fff; margin-bottom: 0.75rem; line-height: 1.3;
}
.lp-banner-sub {
  font-size: 0.9rem; color: rgba(255,255,255,0.65); max-width: 460px; line-height: 1.6;
}
.lp-banner-btn {
  display: inline-block; background: #fff; color: #1a1a1a !important;
  font-size: 0.875rem; font-weight: 600; padding: 0.85rem 2rem;
  border-radius: 2px; text-decoration: none !important; white-space: nowrap;
  transition: background 0.2s ease; flex-shrink: 0;
}
.lp-banner-btn:hover { background: #f0e8e0 !important; }

/* ─── Override Streamlit image container ──────────────────────────────────── */
[data-testid="stImage"] img {
  border-radius: 0 !important;
  display: block;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
  height: 100%;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
hero_left, hero_right = st.columns([1, 1], gap="small")

with hero_left:
    st.markdown("""
    <div class="lp-hero-text">
      <div class="lp-hero-eyebrow">Smart Minds. Smart Money.</div>
      <h1 class="lp-hero-heading">Noise Cancelling<br>für Ihr Vermögen</h1>
      <p class="lp-hero-sub">
        Ausgezeichnete Lösungen für anspruchsvolle Anleger, die ihr Vermögen
        professionell schützen und ausbauen möchten.
      </p>
      <a href="/portfolio-analyse" class="lp-hero-cta">Lösungen entdecken</a>
      <div class="lp-trustpilot">
        <span class="lp-tp-label">Hervorragend</span>
        <span class="lp-tp-stars">★★★★★</span>
        <span class="lp-tp-score">4.6 von 5</span>
        <span class="lp-tp-logo">★ Trustpilot</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    hero_img = pathlib.Path(__file__).parent / "hero.jpg"
    if hero_img.exists():
        st.image(str(hero_img), use_container_width=True)
    else:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#f2e8df 0%,#e0cfc0 20%,#c9b09a 45%,#b09070 65%,#957055 80%,#7a5840 100%);
                    min-height:520px;border-radius:2px;"></div>
        """, unsafe_allow_html=True)

# ── Stats cards — real LIQID data ─────────────────────────────────────────────
st.markdown("""
<div class="lp-stats">
  <div class="lp-stat-card">
    <div class="lp-stat-value">&gt;3,5 Mrd. Euro</div>
    <div class="lp-stat-label">betreutes Kundenvermögen</div>
  </div>
  <div class="lp-stat-card">
    <div class="lp-stat-value">&gt;10.000 Kunden</div>
    <div class="lp-stat-label">in Deutschland und Europa</div>
  </div>
  <div class="lp-stat-card">
    <div class="lp-stat-value">7-fach ausgezeichnet</div>
    <div class="lp-stat-label">vom Wirtschaftsmagazin Capital<sup>2</sup></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Three pillars — real LIQID copy ───────────────────────────────────────────
st.markdown("""
<div class="lp-pillars">
  <div>
    <div class="lp-pillar-title">Professionell</div>
    <p class="lp-pillar-text">
      Sie profitieren von Anlagelösungen, die höchste Anforderungen erfüllen –
      und bisher nur sehr großen Vermögen offen standen.
    </p>
  </div>
  <div>
    <div class="lp-pillar-title">Persönlich</div>
    <p class="lp-pillar-text">
      Sie werden von uns individuell, unabhängig und ohne Verkaufsdruck beraten –
      über den gesamten Anlagezeitraum hinweg.
    </p>
  </div>
  <div>
    <div class="lp-pillar-title">Smart</div>
    <p class="lp-pillar-text">
      Sie investieren bequem digital – mit bis zu 60&nbsp;% niedrigeren Kosten
      als bei klassischen Banken und Fonds.<span class="lp-pillar-footnote">1</span>
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Dark CTA banner ───────────────────────────────────────────────────────────
st.markdown("""
<div class="lp-banner">
  <div>
    <div class="lp-banner-heading">
      Wo steht Ihr Portfolio<br>im Vergleich zu LIQID Kunden?
    </div>
    <p class="lp-banner-sub">
      Laden Sie Ihren Depotauszug hoch. In Sekunden analysiert unsere KI Ihre
      Allokation und vergleicht sie mit dem Benchmark institutioneller Investoren
      Ihrer Vermögensklasse — kostenlos, anonym, ohne Berater.
    </p>
  </div>
  <a href="/portfolio-analyse" class="lp-banner-btn">Jetzt vergleichen →</a>
</div>
""", unsafe_allow_html=True)

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
