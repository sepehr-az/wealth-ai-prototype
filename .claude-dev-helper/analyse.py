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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

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

/* ─── Preference selector section ────────────────────────────────────────── */
.pref-section {
  margin: 2rem 0 1.5rem; padding: 2rem 2rem 1.5rem;
  background: #f9f8f6; border-radius: 8px;
  border: 1px solid #eeebe6;
}
.pref-section-eyebrow {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
  text-transform: uppercase; color: #787878; margin-bottom: 0.6rem;
}
.pref-section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.3rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.5rem;
}
.pref-section-sub {
  font-size: 0.875rem; color: #555; line-height: 1.6; margin-bottom: 0;
}

/* ─── Card-style radio questions (LIQID style) ────────────────────────────── */
.pref-q-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.45rem; font-weight: 700; color: #1a1a1a;
  margin-bottom: 0.35rem; line-height: 1.25;
}
.pref-q-sub { font-size: 0.8rem; color: #999; margin-bottom: 0.9rem; }

div[data-testid="stRadio"] > div { gap: 0.4rem !important; }
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] label {
  display: flex !important; align-items: center !important;
  justify-content: space-between !important;
  padding: 0.95rem 1.1rem !important;
  border: 1px solid #e0ddd8 !important; border-radius: 10px !important;
  background: #fff !important; cursor: pointer !important;
  width: 100% !important; margin: 0 !important;
  transition: border-color 0.15s, background 0.15s !important;
}
div[data-testid="stRadio"] label:hover {
  border-color: #460f28 !important; background: #fdf8f7 !important;
}
div[data-testid="stRadio"] label > div:first-child { display: none !important; }
div[data-testid="stRadio"] label > div:last-child p {
  font-size: 0.95rem !important; color: #1a1a1a !important; margin: 0 !important;
}
div[data-testid="stRadio"] label::after {
  content: "›" !important; font-size: 1.4rem !important;
  color: #ccc !important; line-height: 1 !important; flex-shrink: 0;
}
div[data-testid="stRadio"] label:has(input:checked) {
  border-color: #460f28 !important; background: #fdf8f7 !important;
}
div[data-testid="stRadio"] label:has(input:checked)::after { color: #460f28 !important; }
div[data-testid="stRadio"] label:has(input:checked) > div:last-child p {
  font-weight: 600 !important; color: #460f28 !important;
}


/* ─── Blurred proposal ────────────────────────────────────────────────────── */
.proposal-blurred {
  filter: blur(6px);
  user-select: none;
  pointer-events: none;
  transition: filter 0.6s ease;
  border-radius: 6px;
  overflow: hidden;
}
.proposal-visible {
  filter: none;
  border-radius: 6px;
  overflow: hidden;
}
.proposal-content {
  background: #fff; border: 1px solid #e8e4de; border-radius: 6px;
  padding: 2rem 2.5rem;
}
.proposal-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.2rem; font-weight: 700; color: #1a1a1a; margin-bottom: 1.25rem;
  padding-bottom: 0.75rem; border-bottom: 2px solid #460f28;
}
.proposal-alloc-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin: 1.25rem 0;
}
.proposal-alloc-cell {
  background: #f5f3f0; border-radius: 6px; padding: 1rem 0.75rem; text-align: center;
}
.proposal-alloc-pct {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.5rem; font-weight: 700; color: #460f28; margin-bottom: 0.2rem;
}
.proposal-alloc-label { font-size: 0.7rem; color: #666; text-transform: uppercase; letter-spacing: 0.08em; }

/* ─── Unlock card ─────────────────────────────────────────────────────────── */
.unlock-card {
  background: #1a1a1a; color: #fff; padding: 2.5rem 2rem;
  border-radius: 8px; margin-top: 1.5rem; text-align: center;
}
.unlock-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.unlock-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem; font-weight: 700; color: #fff;
  margin-bottom: 0.5rem; line-height: 1.3;
}
.unlock-sub {
  font-size: 0.875rem; color: rgba(255,255,255,0.65); line-height: 1.6; margin-bottom: 0;
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
    # New: preference + proposal flow
    "investment_prefs": None,
    "prefs_submitted": False,
    "proposal": "",
    "proposal_unlocked": False,
    "show_table": False,
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
            <strong>Hinweis:</strong> Diese Anwendung dient ausschließlich zu Informations-
            und Bildungszwecken. Die Inhalte stellen keine Anlageberatung, keine persönliche
            Empfehlung und kein Angebot zum Kauf oder Verkauf von Finanzinstrumenten dar
            (MiFID II Art. 4(1)(4)). Hochgeladene Daten werden nicht gespeichert und
            ausschließlich zur einmaligen Analyse verwendet (DSGVO Art. 6).
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
  "risk_inferred": "<Conservative|Balanced|Ambitioniert>"
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
                    st.error("API-Key ungültig.")
                except anthropic.APIStatusError as e:
                    st.warning(f"API vorübergehend nicht erreichbar ({e.status_code}). Bitte erneut versuchen.")
                except anthropic.APIConnectionError:
                    st.warning("Keine Verbindung zur API. Bitte Internetverbindung prüfen und erneut versuchen.")
                except json.JSONDecodeError:
                    st.error(
                        "Das Portfolio konnte nicht automatisch eingelesen werden. "
                        "Bitte versuchen Sie einen klareren Screenshot oder wählen Sie ein Demo-Portfolio."
                    )
                except Exception as e:
                    st.warning(f"Vorübergehender Fehler. Bitte erneut versuchen. ({type(e).__name__})")

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
                portfolio.get("estimated_value", 0),
            )

        gap_df = st.session_state.gap_df

        # Header
        source_label = "Live-Analyse" if st.session_state.source == "upload" else "Demo"
        st.markdown(f"""
        <div class="liqid-section-label">Portfolio-Analyse · {source_label}</div>
        <div class="liqid-section-title">
          {format_value(portfolio["estimated_value"])} &nbsp;·&nbsp; Peer-Vergleich
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

        toggle_label = "Detailtabelle ausblenden ↑" if st.session_state.show_table else "Detailtabelle anzeigen ↓"
        if st.button(toggle_label, key="toggle_table"):
            st.session_state.show_table = not st.session_state.show_table
            st.rerun()
        if st.session_state.show_table:
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
            except (anthropic.APIStatusError, anthropic.APIConnectionError):
                st.warning("API vorübergehend nicht erreichbar. Bitte kurz warten und **Analyse starten** erneut drücken.")
            except Exception as e:
                st.warning(f"Vorübergehender Fehler ({type(e).__name__}). Bitte erneut versuchen.")

        if st.session_state.narrative:
            st.markdown(f"""
            <div class="liqid-quote">
              <div class="liqid-quote-text">„{st.session_state.narrative}"</div>
              <div class="liqid-quote-source">Claude AI · LIQID Portfolio Intelligence</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # ── PHASE 3: Investment Preferences → Blurred Proposal ─────────────
            if not st.session_state.prefs_submitted:
                st.markdown("""
                <div class="pref-section">
                  <div class="pref-section-eyebrow">Schritt 2 von 3</div>
                  <div class="pref-section-title">Illustrative Musterallokation</div>
                  <p class="pref-section-sub">
                    Wählen Sie Ihre Präferenzen — wir zeigen Ihnen, wie eine
                    beispielhafte Allokation für dieses Profil aussehen könnte.
                    Dies ist keine Anlageberatung.
                  </p>
                </div>
                """, unsafe_allow_html=True)

                anlageziel = st.pills(
                    "Was möchten Sie erreichen?",
                    options=["Vermögen ausbauen", "Vor Inflation schützen", "Kurzfristig anlegen"],
                    selection_mode="single",
                    key="pref_anlageziel",
                )
                zeithorizont = st.pills(
                    "Wie lange möchten Sie anlegen?",
                    options=["Mehr als 10 Jahre", "5–10 Jahre", "3–5 Jahre", "Unter 3 Jahre"],
                    selection_mode="single",
                    key="pref_zeithorizont",
                )

                all_selected = all([anlageziel, zeithorizont])

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(
                    "Meine Strategie generieren →",
                    type="primary",
                    disabled=not all_selected,
                    use_container_width=True,
                ):
                    st.session_state.investment_prefs = {
                        "anlageziel": anlageziel,
                        "zeithorizont": zeithorizont,
                    }
                    st.session_state.prefs_submitted = True
                    st.rerun()

                if not all_selected:
                    st.caption("Bitte alle drei Fragen beantworten, um Ihre Strategie zu generieren.")

            else:
                # ── Generate proposal if not yet done ─────────────────────────
                if not st.session_state.proposal:
                    prefs = st.session_state.investment_prefs or {}
                    holdings = portfolio.get("holdings", {})
                    wt = portfolio.get("wealth_tier", "EMERGING_HNW")
                    risk = portfolio.get("risk_inferred", "Balanced")
                    val = format_value(portfolio.get("estimated_value", 0))

                    proposal_prompt = f"""Du erstellst eine rein informatorische, illustrative Musterallokation zu Bildungszwecken — keine Anlageberatung, keine persönliche Empfehlung im Sinne von MiFID II.

EINGABEDATEN (nur zur Kontextualisierung der Illustration):
- Portfoliogröße: {val}
- Aktuelle Allokation: {json.dumps(holdings, ensure_ascii=False)}
- Anlageziel: {prefs.get("anlageziel", "—")}
- Zeithorizont: {prefs.get("zeithorizont", "—")}

Erstelle eine illustrative Beispielallokation auf Deutsch mit diesen 3 Abschnitten:

**Illustrative Musterallokation: [sachlicher Strategiename ohne Versprechen]**

**Beispielhafte Zielgewichtung:**
Konkrete Prozentzahlen für Aktien, Anleihen, Alternatives, Liquidität (zusammen 100%). Formuliere als "Ein Anleger mit diesem Profil könnte beispielsweise..." — nicht als persönliche Empfehlung.

**Hintergrund zur Allokationslogik:**
2 Sätze: Erkläre neutral, welche Überlegungen hinter dieser Gewichtung stehen. Verweis auf Assetklassen wie Private Equity oder Private Credit als Diversifikationsbaustein, den institutionelle Anleger historisch nutzen — ohne Renditeversprechen oder Zukunftsaussagen.

**Hinweis:**
Schreibe einen kurzen Standard-Disclaimer: Diese Darstellung dient ausschließlich zu Informationszwecken und stellt keine Anlageberatung, keine persönliche Empfehlung und kein Angebot zum Kauf oder Verkauf von Finanzinstrumenten dar. Vergangene Entwicklungen sind kein verlässlicher Indikator für zukünftige Ergebnisse.

Strikte Regeln:
- Keine Formulierungen: "Sie sollten", "wir empfehlen", "für Sie geeignet", "Ihr Portfolio"
- Keine konkreten Renditeprognosen oder Prozentsätze für erwartete Erträge
- Kein Vergleich mit LIQID-Performance oder anderen Kundendaten
- Neutral, sachlich, illustrativ — keine Verkaufssprache
- Kein Markdown außer den drei Abschnittsüberschriften mit **"""

                    try:
                        proposal_ph = st.empty()
                        full_proposal = ""
                        with get_client().messages.stream(
                            model="claude-sonnet-4-6",
                            max_tokens=800,
                            messages=[{"role": "user", "content": proposal_prompt}],
                        ) as stream:
                            for text in stream.text_stream:
                                full_proposal += text
                                proposal_ph.markdown(
                                    f'<div class="stream-preview">{full_proposal}▌</div>',
                                    unsafe_allow_html=True,
                                )
                        proposal_ph.empty()
                        st.session_state.proposal = full_proposal
                        st.rerun()
                    except anthropic.AuthenticationError:
                        st.error("API-Key ungültig.")
                    except (anthropic.APIStatusError, anthropic.APIConnectionError):
                        st.warning("API vorübergehend nicht erreichbar. Bitte erneut versuchen.")
                    except Exception as e:
                        st.warning(f"Vorübergehender Fehler ({type(e).__name__}). Bitte erneut versuchen.")

                # ── Show proposal (blurred or revealed) ───────────────────────
                if st.session_state.proposal:
                    blur_class = "proposal-visible" if st.session_state.proposal_unlocked else "proposal-blurred"

                    st.markdown(f"""
                    <div class="{blur_class}">
                      <div class="proposal-content">
                        <div class="proposal-heading">Illustrative Musterallokation — nicht personalisierte Anlageberatung</div>
                        {st.session_state.proposal.replace(chr(10), "<br>")}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if not st.session_state.proposal_unlocked:
                        # Unlock card
                        st.markdown("""
                        <div class="unlock-card">
                          <div class="unlock-icon">🔒</div>
                          <div class="unlock-title">Ihre Musterallokation ist bereit</div>
                          <p class="unlock-sub">
                            Hinterlassen Sie Ihre Kontaktdaten, um die vollständige
                            illustrative Allokation zu sehen — und optional ein
                            unverbindliches Erstgespräch zu vereinbaren.
                          </p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.form("unlock_form"):
                            uc1, uc2 = st.columns(2)
                            with uc1:
                                unlock_name = st.text_input("Ihr Name *", placeholder="Max Mustermann")
                            with uc2:
                                unlock_email = st.text_input("E-Mail-Adresse *", placeholder="name@example.com")
                            unlock_phone = st.text_input("Telefon (optional)", placeholder="+49 30 …")
                            submitted = st.form_submit_button(
                                "Vorschlag freischalten →",
                                type="primary",
                                use_container_width=True,
                            )
                            if submitted:
                                if "@" in unlock_email and "." in unlock_email:
                                    st.session_state.email = unlock_email
                                    st.session_state.lead_captured = True
                                    st.session_state.proposal_unlocked = True
                                    st.rerun()
                                else:
                                    st.warning("Bitte geben Sie eine gültige E-Mail-Adresse ein.")

                        st.caption("Kein Spam, kein Verkaufsdruck. Ihr Vorschlag wird sofort freigeschaltet.")

                    else:
                        cta = st.session_state.cta_path
                        if cta == "rm":
                            st.success(
                                f"**Vorschlag freigeschaltet.** Ein Senior LIQID Advisor meldet sich "
                                f"innerhalb von 1 Werktag unter **{st.session_state.email}**."
                            )
                        else:
                            st.success(
                                f"**Vorschlag freigeschaltet.** Ihre vollständige Analyse wurde an "
                                f"**{st.session_state.email}** gesendet."
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
            st.metric("Präferenzen", "✓" if st.session_state.prefs_submitted else "○ Ausstehend")
            st.metric("Vorschlag", "✓ Generiert" if st.session_state.proposal else "○ Ausstehend")
            lead_status = "✓ Konvertiert" if st.session_state.lead_captured else "○ Ausstehend"
            st.metric("Lead", lead_status, delta="Lead captured" if st.session_state.lead_captured else None)

            if st.session_state.investment_prefs:
                st.markdown("---")
                prefs = st.session_state.investment_prefs
                st.caption("**Anlageinteressen**")
                st.caption(f"🎯 {prefs.get('anlageziel','—')}")
                st.caption(f"⏱ {prefs.get('zeithorizont','—')}")

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
