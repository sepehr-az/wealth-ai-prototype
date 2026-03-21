"""
AI Investment Outlook Generator — Wealth Management Lead Gen Demo
Case Study Track A: AI-Native Lead Intelligence
"""

import streamlit as st
import anthropic
import pandas as pd
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Investment Outlook Generator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "views": 1,
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

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📈 AI Investment Outlook Generator")
st.caption(
    "⚠️ **MiFID II Disclaimer:** Dies ist keine Anlageberatung. "
    "Alle Inhalte dienen ausschließlich zu Informationszwecken und stellen "
    "keine individuelle Anlageempfehlung dar."
)
st.divider()

# ── Sidebar — Progressive Inputs ─────────────────────────────────────────────
with st.sidebar:
    st.header("🎯 Ihr Investor-Profil")

    assets = st.slider(
        "Investable Assets",
        min_value=100_000,
        max_value=5_000_000,
        value=500_000,
        step=50_000,
        format="€%,d",
    )

    risk = st.selectbox(
        "Risk Appetite",
        ["Conservative", "Balanced", "Aggressive"],
        index=1,
    )

    goals = st.multiselect(
        "Investment Goals",
        ["Growth", "Income", "Capital Preservation", "ESG / Sustainability", "Liquidity"],
        default=["Growth", "Capital Preservation"],
    )

    st.divider()
    st.caption("Powered by Claude AI · For demo purposes only")

# ── Mock baseline allocations per risk profile ───────────────────────────────
MOCK_CURRENT = {
    "Equities":      {"Conservative": 20, "Balanced": 45, "Aggressive": 70},
    "Bonds":         {"Conservative": 55, "Balanced": 35, "Aggressive": 10},
    "Alternatives":  {"Conservative": 10, "Balanced": 10, "Aggressive": 12},
    "Cash":          {"Conservative": 15, "Balanced": 10, "Aggressive":  8},
}

TARGET_RANGES = {
    "Conservative": {"Equities": 25, "Bonds": 50, "Alternatives": 15, "Cash": 10},
    "Balanced":     {"Equities": 55, "Bonds": 28, "Alternatives": 12, "Cash":  5},
    "Aggressive":   {"Equities": 75, "Bonds":  8, "Alternatives": 12, "Cash":  5},
}

def build_gap_df(risk_profile: str) -> pd.DataFrame:
    rows = []
    for asset_class in ["Equities", "Bonds", "Alternatives", "Cash"]:
        current = MOCK_CURRENT[asset_class][risk_profile]
        target  = TARGET_RANGES[risk_profile][asset_class]
        gap     = target - current
        rows.append({
            "Asset Class": asset_class,
            "Current (%)": current,
            "Target (%)":  target,
            "Gap (pp)":    gap,
            "Action":      "Increase ▲" if gap > 0 else ("Reduce ▼" if gap < 0 else "On target ✓"),
        })
    return pd.DataFrame(rows)

def style_gap(val):
    if isinstance(val, (int, float)):
        if val > 0:  return "color: #22c55e; font-weight: bold"
        if val < 0:  return "color: #ef4444; font-weight: bold"
    return ""

# ── Main area ─────────────────────────────────────────────────────────────────
col_main, col_metrics = st.columns([3, 1])

