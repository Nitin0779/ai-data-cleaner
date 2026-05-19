"""
DataCleaner AI — Visualization Lab Page
Interactive Plotly charts for deep data analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


PLOTLY_THEME = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#94a3b8",
    "font_family": "Inter",
}

NEON_COLORS = [
    "#8b5cf6", "#06b6d4", "#ec4899", "#10b981",
    "#f59e0b", "#3b82f6", "#f97316", "#a855f7",
]


def render_visualization_lab():
    """Render the interactive visualization lab."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">📊 VIZ LAB</div>
<h1 class="page-title">Visualization <span class="gradient-text">Lab</span></h1>
<p class="page-subtitle">
Explore your data with stunning interactive Plotly charts. Every insight, beautifully visualized.
</p>
</div>""", unsafe_allow_html=True)

    if "df_cleaned" not in st.session_state:
        _no_data_message()
        return

    df = st.session_state["df_cleaned"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔥 Correlation", "📊 Distributions",
        "📦 Boxplots", "🔵 Scatter", "🌐 3D Plot", "🎭 Missing Map"
    ])

    with tab1:
        _render_correlation_tab(df, numeric_cols)

    with tab2:
        _render_distributions_tab(df, numeric_cols, cat_cols)

    with tab3:
        _render_boxplot_tab(df, numeric_cols, cat_cols)

    with tab4:
        _render_scatter_tab(df, numeric_cols, cat_cols)

    with tab5:
        _render_3d_tab(df, numeric_cols)

    with tab6:
        _render_missing_map(df)


def _render_correlation_tab(df, numeric_cols):
    st.markdown("#### 🔥 Correlation Heatmap")
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for correlation analysis.")
        return

    corr = df[numeric_cols].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale=[
            [0.0, "#1e0533"],
            [0.25, "#5b21b6"],
            [0.5, "#1e293b"],
            [0.75, "#0369a1"],
            [1.0, "#06b6d4"],
        ],
        text=corr.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False,
        zmin=-1, zmax=1,
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text="Feature Correlation Matrix", x=0.5, font=dict(color="#f1f5f9", size=16)),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Highlight high correlations
    high_corr = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            val = abs(corr.iloc[i, j])
            if val > 0.7:
                high_corr.append((corr.columns[i], corr.columns[j], round(corr.iloc[i, j], 3)))

    if high_corr:
        st.markdown("##### ⚡ High Correlation Pairs")
        for c1, c2, val in high_corr:
            color = "#ef4444" if abs(val) > 0.9 else "#f59e0b"
            st.markdown(f"""<div style="display:flex; align-items:center; justify-content:space-between;
