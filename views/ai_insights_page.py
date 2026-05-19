"""
DataCleaner AI — AI Insights Engine Page
Dataset quality scoring, feature importance, and smart recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_profiler import (
    profile_dataset, get_feature_importance_proxy,
    get_ml_problem_type
)

PLOTLY_THEME = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#94a3b8",
}

NEON_COLORS = ["#8b5cf6", "#06b6d4", "#ec4899", "#10b981", "#f59e0b", "#3b82f6"]


def render_ai_insights():
    """Render the AI insights dashboard."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">🤖 AI INSIGHTS</div>
<h1 class="page-title">AI <span class="gradient-text">Insights Engine</span></h1>
<p class="page-subtitle">
Smart automated analysis — dataset quality scoring, feature importance, and ML recommendations.
</p>
</div>""".replace('\n', ' '), unsafe_allow_html=True)

    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df_cleaned"]
    profile = profile_dataset(df)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # ── QUALITY SCORE ──────────────────────────────────────────────────
    score = profile["quality_score"]
    _render_quality_hero(score)

    st.markdown("---")

    # ── TOP ROW: ML TYPE + KEY STATS ──────────────────────────────────
    col1, col2 = st.columns([1, 2])
    with col1:
        _render_ml_type_card(df)

    with col2:
        _render_smart_warnings(profile)

    st.markdown("---")

    # ── FEATURE IMPORTANCE ─────────────────────────────────────────────
    st.markdown("### 📊 Feature Importance (Proxy Score)")
    _render_feature_importance(df)

    st.markdown("---")

    # ── CORRELATION INSIGHTS ────────────────────────────────────────────
    if len(numeric_cols) >= 2:
        st.markdown("### 🔗 Correlation Insights")
        _render_correlation_insights(df, numeric_cols)

    st.markdown("---")

    # ── AI SUMMARY ──────────────────────────────────────────────────────
    st.markdown("### 🧠 AI-Generated Dataset Summary")
    _render_ai_summary(df, profile)

    st.markdown("---")

    # ── PREPROCESSING PIPELINE ──────────────────────────────────────────
    st.markdown("### ⚙️ Recommended Preprocessing Pipeline")
    _render_preprocessing_pipeline(profile)


def _render_quality_hero(score: int):
    """Render a big quality score hero section."""
    if score >= 80:
        color, label, desc = "#10b981", "Excellent", "Your dataset is in great shape for ML!"
        glow = "rgba(16,185,129,0.3)"
    elif score >= 60:
        color, label, desc = "#f59e0b", "Good", "Minor issues detected. Quick cleanup recommended."
        glow = "rgba(245,158,11,0.3)"
    elif score >= 40:
        color, label, desc = "#f97316", "Fair", "Several data quality issues need attention."
        glow = "rgba(249,115,22,0.3)"
    else:
        color, label, desc = "#ef4444", "Poor", "Critical data issues detected. Full cleaning required."
        glow = "rgba(239,68,68,0.3)"

    circumference = 2 * 3.14159 * 70
    offset = circumference * (1 - score / 100)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"""<div style="text-align:center; padding:2rem 1rem; background:rgba(255,255,255,0.02);
