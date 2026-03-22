"""
LIQID Landing Page — faithful recreation of liqid.com
"""
import streamlit as st
from shared import inject_styles, inject_chrome

inject_styles()
inject_chrome(active="home")

# ── Landing-page-specific styles ──────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Hero ────────────────────────────────────────────────────────────────── */
.lp-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 82vh;
  margin: 0 -2rem;
  align-items: stretch;
}
.lp-hero-left {
  padding: 5rem 3rem 5rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 600px;
}
.lp-hero-eyebrow {
  font-size: 0.72rem; font-weight: 500; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 1.25rem;
}
.lp-hero-heading {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: clamp(2.4rem, 4.5vw, 3.75rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.01em;
  color: #1a1a1a;
  margin: 0 0 1.5rem;
}
.lp-hero-sub {
  font-size: 1rem; color: #444; line-height: 1.7; margin-bottom: 2.25rem; max-width: 420px;
}
.lp-hero-cta {
  display: inline-block;
  background: #1a1a1a; color: #fff !important;
  font-size: 0.875rem; font-weight: 500;
  padding: 0.85rem 2rem; border-radius: 2px;
  text-decoration: none !important;
  transition: background 0.25s; margin-bottom: 2rem;
}
.lp-hero-cta:hover { background: #460f28 !important; }
.lp-trustpilot {
  display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;
}
.lp-tp-label { font-size: 0.875rem; font-weight: 600; color: #1a1a1a; }
.lp-tp-score { font-size: 0.875rem; color: #444; }
.lp-tp-stars { color: #00b67a; font-size: 1rem; letter-spacing: 0.05em; }
.lp-tp-logo  { font-size: 0.75rem; font-weight: 700; color: #1a1a1a; letter-spacing: 0.05em; }

/* Photo side */
.lp-hero-right {
  background: linear-gradient(145deg,
    #f2e8df 0%,
    #e0cfc0 20%,
    #c9b09a 45%,
    #b09070 65%,
    #957055 80%,
    #7a5840 100%);
  position: relative;
  overflow: hidden;
}
.lp-hero-right::after {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 40% 35%, rgba(255,240,225,0.3) 0%, transparent 60%);
}

/* ─── Stats bar ───────────────────────────────────────────────────────────── */
.lp-stats {
  display: grid; grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid #ececec; border-bottom: 1px solid #ececec;
  padding: 2.5rem 0; margin-bottom: 4rem;
}
.lp-stat { padding: 0 2rem; border-right: 1px solid #ececec; }
.lp-stat:first-child { padding-left: 0; }
.lp-stat:last-child  { border-right: none; }
.lp-stat-value {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2rem; font-weight: 400; color: #1a1a1a; margin-bottom: 0.25rem;
}
.lp-stat-label { font-size: 0.8rem; color: #787878; line-height: 1.4; }

/* ─── Pillars ─────────────────────────────────────────────────────────────── */
.lp-pillars {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 3rem; margin-bottom: 4rem;
}
.lp-pillar-number {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #d0021b; margin-bottom: 1rem;
}
.lp-pillar-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.3rem; font-weight: 400; color: #1a1a1a; margin-bottom: 0.75rem;
}
.lp-pillar-text { font-size: 0.875rem; color: #555; line-height: 1.7; }

/* ─── Dark CTA banner ─────────────────────────────────────────────────────── */
.lp-banner {
  background: #1a1a1a; padding: 4rem 3rem; border-radius: 2px; margin-bottom: 4rem;
  display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap;
}
.lp-banner-text { color: #fff; }
.lp-banner-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 400;
  color: #fff; margin-bottom: 0.75rem; line-height: 1.3;
}
.lp-banner-sub { font-size: 0.9rem; color: rgba(255,255,255,0.65); max-width: 460px; line-height: 1.6; }
.lp-banner-btn {
  display: inline-block; background: #fff; color: #1a1a1a !important;
  font-size: 0.875rem; font-weight: 600; padding: 0.85rem 2rem;
  border-radius: 2px; text-decoration: none !important; white-space: nowrap;
  transition: background 0.2s ease; flex-shrink: 0;
}
.lp-banner-btn:hover { background: #f0e8e0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lp-hero">
  <div class="lp-hero-left">
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
  <div class="lp-hero-right"></div>
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lp-stats">
  <div class="lp-stat">
    <div class="lp-stat-value">€5,2 Mrd.</div>
    <div class="lp-stat-label">verwaltetes Vermögen</div>
  </div>
  <div class="lp-stat">
    <div class="lp-stat-value">12.000+</div>
    <div class="lp-stat-label">Kunden im DACH-Raum</div>
  </div>
  <div class="lp-stat">
    <div class="lp-stat-value">€150K</div>
    <div class="lp-stat-label">Mindestanlage</div>
  </div>
  <div class="lp-stat">
    <div class="lp-stat-value">0,5–1,0%</div>
    <div class="lp-stat-label">p.a. All-in-Fee</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Three pillars ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="lp-pillars">
  <div>
    <div class="lp-pillar-number">01 — Qualität</div>
    <div class="lp-pillar-title">Institutionelle Investments</div>
    <p class="lp-pillar-text">
      Sie profitieren von Anlagestrategien, die bisher nur Family Offices und
      institutionellen Investoren zugänglich waren — ab €150.000 Anlagekapital.
    </p>
  </div>
  <div>
    <div class="lp-pillar-number">02 — Beratung</div>
    <div class="lp-pillar-title">Persönlicher Relationship Manager</div>
    <p class="lp-pillar-text">
      Ihr Vermögen wird von einem dedizierten Berater betreut — digital-first,
      ohne Verkaufsdruck, mit vollständiger Kostentransparenz.
    </p>
  </div>
  <div>
    <div class="lp-pillar-number">03 — Zugang</div>
    <div class="lp-pillar-title">Private Markets & Alternatives</div>
    <p class="lp-pillar-text">
      Private Equity, Venture Capital und Hedgefonds-Strategien — Anlageklassen,
      die das Rendite-Risiko-Profil Ihres Portfolios nachweislich verbessern.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Dark CTA banner ───────────────────────────────────────────────────────────
st.markdown("""
<div class="lp-banner">
  <div class="lp-banner-text">
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