padding:10px 16px; background:rgba(255,255,255,0.03);
border:1px solid rgba(255,255,255,0.08); border-radius:12px; margin-bottom:6px;">
<span style="color:#f1f5f9; font-weight:500;">{c1} ↔ {c2}</span>
<span style="color:{color}; font-weight:700; font-family:'JetBrains Mono',monospace;">r = {val}</span>
</div>""", unsafe_allow_html=True)


def _render_distributions_tab(df, numeric_cols, cat_cols):
    st.markdown("#### 📊 Feature Distributions")
    if not numeric_cols:
        st.warning("No numeric columns found.")
        return

    col1, col2 = st.columns([1, 3])
    with col1:
        selected_col = st.selectbox("Select Column", numeric_cols, key="dist_col")
        color_col = st.selectbox("Color by", ["None"] + cat_cols, key="dist_color")
        n_bins = st.slider("Bins", 10, 100, 30, key="dist_bins")

    with col2:
        color = color_col if color_col != "None" else None
        fig = px.histogram(
            df, x=selected_col,
            color=color,
            nbins=n_bins,
            marginal="violin",
            color_discrete_sequence=NEON_COLORS,
            opacity=0.85,
        )
        fig.update_layout(
            **PLOTLY_THEME,
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            bargap=0.05,
            title=dict(text=f"Distribution of {selected_col}", x=0.5, font=dict(color="#f1f5f9")),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Stats summary
    stats = df[selected_col].describe()
    s1, s2, s3, s4 = st.columns(4)
    with s1: st.metric("Mean", f"{stats['mean']:.2f}")
    with s2: st.metric("Std Dev", f"{stats['std']:.2f}")
    with s3: st.metric("Min", f"{stats['min']:.2f}")
    with s4: st.metric("Max", f"{stats['max']:.2f}")


def _render_boxplot_tab(df, numeric_cols, cat_cols):
    st.markdown("#### 📦 Box & Violin Plots")
    if not numeric_cols:
        st.warning("No numeric columns found.")
        return

    col1, col2 = st.columns([1, 3])
    with col1:
        y_col = st.selectbox("Y-Axis (Numeric)", numeric_cols, key="box_y")
        x_col = st.selectbox("X-Axis (Group by)", ["None"] + cat_cols, key="box_x")
        plot_type = st.radio("Plot Type", ["Box", "Violin"], key="box_type", horizontal=True)

    with col2:
        x = x_col if x_col != "None" else None
        if plot_type == "Box":
            fig = px.box(
                df, x=x, y=y_col,
                color=x,
                color_discrete_sequence=NEON_COLORS,
                points="outliers",
                notched=True,
            )
        else:
            fig = px.violin(
                df, x=x, y=y_col,
                color=x,
                color_discrete_sequence=NEON_COLORS,
                box=True,
                points="outliers",
            )
        fig.update_layout(
            **PLOTLY_THEME,
            height=450,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False,
            title=dict(text=f"{plot_type} Plot: {y_col}", x=0.5, font=dict(color="#f1f5f9")),
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_scatter_tab(df, numeric_cols, cat_cols):
    st.markdown("#### 🔵 Scatter Plot")
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns.")
        return

    c1, c2, c3 = st.columns(3)
    with c1: x_col = st.selectbox("X-Axis", numeric_cols, key="sc_x")
    with c2: y_col = st.selectbox("Y-Axis", numeric_cols, index=min(1, len(numeric_cols)-1), key="sc_y")
    with c3: color_col = st.selectbox("Color", ["None"] + cat_cols + numeric_cols, key="sc_c")

    color = color_col if color_col != "None" else None
    size_col = None
    if len(numeric_cols) > 2:
        size_col = [c for c in numeric_cols if c not in [x_col, y_col]]
        size_col = size_col[0] if size_col else None

    fig = px.scatter(
        df.sample(min(2000, len(df))),
        x=x_col, y=y_col,
        color=color,
        color_discrete_sequence=NEON_COLORS,
        color_continuous_scale="Viridis",
        opacity=0.75,
        hover_data=df.columns[:5].tolist(),
        trendline="ols" if not color else None,
    )
    fig.update_layout(
        **PLOTLY_THEME,
        height=480,
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text=f"Scatter: {x_col} vs {y_col}", x=0.5, font=dict(color="#f1f5f9")),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0)))
    st.plotly_chart(fig, use_container_width=True)


def _render_3d_tab(df, numeric_cols):
    st.markdown("#### 🌐 3D Scatter Plot")
    if len(numeric_cols) < 3:
        st.warning("Need at least 3 numeric columns for 3D visualization.")
        return

    c1, c2, c3 = st.columns(3)
    with c1: x = st.selectbox("X-Axis", numeric_cols, key="3d_x")
    with c2: y = st.selectbox("Y-Axis", numeric_cols, index=1, key="3d_y")
    with c3: z = st.selectbox("Z-Axis", numeric_cols, index=2, key="3d_z")

    sample_df = df[[x, y, z]].dropna().sample(min(1500, len(df)))

    fig = go.Figure(data=[go.Scatter3d(
        x=sample_df[x],
        y=sample_df[y],
        z=sample_df[z],
        mode="markers",
        marker=dict(
            size=4,
            color=sample_df[z],
            colorscale=[[0, "#8b5cf6"], [0.5, "#06b6d4"], [1, "#ec4899"]],
            opacity=0.85,
            line=dict(width=0),
        ),
    )])
    fig.update_layout(
        **PLOTLY_THEME,
        height=550,
        margin=dict(l=0, r=0, t=40, b=0),
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=x, color="#94a3b8"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=y, color="#94a3b8"),
            zaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=z, color="#94a3b8"),
        ),
        title=dict(text="3D Feature Space", x=0.5, font=dict(color="#f1f5f9")),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_missing_map(df):
    st.markdown("#### 🎭 Missing Value Map")
    missing_pct = (df.isnull().sum() / len(df) * 100).reset_index()
    missing_pct.columns = ["Column", "Missing %"]
    missing_pct = missing_pct.sort_values("Missing %", ascending=True)

    if missing_pct["Missing %"].max() == 0:
        st.success("🎉 No missing values in the cleaned dataset!")
        return

    fig = px.bar(
        missing_pct[missing_pct["Missing %"] > 0],
        x="Missing %", y="Column",
        orientation="h",
        color="Missing %",
        color_continuous_scale=[[0, "#06b6d4"], [0.5, "#f59e0b"], [1, "#ef4444"]],
        text="Missing %",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        **PLOTLY_THEME,
        height=max(300, 30 * len(missing_pct[missing_pct["Missing %"] > 0]) + 100),
        margin=dict(l=20, r=80, t=40, b=20),
        title=dict(text="Missing Value Distribution by Column", x=0.5, font=dict(color="#f1f5f9")),
        showlegend=False,
        xaxis=dict(range=[0, 110]),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap-style missing grid (sample)
    st.markdown("##### 🗺️ Missing Value Grid (Sampled 100 rows)")
    sample = df.head(100).isnull().astype(int)
    fig2 = go.Figure(data=go.Heatmap(
        z=sample.values.T,
        x=list(range(len(sample))),
        y=sample.columns.tolist(),
        colorscale=[[0, "rgba(139,92,246,0.2)"], [1, "#ef4444"]],
        showscale=False,
        hovertemplate="Row: %{x}<br>Col: %{y}<br>Missing: %{z}<extra></extra>",
    ))
    fig2.update_layout(
        **PLOTLY_THEME,
        height=max(250, 20 * len(df.columns) + 60),
        margin=dict(l=10, r=10, t=20, b=20),
    )
    st.plotly_chart(fig2, use_container_width=True)


def _no_data_message():
    st.markdown("""<div style="text-align:center; padding:3rem; background:rgba(245,158,11,0.08);
border:1px solid rgba(245,158,11,0.2); border-radius:20px;">
<div style="font-size:3rem;">⚠️</div>
<h3 style="color:#fbbf24; font-family:'Space Grotesk',sans-serif;">No Dataset Loaded</h3>
<p style="color:#94a3b8;">Please upload a dataset first from the Upload Center.</p>
</div>""", unsafe_allow_html=True)