border:1px solid {glow}; border-radius:24px;
box-shadow: 0 0 40px {glow}; animation:fadeInUp 0.6s ease;">
<svg width="180" height="180" viewBox="0 0 180 180">
<circle cx="90" cy="90" r="70" fill="none"
stroke="rgba(255,255,255,0.06)" stroke-width="14"/>
<circle cx="90" cy="90" r="70" fill="none"
stroke="{color}" stroke-width="14"
stroke-dasharray="{circumference:.1f}"
stroke-dashoffset="{offset:.1f}"
stroke-linecap="round"
transform="rotate(-90 90 90)"
style="filter:drop-shadow(0 0 12px {color});"/>
<text x="90" y="82" text-anchor="middle"
font-family="Space Grotesk" font-size="38" font-weight="900"
fill="{color}">{score}</text>
<text x="90" y="105" text-anchor="middle"
font-family="Inter" font-size="13" fill="#64748b">out of 100</text>
</svg>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem;
font-weight:800; color:{color}; margin-top:0.5rem;">{label}</div>
<div style="color:#94a3b8; font-size:0.9rem; margin-top:0.4rem;">{desc}</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def _render_ml_type_card(df: pd.DataFrame):
    """Guess and display ML problem type."""
    col_types = df.dtypes
    target_guess = None
    # Try to guess target column
    for col in ["target", "label", "survived", "churn", "price", "saleprice", "outcome"]:
        if col.lower() in [c.lower() for c in df.columns]:
            target_guess = col
            break

    ml_type = get_ml_problem_type(df, target_guess)
    icons = {
        "Classification": "🎯",
        "Binary Classification": "⚖️",
        "Multi-class Classification": "🎲",
        "Regression": "📈",
        "Clustering / Unsupervised": "🌐",
    }
    icon = icons.get(ml_type, "🤖")

    st.markdown(f"""<div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.25);
border-radius:20px; padding:1.5rem; height:100%; animation:fadeInLeft 0.6s ease;">
<div style="font-size:0.72rem; color:#64748b; text-transform:uppercase;
letter-spacing:0.1em; margin-bottom:12px;">🤖 Predicted ML Problem Type</div>
<div style="font-size:3rem; margin-bottom:8px;">{icon}</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem;
font-weight:700; color:#a78bfa; margin-bottom:8px;">{ml_type}</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.5;">
Based on dataset structure, column types, and cardinality analysis.
{f"<br>Target column guess: <code style='color:#a78bfa;'>{target_guess}</code>" if target_guess else ""}
</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def _render_smart_warnings(profile: dict):
    """Render AI-generated smart warnings."""
    issues = profile.get("issues", [])
    high_issues = [i for i in issues if i.get("severity") == "high"]
    med_issues  = [i for i in issues if i.get("severity") == "medium"]

    warnings = []
    if profile.get("null_rate", 0) > 20:
        warnings.append(("🔴", "High", f"Missing rate is {profile['null_rate']:.1f}% — consider imputation or column removal."))
    if profile.get("duplicate_rows", 0) > 0:
        warnings.append(("🟡", "Medium", f"{profile['duplicate_rows']} duplicate rows may bias your model."))
    if profile.get("constant_columns"):
        warnings.append(("🟡", "Medium", f"{len(profile['constant_columns'])} constant columns have zero predictive value."))
    if profile.get("rows", 0) < 100:
        warnings.append(("🔴", "High", "Very small dataset (<100 rows) — model may overfit significantly."))
    if profile.get("columns", 0) > profile.get("rows", 1) / 10:
        warnings.append(("🟡", "Medium", "High feature-to-sample ratio — consider dimensionality reduction (PCA)."))
    if not warnings:
        warnings.append(("🟢", "Good", "No critical warnings detected. Dataset looks clean and ready!"))

    warnings_html = ""
    for emoji, level, msg in warnings:
        color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Good": "#10b981"}
        color = color_map.get(level, "#94a3b8")
        warnings_html += f"""<div style="display:flex; gap:10px; align-items:flex-start; padding:10px 12px;
background:rgba(255,255,255,0.02); border-radius:10px; margin-bottom:6px;
border-left:3px solid {color};">
<span>{emoji}</span>
<div>
<span style="font-size:0.72rem; color:{color}; font-weight:700;
text-transform:uppercase;">{level}</span>
<div style="font-size:0.83rem; color:#94a3b8; margin-top:2px;">{msg}</div>
</div>
</div>"""

    st.markdown(f"""<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08);
