"""
DataCleaner AI — Before vs After Comparison Page
Cinematic animated comparison of cleaning improvements.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.data_profiler import profile_dataset

PLOTLY_THEME = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#94a3b8",
}


def render_before_after():
    """Render the Before vs After comparison page."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">📈 COMPARISON</div>
<h1 class="page-title">Before vs After <span class="gradient-text">Analysis</span></h1>
<p class="page-subtitle">
See exactly how much your dataset improved after AI cleaning.
</p>
</div>""", unsafe_allow_html=True)

    if "df_original" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df_orig = st.session_state["df_original"]
    df_clean = st.session_state.get("df_cleaned", df_orig)

    # Compute profiles
    p_before = st.session_state.get("profile_before", profile_dataset(df_orig))
    p_after  = profile_dataset(df_clean)

    # ── HERO IMPROVEMENT BANNER ────────────────────────────────────────
    score_improvement = p_after["quality_score"] - p_before["quality_score"]
    rows_removed = p_before["rows"] - p_after["rows"]
    nulls_fixed  = p_before["total_nulls"] - p_after["total_nulls"]
    dups_removed = p_before["duplicate_rows"] - p_after["duplicate_rows"]

    if score_improvement > 0:
        banner_color = "#10b981"
        banner_text = f"✨ Dataset quality improved by {score_improvement} points!"
    elif score_improvement == 0:
        banner_color = "#06b6d4"
        banner_text = "ℹ️ No cleaning applied yet. Run the AI Cleaning Engine first."
    else:
        banner_color = "#f59e0b"
        banner_text = "⚠️ Quality score unchanged. Consider more aggressive cleaning."

    st.markdown(f"""<div style="background:rgba(255,255,255,0.02); border:1px solid {banner_color}40;
