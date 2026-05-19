"""
DataCleaner AI — Outlier Detection Page
Z-Score, IQR, and Isolation Forest with live visual updates.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.outlier_detector import (
    detect_outliers_zscore,
    detect_outliers_iqr,
    detect_outliers_isolation_forest,
    remove_outliers,
)

PLOTLY_THEME = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#94a3b8",
}


def render_outlier_detection():
    """Render the outlier detection system."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">🚨 ANOMALY DETECTION</div>
<h1 class="page-title">Outlier <span class="gradient-text">Detection System</span></h1>
<p class="page-subtitle">
Three AI-powered algorithms to identify and handle anomalous data points.
</p>
</div>""", unsafe_allow_html=True)

    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df_cleaned"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns found for outlier detection.")
        return

    tab1, tab2, tab3 = st.tabs(["📐 Z-Score", "📦 IQR Method", "🌲 Isolation Forest"])

    with tab1:
        _zscore_tab(df, numeric_cols)

    with tab2:
        _iqr_tab(df, numeric_cols)

    with tab3:
        _isolation_forest_tab(df, numeric_cols)


def _zscore_tab(df, numeric_cols):
    st.markdown("#### 📐 Z-Score Outlier Detection")
    st.markdown("""<div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.2);
border-radius:12px; padding:1rem 1.5rem; margin-bottom:1rem; font-size:0.88rem; color:#94a3b8;">
Z-Score identifies outliers as data points more than <strong style="color:#a78bfa;">N standard deviations</strong>
from the mean. A threshold of 3 is standard (covers 99.7% of normal distribution).
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        threshold = st.slider("Z-Score Threshold", 1.5, 5.0, 3.0, 0.1, key="z_thresh")
        col_select = st.selectbox("Visualize Column", numeric_cols, key="z_col")

    outlier_mask, stats = detect_outliers_zscore(df, threshold)

    with c2:
        _render_outlier_stats(stats)

    # Chart
    _render_outlier_chart(df, col_select, outlier_mask, f"Z-Score (threshold={threshold})")

    # Per-column breakdown
    if stats.get("per_column"):
        _render_per_column_bars(stats["per_column"])

    # Remove button
    if stats.get("total_outliers", 0) > 0:
        if st.button(f"🗑️ Remove {stats['total_outliers']} Outliers (Z-Score)", key="remove_z"):
            df_clean, n = remove_outliers(df, outlier_mask)
            st.session_state["df_cleaned"] = df_clean
            st.session_state.setdefault("cleaning_log", []).append(
                f"Removed {n} outliers via Z-Score (threshold={threshold})"
            )
            st.success(f"✅ Removed {n} outlier rows.")
            st.rerun()