border-radius:20px; padding:1.5rem; animation:slideInRight 0.6s ease;">
<div style="font-size:0.72rem; color:#64748b; text-transform:uppercase;
letter-spacing:0.1em; margin-bottom:12px;">⚡ Smart AI Warnings</div>
{warnings_html}
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def _render_feature_importance(df: pd.DataFrame):
    """Bar chart of feature importance proxy scores."""
    importance = get_feature_importance_proxy(df)
    if not importance:
        st.info("Not enough columns to compute feature importance.")
        return

    cols, scores = zip(*importance[:20])  # Top 20
    fig = go.Figure(go.Bar(
        x=list(scores),
        y=list(cols),
        orientation="h",
        marker=dict(
            color=list(scores),
            colorscale=[[0, "#1e0533"], [0.5, "#8b5cf6"], [1, "#06b6d4"]],
            line=dict(width=0),
        ),
        text=[f"{s:.3f}" for s in scores],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=11),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=max(300, 35 * min(len(cols), 20) + 80),
        margin=dict(l=20, r=80, t=20, b=20),
        xaxis_title="Importance Score (proxy)",
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("⚠️ Importance scores are heuristic proxies (coefficient of variation / cardinality ratio), not true ML feature importances.")


def _render_correlation_insights(df: pd.DataFrame, numeric_cols: list):
    """Highlight highly correlated feature pairs."""
    corr = df[numeric_cols].corr()
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            val = corr.iloc[i, j]
            if abs(val) > 0.5:
                pairs.append((corr.columns[i], corr.columns[j], round(val, 3)))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    if not pairs:
        st.success("✅ No strongly correlated feature pairs detected.")
        return

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**{len(pairs)} correlated pairs found** (|r| > 0.5)")
        for c1_name, c2_name, val in pairs[:8]:
            abs_val = abs(val)
            color = "#ef4444" if abs_val > 0.9 else ("#f59e0b" if abs_val > 0.7 else "#06b6d4")
            bar_pct = int(abs_val * 100)
            st.markdown(f"""<div style="margin-bottom:10px;">
<div style="display:flex; justify-content:space-between; margin-bottom:3px;">
<span style="font-size:0.83rem; color:#f1f5f9;">{c1_name} ↔ {c2_name}</span>
<span style="font-size:0.83rem; color:{color}; font-weight:700;">{val:+.3f}</span>
</div>
<div style="background:rgba(255,255,255,0.05); border-radius:999px; height:5px;">
<div style="width:{bar_pct}%; height:100%; background:{color};
border-radius:999px; box-shadow:0 0 6px {color}60;"></div>
</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)

    with col2:
        # Mini heatmap of top correlated columns
        top_cols = list(set([p[0] for p in pairs[:6]] + [p[1] for p in pairs[:6]]))[:8]
        mini_corr = df[top_cols].corr()
        fig = go.Figure(go.Heatmap(
            z=mini_corr.values,
            x=mini_corr.columns,
            y=mini_corr.columns,
            colorscale=[[0,"#1e0533"],[0.5,"#0f172a"],[1,"#06b6d4"]],
            text=mini_corr.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 9},
            zmin=-1, zmax=1,
        ))
        fig.update_layout(**PLOTLY_THEME, height=300,
                          margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)


def _render_ai_summary(df: pd.DataFrame, profile: dict):
    """Generate and display AI-style natural language summary."""
    rows = profile.get("rows", 0)
    cols = profile.get("columns", 0)
    nulls = profile.get("total_nulls", 0)
    null_rate = profile.get("null_rate", 0)
    dups = profile.get("duplicate_rows", 0)
    score = profile.get("quality_score", 0)
    numeric_count = len(df.select_dtypes(include=[np.number]).columns)
    cat_count = len(df.select_dtypes(include="object").columns)
    memory = profile.get("memory_usage_mb", 0)

    quality_word = "excellent" if score >= 80 else ("good" if score >= 60 else ("fair" if score >= 40 else "poor"))
    null_word = "minimal" if null_rate < 5 else ("moderate" if null_rate < 20 else "significant")

    summary = f"""This dataset contains **{rows:,} records** across **{cols} features** ({numeric_count} numeric, {cat_count} categorical), occupying **{memory:.2f} MB** in memory. The overall data quality is rated as **{quality_word}** ({score}/100).

{f"There are **{nulls:,} missing values** ({null_rate:.1f}% of all cells), indicating {null_word} data completeness issues that should be addressed before modeling." if nulls > 0 else "The dataset has **no missing values** — excellent data completeness!"}

{f"**{dups} duplicate rows** were detected, which could introduce bias and should be removed." if dups > 0 else "No duplicate rows were found."}

{"The high feature count relative to sample size suggests **dimensionality reduction** (e.g., PCA) may be beneficial." if cols > rows / 10 else "The feature-to-sample ratio is healthy for most ML algorithms."}

**Recommended next steps:** {"Fix missing values → " if nulls > 0 else ""}{"Remove duplicates → " if dups > 0 else ""}Apply feature scaling → {"Dimensionality reduction → " if cols > 10 else ""}Train ML model."""

    st.markdown(f"""<div style="background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.2);
border-radius:20px; padding:1.5rem 2rem; animation:fadeInUp 0.6s ease; line-height:1.8;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">
<span style="font-size:1.5rem;">🧠</span>
<span style="font-family:'Space Grotesk',sans-serif; font-weight:700;
color:#f1f5f9;">AI Analysis Report</span>
<span style="font-size:0.72rem; color:#64748b; margin-left:auto;">Generated by DataCleaner AI</span>
</div>
<div style="color:#94a3b8; font-size:0.92rem;">{summary.replace(chr(10), "<br>")}</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def _render_preprocessing_pipeline(profile: dict):
    """Render a recommended step-by-step preprocessing pipeline."""
    issues = profile.get("issues", [])
    steps = []

    if any(i["type"] == "duplicates" for i in issues):
        steps.append(("1", "Remove Duplicates", "Drop duplicate rows to prevent model bias.", "#ef4444", "🗑️"))
    if any(i["type"] == "wrong_dtype" for i in issues):
        steps.append(("2", "Fix Datatypes", "Convert numeric-string columns to numeric.", "#f59e0b", "🔧"))
    if any(i["type"] == "constant_column" for i in issues):
        steps.append(("3", "Drop Constant Columns", "Remove zero-variance features.", "#f97316", "📉"))
    if any(i["type"] == "missing_values" for i in issues):
        steps.append(("4", "Impute Missing Values", "Use median/mode strategy for missing data.", "#8b5cf6", "🕳️"))
    steps.append(("5", "Outlier Treatment", "Detect and handle anomalous data points.", "#06b6d4", "🚨"))
    steps.append(("6", "Feature Encoding", "Encode categorical variables for ML compatibility.", "#10b981", "🏷️"))
    steps.append(("7", "Feature Scaling", "Standardize numeric features for distance-based models.", "#3b82f6", "📏"))
    if profile.get("columns", 0) > 10:
        steps.append(("8", "Dimensionality Reduction", "Apply PCA if feature count is high.", "#a855f7", "🔭"))

    cols = st.columns(min(4, len(steps)))
    for i, (num, title, desc, color, icon) in enumerate(steps):
        with cols[i % 4]:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
border-radius:16px; padding:1.2rem; text-align:center; margin-bottom:1rem;
border-top:3px solid {color}; animation:fadeInUp 0.5s ease {i*0.08}s both;
transition:all 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'"
onmouseout="this.style.transform='translateY(0)'">
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.5rem;
font-weight:900; color:{color}; opacity:0.4; line-height:1;">{num}</div>
<div style="font-size:1.5rem; margin:6px 0;">{icon}</div>
<div style="font-weight:600; color:#f1f5f9; font-size:0.88rem;
margin-bottom:6px;">{title}</div>
<div style="font-size:0.78rem; color:#64748b; line-height:1.4;">{desc}</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)