border-radius:20px; padding:1.5rem 2rem; text-align:center;
box-shadow:0 0 30px {banner_color}20; margin-bottom:1.5rem; animation:fadeInUp 0.6s ease;">
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.4rem;
font-weight:700; color:{banner_color};">{banner_text}</div>
</div>""", unsafe_allow_html=True)

    # ── ANIMATED COMPARISON METRICS ────────────────────────────────────
    st.markdown("### 📊 Key Metrics Comparison")

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    metrics = [
        ("Quality Score", p_before["quality_score"], p_after["quality_score"], "/100", "#8b5cf6"),
        ("Rows",          p_before["rows"],          p_after["rows"],          "",     "#06b6d4"),
        ("Columns",       p_before["columns"],        p_after["columns"],       "",     "#3b82f6"),
        ("Missing Values",p_before["total_nulls"],    p_after["total_nulls"],   "",     "#ec4899"),
        ("Duplicates",    p_before["duplicate_rows"], p_after["duplicate_rows"],"",     "#f59e0b"),
        ("Memory (MB)",   round(p_before["memory_usage_mb"],2),
                          round(p_after["memory_usage_mb"],2), " MB", "#10b981"),
    ]

    for col, (label, before, after, unit, color) in zip([m1, m2, m3, m4, m5, m6], metrics):
        delta = after - before if isinstance(after, (int, float)) else 0
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        delta_color = "#10b981" if (label in ["Quality Score"] and delta >= 0) else \
                      ("#10b981" if delta <= 0 and label != "Quality Score" else "#ef4444")

        with col:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
border-top:3px solid {color}; border-radius:16px; padding:1rem;
text-align:center; animation:fadeInUp 0.5s ease; transition:all 0.3s ease;"
onmouseover="this.style.transform='translateY(-4px)'"
onmouseout="this.style.transform='translateY(0)'">
<div style="font-size:0.68rem; color:#64748b; text-transform:uppercase;
letter-spacing:0.1em; margin-bottom:8px;">{label}</div>
<div style="display:flex; justify-content:space-around; align-items:center; gap:6px;">
<div>
<div style="font-size:0.6rem; color:#64748b; margin-bottom:2px;">BEFORE</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1rem;
font-weight:700; color:#94a3b8;">{before}{unit}</div>
</div>
<div style="color:#475569; font-size:1rem;">→</div>
<div>
<div style="font-size:0.6rem; color:{color}; margin-bottom:2px;">AFTER</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1rem;
font-weight:700; color:{color};">{after}{unit}</div>
</div>
</div>
<div style="font-size:0.72rem; color:{delta_color}; margin-top:6px;
font-weight:600;">{delta_str}{unit}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── COMPARISON BAR CHART ───────────────────────────────────────────
    st.markdown("### 📊 Visual Comparison")

    chart_data = {
        "Metric":  ["Quality Score", "Missing Values", "Duplicate Rows", "Rows Removed"],
        "Before":  [p_before["quality_score"], p_before["total_nulls"],
                    p_before["duplicate_rows"], 0],
        "After":   [p_after["quality_score"],  p_after["total_nulls"],
                    p_after["duplicate_rows"],  rows_removed],
    }

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Before",
        x=chart_data["Metric"],
        y=chart_data["Before"],
        marker_color="rgba(100,116,139,0.6)",
        marker_line=dict(color="#475569", width=1),
    ))
    fig.add_trace(go.Bar(
        name="After",
        x=chart_data["Metric"],
        y=chart_data["After"],
        marker_color="rgba(139,92,246,0.75)",
        marker_line=dict(color="#8b5cf6", width=1),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        barmode="group",
        height=380,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text="Before vs After — Key Metrics", x=0.5, font=dict(color="#f1f5f9")),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        bargap=0.25,
        bargroupgap=0.1,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── QUALITY SCORE GAUGE ────────────────────────────────────────────
    g1, g2 = st.columns(2)
    with g1:
        _render_gauge(p_before["quality_score"], "Quality Score — BEFORE", "#64748b")
    with g2:
        _render_gauge(p_after["quality_score"], "Quality Score — AFTER", "#8b5cf6")

    st.markdown("---")

    # ── COLUMN-LEVEL NULL COMPARISON ───────────────────────────────────
    st.markdown("### 🕳️ Column-Level Missing Value Comparison")
    orig_nulls = df_orig.isnull().sum()
    clean_nulls = df_clean.isnull().sum()

    common_cols = [c for c in df_orig.columns if c in df_clean.columns]
    if common_cols:
        null_df = pd.DataFrame({
            "Column": common_cols,
            "Before": [int(orig_nulls.get(c, 0)) for c in common_cols],
            "After":  [int(clean_nulls.get(c, 0)) for c in common_cols],
        })
        null_df = null_df[null_df["Before"] > 0].sort_values("Before", ascending=False)

        if not null_df.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                name="Before", x=null_df["Column"], y=null_df["Before"],
                marker_color="rgba(239,68,68,0.6)", marker_line=dict(color="#ef4444", width=1),
            ))
            fig2.add_trace(go.Bar(
                name="After", x=null_df["Column"], y=null_df["After"],
                marker_color="rgba(16,185,129,0.7)", marker_line=dict(color="#10b981", width=1),
            ))
            fig2.update_layout(
                **PLOTLY_THEME, barmode="group", height=320,
                margin=dict(l=20, r=20, t=30, b=20),
                title=dict(text="Missing Values per Column", x=0.5, font=dict(color="#f1f5f9")),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.success("🎉 All missing values have been resolved!")

    # ── CLEANING LOG ───────────────────────────────────────────────────
    cleaning_log = st.session_state.get("cleaning_log", [])
    if cleaning_log:
        st.markdown("---")
        st.markdown(f"### 📋 Applied Operations ({len(cleaning_log)})")
        for i, entry in enumerate(cleaning_log, 1):
            st.markdown(f"""<div style="display:flex; align-items:center; gap:12px; padding:10px 16px;
background:rgba(16,185,129,0.05); border:1px solid rgba(16,185,129,0.15);
border-radius:10px; margin-bottom:6px; animation:fadeInLeft 0.4s ease {i*0.05}s both;">
<div style="width:28px; height:28px; background:rgba(16,185,129,0.2);
border-radius:50%; display:flex; align-items:center; justify-content:center;
font-size:0.78rem; font-weight:700; color:#34d399; flex-shrink:0;">
{i:02d}
</div>
<span style="color:#94a3b8; font-size:0.85rem;">✓ {entry}</span>
</div>""", unsafe_allow_html=True)


def _render_gauge(value: int, title: str, color: str):
    """Render a gauge chart for quality score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#94a3b8", "size": 13}},
        number={"font": {"color": color, "size": 40, "family": "Space Grotesk"}, "suffix": "/100"},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#475569", "tickfont": {"color": "#475569"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(255,255,255,0.06)",
            "steps": [
                {"range": [0, 40],  "color": "rgba(239,68,68,0.1)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.1)"},
                {"range": [70, 100],"color": "rgba(16,185,129,0.1)"},
            ],
            "threshold": {
                "line": {"color": "#f1f5f9", "width": 2},
                "thickness": 0.75,
                "value": value,
            },
        },
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