with col_main:
    # ── Generate button ───────────────────────────────────────────────────────
    generate_clicked = st.button(
        "🔍 Generate Portfolio Gap Analysis",
        type="primary",
        use_container_width=True,
        disabled=len(goals) == 0,
    )

    if len(goals) == 0:
        st.info("Please select at least one Investment Goal in the sidebar.")

    if generate_clicked:
        st.session_state.inputs_submitted = True
        st.session_state.report_generated = False
        st.session_state.gap_df = None
        st.session_state.narrative = ""

        # Build gap DataFrame from mock data (hallucination guardrail)
        gap_df = build_gap_df(risk)
        st.session_state.gap_df = gap_df

        goals_str = ", ".join(goals)
        assets_fmt = f"€{assets:,.0f}"

        prompt = f"""You are a senior wealth management advisor generating a concise portfolio gap analysis.

Client profile:
- Investable assets: {assets_fmt}
- Risk appetite: {risk}
- Investment goals: {goals_str}

The following allocation gap data has been calculated (use EXACTLY these numbers — do not invent different figures):

{gap_df.to_string(index=False)}

Tasks:
1. Write a 2-3 sentence executive summary of the current vs. target allocation gap.
2. For each asset class with a non-zero gap, give one specific, actionable recommendation (1 sentence each).
3. Close with one sentence on how these adjustments align with the client's stated goals.

Keep the tone professional but accessible. Do not add disclaimers — those are handled separately."""

        # ── Streaming LLM call ────────────────────────────────────────────────
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
            client_ai = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

            with st.spinner("Analysing your portfolio with Claude AI…"):
                narrative_placeholder = st.empty()
                full_text = ""

                with client_ai.messages.stream(
                    model="claude-opus-4-6",
                    max_tokens=1024,
                    thinking={"type": "adaptive"},
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    for text in stream.text_stream:
                        full_text += text
                        narrative_placeholder.markdown(full_text + "▌")

                narrative_placeholder.markdown(full_text)
                st.session_state.narrative = full_text
                st.session_state.report_generated = True

        except anthropic.AuthenticationError:
            st.error("API key invalid or missing. Set ANTHROPIC_API_KEY in `.streamlit/secrets.toml`.")
        except Exception as e:
            st.error(f"Error calling Claude API: {e}")

    # ── Display report ────────────────────────────────────────────────────────
    if st.session_state.report_generated and st.session_state.gap_df is not None:
        st.subheader("📊 Portfolio Gap Analysis")

        styled = (
            st.session_state.gap_df
            .style
            .applymap(style_gap, subset=["Gap (pp)"])
            .format({"Current (%)": "{:.0f}%", "Target (%)": "{:.0f}%", "Gap (pp)": "{:+.0f}pp"})
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

        st.subheader("💡 AI-Powered Insights")
        if st.session_state.narrative:
            st.chat_message("assistant").markdown(st.session_state.narrative)

        st.divider()

        # ── Lead capture ──────────────────────────────────────────────────────
        if not st.session_state.qualified_lead:
            st.subheader("📬 Vollständigen personalisierten Report per Email?")
            with st.form("lead_form"):
                email_input = st.text_input(
                    "Ihre Email-Adresse",
                    placeholder="name@example.com",
                )
                submit_lead = st.form_submit_button(
                    "📩 Report zusenden",
                    type="primary",
                    use_container_width=True,
                )
                if submit_lead:
                    if "@" in email_input and "." in email_input:
                        st.session_state.email = email_input
                        st.session_state.qualified_lead = True
                        st.rerun()
                    else:
                        st.warning("Bitte geben Sie eine gültige Email-Adresse ein.")
        else:
            st.success(
                f"✅ **Lead qualifiziert!** Report wird an **{st.session_state.email}** gesendet. "
                "Ein Berater meldet sich innerhalb von 24 Stunden."
            )
            st.balloons()

# ── Metrics column ────────────────────────────────────────────────────────────
with col_metrics:
    st.subheader("📈 Funnel")
    st.metric("👁 Views", st.session_state.views)
    st.metric(
        "📝 Inputs",
        1 if st.session_state.inputs_submitted else 0,
        delta="Active" if st.session_state.inputs_submitted else None,
    )
    st.metric(
        "📊 Reports",
        1 if st.session_state.report_generated else 0,
        delta="Generated" if st.session_state.report_generated else None,
    )
    st.metric(
        "🎯 Leads",
        1 if st.session_state.qualified_lead else 0,
        delta="Qualified ✓" if st.session_state.qualified_lead else None,
    )

    if st.session_state.report_generated:
        gap_df = st.session_state.gap_df
        max_gap_row = gap_df.loc[gap_df["Gap (pp)"].abs().idxmax()]
        st.divider()
        st.caption("**Top Gap**")
        st.metric(
            max_gap_row["Asset Class"],
            f"{max_gap_row['Gap (pp)']:+.0f}pp",
        )
