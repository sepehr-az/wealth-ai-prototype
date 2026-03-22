"""
LIQID | Silent Portfolio Intelligence
AI-Native Lead Qualification Engine — Track A: Growth & Acquisition
"""
import streamlit as st
import json
import base64
import anthropic
from shared import (
    inject_styles, inject_chrome,
    DEMO_PERSONAS, BENCHMARKS,
    compute_cta_path, build_gap_df, format_value,
    get_client, build_narrative_prompt,
)

inject_styles()
inject_chrome(active="analyse")

# ── Analyse-page-specific styles ──────────────────────────────────────────────
st.markdown("""
<style>
.demo-card {
  border: 1px solid #ececec; border-radius: 2px; padding: 1rem;
  margin-bottom: 0.75rem; background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.demo-card:hover { border-color: #460f28; box-shadow: 0 2px 12px rgba(70,15,40,0.08); }
.demo-card-eyebrow {
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.25rem;
}
.demo-card-name { font-size: 0.95rem; font-weight: 500; color: #232425; margin-bottom: 0.2rem; }
.demo-card-sub  { font-size: 0.75rem; color: #787878; line-height: 1.4; }

.analyse-hero {
  padding: 2.5rem 0 2rem; border-bottom: 1px solid #ececec; margin-bottom: 2.5rem;
}
.analyse-hero-eyebrow {
  font-size: 0.7rem; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.75rem;
}
.analyse-hero h1 {
  font-size: clamp(1.75rem, 3vw, 2.5rem) !important; font-weight: 500 !important;
  line-height: 1.2; letter-spacing: -0.02em; color: #232425 !important; margin: 0 0 1rem;
}
.analyse-hero-sub { font-size: 1rem; color: #2f3030; line-height: 1.7; max-width: 520px; }
.analyse-hero-disclaimer {
  font-size: 0.7rem; color: #787878; margin-top: 1.25rem;
  padding-top: 1rem; border-top: 1px solid #ececec;
}
.upload-label {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
_defaults = {
    "analyzed": False,
    "portfolio": None,
    "gap_df": None,
    "narrative": "",
    "cta_path": None,
    "email": "",
    "lead_captured": False,
    "source": None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

col_main, col_funnel = st.columns([3, 1])

# ════════════════════════════════════════════════════════════════════════════
# MAIN COLUMN
# ════════════════════════════════════════════════════════════════════════════
with col_main:

    # ── PHASE 1: Upload / Demo selection ──────────────────────────────────────
    if not st.session_state.analyzed:

        st.markdown("""
        <div class="analyse-hero">
          <div class="analyse-hero-eyebrow">KI-gestützte Portfolio-Analyse</div>
          <h1>Ihr Portfolio.<br>Verglichen mit Ihren Peers.</h1>
          <p class="analyse-hero-sub">
            Laden Sie Ihren Depotauszug hoch — keine Formulare, keine Registrierung.
            Die KI liest Ihre Allokation und vergleicht sie mit dem Benchmark institutioneller
            Investoren Ihrer Vermögensklasse.
          </p>
          <p class="analyse-hero-disclaimer">
            <strong>MiFID II:</strong> Dies ist keine Anlageberatung. Alle Inhalte dienen
            ausschließlich zu Informationszwecken.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Upload
        st.markdown('<div class="upload-label">Depotauszug hochladen</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Depotauszug hochladen (PNG, JPG)",
            type=["png", "jpg", "jpeg"],
            help="Unterstützte Broker: Trade Republic · Scalable Capital · DKB · Deutsche Bank · Comdirect · ING",
            label_visibility="collapsed",
        )
        st.markdown(
            '<p style="font-size:0.75rem;color:#787878;margin-top:0.5rem">'
            'Ihr Screenshot verlässt nicht Ihren Browser. Analyse läuft über verschlüsselte API-Verbindung.</p>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Demo personas
        st.markdown("""
        <div class="liqid-section-label">Demo-Portfolios</div>
        <div class="liqid-section-title" style="margin-bottom:0.25rem">Oder wählen Sie ein Beispielprofil</div>
        <p class="liqid-section-sub">
          Drei typische DACH-Anleger — unterschiedliche Vermögenstiers, unterschiedliche Gaps.
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
                if st.button("Analysieren →", key=f"demo_{name}", use_container_width=True):
                    st.session_state.portfolio = data
                    st.session_state.source = "demo"
                    st.session_state.analyzed = True
                    st.rerun()

        # Process upload
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

Sophistication: HIGH = Alternatives/Einzelaktien-Mix | MEDIUM = ETFs+Aktien od. ETFs+Anleihen | LOW = nur ETFs od. Cash
Wealth-Tier: UHNW >€2M | HNW €500K–€2M | EMERGING_HNW €100K–€500K
Holdings müssen sich zu 100 addieren. Fehlende Kategorien → 0."""

                    response = get_client().messages.create(
                        model="claude-opus-4-6",
                        max_tokens=1024,
                        messages=[{
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {"type": "base64", "media_type": media_type, "data": img_b64},
                                },
                                {"type": "text", "text": extraction_prompt},
                            ],
                        }],
                    )

                    raw = response.content[0].text.strip()
                    if "```" in raw:
                        parts = raw.split("```")
                        raw = parts[1] if len(parts) > 1 else parts[0]
                        if raw.startswith("json"):
                            raw = raw[4:]

                    data = json.loads(raw.strip())
                    raw_holdings = data.get("holdings", {})
                    total = sum(raw_holdings.values()) if raw_holdings else 0

                    if total < 10:
                        st.error(
                            "Kein Depot erkannt. Das Bild enthält keine lesbaren Portfolio-Daten. "
                            "Bitte laden Sie einen Depotauszug hoch oder wählen Sie ein Demo-Portfolio."
                        )
                        st.stop()

                    if abs(total - 100) > 2:
                        raw_holdings = {k: round(v / total * 100) for k, v in raw_holdings.items()}

                    portfolio = {
                        "holdings": raw_holdings,
                        "estimated_value": data.get("estimated_value") or 300_000,
                        "holding_names": data.get("holding_names", "Erkannte Positionen"),
                        "sophistication": data.get("sophistication", "MEDIUM"),
                        "wealth_tier": data.get("wealth_tier", "EMERGING_HNW"),
                        "risk_inferred": data.get("risk_inferred", "Balanced"),
                        "subtitle": "Hochgeladener Depotauszug",
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

        if st.session_state.gap_df is None:
            tier_b = BENCHMARKS.get(portfolio.get("wealth_tier", "EMERGING_HNW"), BENCHMARKS["EMERGING_HNW"])
            benchmark = tier_b.get(portfolio.get("risk_inferred", "Balanced"), tier_b["Balanced"])
            gap_df = build_gap_df(portfolio["holdings"], benchmark)
            st.session_state.gap_df = gap_df
            st.session_state.cta_path = compute_cta_path(
                portfolio.get("sophistication", "MEDIUM"),
                portfolio.get("wealth_tier", "EMERGING_HNW"),
            )

        gap_df = st.session_state.gap_df

        # Header
        source_label = "Live-Analyse" if st.session_state.source == "upload" else "Demo"
        st.markdown(f"""
        <div class="liqid-section-label">Portfolio-Analyse · {source_label}</div>
        <div class="liqid-section-title">
          {format_value(portfolio["estimated_value"])} &nbsp;·&nbsp;
          {portfolio.get("risk_inferred","—")} &nbsp;·&nbsp;
          Benchmark: {portfolio.get("wealth_tier","—")}-Peers
        </div>
        <p class="liqid-section-sub">{portfolio["holding_names"]}</p>
        """, unsafe_allow_html=True)

        # Gap cards
        cards_html = '<div class="liqid-cards">'
        for _, row in gap_df.iterrows():
            gap = row["Gap (pp)"]
            cur = row["Ihr Portfolio (%)"]
            tgt = row["Peer-Benchmark (%)"]
            if gap > 2:
                bc, bt, gc = "increase", "Untergewichtet", "pos"
            elif gap < -2:
                bc, bt, gc = "reduce", "Übergewichtet", "neg"
            else:
                bc, bt, gc = "ontarget", "Im Zielbereich", "zero"
            cards_html += f"""
            <div class="liqid-card">
              <div class="liqid-card-badge {bc}">{bt}</div>
              <div class="liqid-card-asset">{row['Asset-Klasse']}</div>
              <div class="liqid-card-gap {gc}">{gap:+.0f} pp</div>
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
                .format({"Ihr Portfolio (%)": "{:.0f}%", "Peer-Benchmark (%)": "{:.0f}%", "Gap (pp)": "{:+.0f}pp"})
            )
            st.dataframe(styled, use_container_width=True, hide_index=True)

        # Narrative (streaming)
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
                st.error("API-Key ungültig.")
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

            # Forked CTA (user never sees the routing decision)
            if not st.session_state.lead_captured:
                cta = st.session_state.cta_path

                if cta == "rm":
                    st.markdown("""
                    <div class="liqid-lead-card rm-path">
                      <div class="liqid-rm-badge">Private Markets Zugang</div>
                      <div class="liqid-lead-title">Ihr Portfolio qualifiziert für institutionelle Investmentstrategien</div>
                      <div class="liqid-lead-sub">
                        Basierend auf Ihrer Allokation sehen wir konkrete Optimierungspotenziale —
                        insbesondere im Bereich Private Equity und alternative Anlageklassen.
                        Ein Senior Advisor zeigt Ihnen, was Investoren Ihrer Größenordnung heute anders machen.
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.form("rm_form"):
                        fc1, fc2 = st.columns(2)
                        with fc1:
                            name_in = st.text_input("Ihr Name", placeholder="Dr. Max Mustermann")
                        with fc2:
                            email_in = st.text_input("E-Mail", placeholder="max@example.com")
                        phone_in = st.text_input("Telefon (optional)", placeholder="+49 30 …")
                        if st.form_submit_button("Beratungsgespräch vereinbaren", type="primary", use_container_width=True):
                            if "@" in email_in and "." in email_in:
                                st.session_state.email = email_in
                                st.session_state.lead_captured = True
                                st.rerun()
                            else:
                                st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")
                    st.caption("Ein Senior LIQID Advisor meldet sich innerhalb von 1 Werktag persönlich.")

                else:
                    st.markdown("""
                    <div class="liqid-lead-card">
                      <div class="liqid-lead-title">Vollständigen Portfolio-Report erhalten</div>
                      <div class="liqid-lead-sub">
                        Ihre detaillierte Analyse inklusive Benchmark-Vergleich und
                        Optimierungsszenarien — direkt in Ihr Postfach.
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.form("nurture_form"):
                        email_in = st.text_input("Ihre E-Mail-Adresse", placeholder="name@example.com")
                        if st.form_submit_button("Report anfordern", type="primary", use_container_width=True):
                            if "@" in email_in and "." in email_in:
                                st.session_state.email = email_in
                                st.session_state.lead_captured = True
                                st.rerun()
                            else:
                                st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")
                    st.caption("Automatischer Versand innerhalb von 2 Minuten. Kein Verkaufsgespräch.")

            else:
                if st.session_state.cta_path == "rm":
                    st.success(
                        f"**Beratungstermin angefragt.** Ein Senior LIQID Advisor meldet sich innerhalb "
                        f"von 1 Werktag persönlich unter **{st.session_state.email}**."
                    )
                else:
                    st.success(
                        f"**Report wird zugestellt.** Ihre Analyse wurde an **{st.session_state.email}** gesendet."
                    )
                st.balloons()

        st.markdown("---")
        if st.button("← Neues Portfolio analysieren"):
            for k, v in _defaults.items():
                st.session_state[k] = v
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# INTERNAL SCORING PANEL
# ════════════════════════════════════════════════════════════════════════════
with col_funnel:
    st.markdown('<div class="liqid-funnel-label">Internes Scoring</div>', unsafe_allow_html=True)

    if not st.session_state.analyzed:
        st.markdown("""
        <div class="score-note">
          Dieses Panel zeigt das stille Lead-Scoring,<br>das dem Nutzer nicht angezeigt wird.<br><br>
          Wählen Sie ein Demo-Portfolio oder laden Sie einen Depotauszug hoch.
        </div>
        """, unsafe_allow_html=True)
    else:
        portfolio = st.session_state.portfolio or {}
        wt   = portfolio.get("wealth_tier", "—")
        soph = portfolio.get("sophistication", "—")
        ev   = portfolio.get("estimated_value", 0)
        cta  = st.session_state.cta_path

        wt_color   = {"UHNW": "#460f28", "HNW": "#1a7340", "EMERGING_HNW": "#2c4ab5"}.get(wt, "#232425")
        soph_color = {"HIGH": "#1a7340", "MEDIUM": "#b87c10", "LOW": "#787878"}.get(soph, "#232425")

        st.markdown(f"""
        <div style="margin-bottom:1.25rem">
          <div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.4rem">Vermögenstier</div>
          <div class="score-badge" style="background:{wt_color}">{wt}</div>
        </div>
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
            <div class="score-note">Nutzer sieht nur das passende CTA — kein Routing sichtbar.</div>
            """, unsafe_allow_html=True)

        if st.session_state.narrative:
            st.markdown("---")
            st.markdown('<div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#787878;margin-bottom:0.75rem">Pipeline</div>', unsafe_allow_html=True)
            st.metric("Extraktion", "✓")
            st.metric("Narrative", "✓ Streaming")
            lead_status = "✓ Konvertiert" if st.session_state.lead_captured else "○ Ausstehend"
            st.metric("Lead", lead_status, delta="Lead captured" if st.session_state.lead_captured else None)

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