def _iqr_tab(df, numeric_cols):
    st.markdown("#### 📦 IQR-Based Outlier Detection")
    st.markdown("""<div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.2);
border-radius:12px; padding:1rem 1.5rem; margin-bottom:1rem; font-size:0.88rem; color:#94a3b8;">
IQR method flags points outside <strong style="color:#22d3ee;">[Q1 − k·IQR, Q3 + k·IQR]</strong>.
More robust than Z-score for non-normal distributions.
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        multiplier = st.slider("IQR Multiplier (k)", 0.5, 4.0, 1.5, 0.1, key="iqr_mult")
        col_select = st.selectbox("Visualize Column", numeric_cols, key="iqr_col")

    outlier_mask, stats = detect_outliers_iqr(df, multiplier)

    with c2:
        _render_outlier_stats(stats)

    _render_outlier_chart(df, col_select, outlier_mask, f"IQR (multiplier={multiplier})")

    if stats.get("per_column"):
        _render_per_column_bars(stats["per_column"])

    if stats.get("total_outliers", 0) > 0:
        if st.button(f"🗑️ Remove {stats['total_outliers']} Outliers (IQR)", key="remove_iqr"):
            df_clean, n = remove_outliers(df, outlier_mask)
            st.session_state["df_cleaned"] = df_clean
            st.session_state.setdefault("cleaning_log", []).append(
                f"Removed {n} outliers via IQR (k={multiplier})"
            )
            st.success(f"✅ Removed {n} outlier rows.")
            st.rerun()


def _isolation_forest_tab(df, numeric_cols):
    st.markdown("#### 🌲 Isolation Forest Anomaly Detection")
    st.markdown("""<div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
border-radius:12px; padding:1rem 1.5rem; margin-bottom:1rem; font-size:0.88rem; color:#94a3b8;">
Isolation Forest is an unsupervised ML algorithm that isolates anomalies using random decision trees.
Excellent for <strong style="color:#34d399;">high-dimensional multivariate anomaly detection</strong>.
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        contamination = st.slider("Expected Contamination %", 1, 20, 5, 1, key="iso_cont") / 100
        col_select = st.selectbox("Visualize Column", numeric_cols, key="iso_col")
        run_btn = st.button("🌲 Run Isolation Forest", use_container_width=True, key="run_iso")

    if run_btn:
        with st.spinner("Training Isolation Forest model..."):
            outlier_mask, stats = detect_outliers_isolation_forest(df, contamination)
        st.session_state["iso_mask"] = outlier_mask
        st.session_state["iso_stats"] = stats

    if "iso_mask" in st.session_state:
        outlier_mask = st.session_state["iso_mask"]
        stats = st.session_state["iso_stats"]

        with c2:
            _render_outlier_stats(stats)

        _render_outlier_chart(df, col_select, outlier_mask, "Isolation Forest")

        # Anomaly scores histogram
        if "anomaly_scores" in stats:
            scores = stats["anomaly_scores"]
            fig = go.Figure(data=[
                go.Histogram(
                    x=scores,
                    nbinsx=40,
                    marker=dict(
                        color="rgba(139,92,246,0.6)",
                        line=dict(color="#8b5cf6", width=1),
                    ),
                    name="Anomaly Scores",
                )
            ])
            fig.add_vline(x=np.percentile(scores, int(contamination * 100)),
                          line_dash="dash", line_color="#ef4444",
                          annotation_text="Anomaly Threshold",
                          annotation_font_color="#ef4444")
            fig.update_layout(
                **PLOTLY_THEME,
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                title=dict(text="Anomaly Score Distribution", x=0.5, font=dict(color="#f1f5f9")),
                xaxis_title="Score (lower = more anomalous)",
            )
            st.plotly_chart(fig, use_container_width=True)

        if stats.get("total_outliers", 0) > 0:
            if st.button(f"🗑️ Remove {stats['total_outliers']} Anomalies", key="remove_iso"):
                df_clean, n = remove_outliers(df, outlier_mask)
                st.session_state["df_cleaned"] = df_clean
                st.session_state.pop("iso_mask", None)
                st.session_state.pop("iso_stats", None)
                st.session_state.setdefault("cleaning_log", []).append(
                    f"Removed {n} anomalies via Isolation Forest (contamination={contamination:.0%})"
                )
                st.success(f"✅ Removed {n} anomalous rows.")
                st.rerun()
    else:
        st.info("Click **Run Isolation Forest** to detect anomalies using ML.")


def _render_outlier_stats(stats: dict):
    """Display outlier stats in a styled card."""
    total = stats.get("total_outliers", 0)
    pct = stats.get("outlier_pct", 0)
    method = stats.get("method", "")
    color = "#ef4444" if pct > 10 else ("#f59e0b" if pct > 5 else "#10b981")

    st.markdown(f"""<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
border-radius:16px; padding:1.2rem; text-align:center; animation:fadeInUp 0.5s ease;">
<div style="font-size:0.72rem; color:#64748b; text-transform:uppercase;
letter-spacing:0.1em; margin-bottom:8px;">{method}</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:2.5rem;
font-weight:800; color:{color}; line-height:1;">{total:,}</div>
<div style="font-size:0.85rem; color:#94a3b8; margin-top:4px;">
outliers detected ({pct}% of data)
</div>
</div>""", unsafe_allow_html=True)


def _render_outlier_chart(df, col, outlier_mask, title):
    """Scatter chart with outliers highlighted in red."""
    if col not in df.columns:
        return

    series = df[col].reset_index(drop=True)
    mask = outlier_mask.reset_index(drop=True)

    normal_x = series[~mask].index.tolist()
    normal_y = series[~mask].tolist()
    outlier_x = series[mask].index.tolist()
    outlier_y = series[mask].tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=normal_x, y=normal_y, mode="markers",
        name="Normal",
        marker=dict(color="rgba(139,92,246,0.5)", size=4, line=dict(width=0)),
    ))
    fig.add_trace(go.Scatter(
        x=outlier_x, y=outlier_y, mode="markers",
        name="Outlier",
        marker=dict(
            color="#ef4444", size=8,
            line=dict(color="#ff0000", width=1),
            symbol="x",
        ),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(text=f"{col} — {title}", x=0.5, font=dict(color="#f1f5f9", size=14)),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis_title="Index",
        yaxis_title=col,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_per_column_bars(per_col: dict):
    """Bar chart of outlier counts per column."""
    items = [(k, v) for k, v in per_col.items() if v > 0]
    if not items:
        return
    items.sort(key=lambda x: x[1], reverse=True)
    cols, counts = zip(*items)

    fig = px.bar(
        x=list(cols), y=list(counts),
        color=list(counts),
        color_continuous_scale=[[0, "#8b5cf6"], [1, "#ef4444"]],
        labels={"x": "Column", "y": "Outlier Count"},
    )
    fig.update_layout(
        **PLOTLY_THEME,
        height=280,
        margin=dict(l=20, r=20, t=30, b=30),
        showlegend=False,
        title=dict(text="Outliers per Column", x=0.5, font=dict(color="#f1f5f9", size=13)),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)
