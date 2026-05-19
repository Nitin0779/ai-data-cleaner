"""
DataCleaner AI — Feature Engineering Studio Page
Encoding, scaling, and PCA with live previews.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.feature_engineer import (
    label_encode, one_hot_encode, scale_features, apply_pca
)

PLOTLY_THEME = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#94a3b8",
}


def render_feature_engineering():
    """Render the feature engineering studio."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">🧬 FEATURE STUDIO</div>
<h1 class="page-title">Feature Engineering <span class="gradient-text">Studio</span></h1>
<p class="page-subtitle">
Transform, encode, and scale your features for optimal ML performance.
</p>
</div>""", unsafe_allow_html=True)

    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first.")
        return

    df = st.session_state["df_cleaned"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏷️ Encoding", "📏 Scaling", "🔭 PCA", "👁️ Preview"
    ])

    with tab1:
        _encoding_tab(df, cat_cols)

    with tab2:
        _scaling_tab(df, numeric_cols)

    with tab3:
        _pca_tab(df, numeric_cols)

    with tab4:
        _preview_tab()


def _encoding_tab(df, cat_cols):
    st.markdown("#### 🏷️ Categorical Encoding")

    if not cat_cols:
        st.success("✅ No categorical columns to encode!")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        encoding_method = st.radio(
            "Encoding Method",
            ["Label Encoding", "One-Hot Encoding"],
            key="enc_method",
        )
        cols_to_encode = st.multiselect(
            "Select Columns",
            cat_cols,
            default=cat_cols[:min(3, len(cat_cols))],
            key="enc_cols",
        )

        if encoding_method == "One-Hot Encoding":
            drop_first = st.checkbox("Drop first category (avoid multicollinearity)", value=True)

    with col2:
        if cols_to_encode:
            st.markdown("**Preview:**")
            preview = df[cols_to_encode].head(5)
            st.dataframe(preview, use_container_width=True)

            # Cardinality info
            for col in cols_to_encode:
                n_unique = df[col].nunique()
                if encoding_method == "One-Hot Encoding" and n_unique > 20:
                    st.warning(f"⚠️ `{col}` has {n_unique} categories — one-hot encoding will add {n_unique} columns!")
                else:
                    st.markdown(f"<span style='color:#94a3b8; font-size:0.82rem;'>📌 {col}: {n_unique} unique values</span>", unsafe_allow_html=True)

    if cols_to_encode and st.button("✅ Apply Encoding", use_container_width=True, key="apply_enc"):
        try:
            if encoding_method == "Label Encoding":
                df_enc, mappings = label_encode(df, cols_to_encode)
                log = f"Label encoded: {', '.join(cols_to_encode)}"
            else:
                df_enc = one_hot_encode(df, cols_to_encode, drop_first=drop_first)
                new_cols = len(df_enc.columns) - len(df.columns) + len(cols_to_encode)
                log = f"One-hot encoded: {', '.join(cols_to_encode)} (+{new_cols} columns)"

            st.session_state["df_cleaned"] = df_enc
            st.session_state.setdefault("cleaning_log", []).append(log)
            st.success(f"✅ {log}")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Encoding error: {str(e)}")


def _scaling_tab(df, numeric_cols):
    st.markdown("#### 📏 Feature Scaling")

    if not numeric_cols:
        st.warning("No numeric columns found.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        scaler_method = st.radio(
            "Scaling Method",
            ["standard", "minmax", "robust"],
            format_func=lambda x: {
                "standard": "📊 StandardScaler (z-score normalization)",
                "minmax": "📐 MinMaxScaler (0–1 range)",
                "robust": "🛡️ RobustScaler (median-based, outlier-robust)",
            }[x],
            key="scale_method",
        )
        cols_to_scale = st.multiselect(
            "Select Columns to Scale",
            numeric_cols,
            default=numeric_cols[:min(4, len(numeric_cols))],
            key="scale_cols",
        )

    with col2:
        if cols_to_scale:
            st.markdown("**Before scaling:**")
            stats = df[cols_to_scale].describe().round(2)
            st.dataframe(stats, use_container_width=True)

    # Method explanation
    explanations = {
        "standard": "StandardScaler transforms features to have **mean=0** and **std=1**. Best for algorithms that assume normal distribution (SVM, logistic regression, PCA).",
        "minmax": "MinMaxScaler scales features to a **fixed range [0, 1]**. Preserves zero in sparse data. Sensitive to outliers.",
        "robust": "RobustScaler uses **median and IQR** instead of mean and std. Excellent choice when your data contains outliers.",
    }
    st.markdown(f"""<div style="background:rgba(6,182,212,0.06); border:1px solid rgba(6,182,212,0.2);
border-radius:12px; padding:1rem 1.5rem; font-size:0.88rem; color:#94a3b8; margin:0.5rem 0;">
ℹ️ {explanations[scaler_method]}
</div>""", unsafe_allow_html=True)

    if cols_to_scale and st.button("📏 Apply Scaling", use_container_width=True, key="apply_scale"):
        try:
            df_scaled, scaler = scale_features(df, cols_to_scale, scaler_method)
            st.session_state["df_cleaned"] = df_scaled
            log = f"Applied {scaler_method} scaling to: {', '.join(cols_to_scale)}"
            st.session_state.setdefault("cleaning_log", []).append(log)
            st.success(f"✅ {log}")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Scaling error: {str(e)}")


def _pca_tab(df, numeric_cols):
    st.markdown("#### 🔭 PCA — Dimensionality Reduction")

    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for PCA.")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        n_components = st.slider("Number of Components", 2, min(10, len(numeric_cols)), 2, key="pca_n")
        pca_cols = st.multiselect(
            "Columns to Reduce",
            numeric_cols,
            default=numeric_cols,
            key="pca_cols",
        )
        run_pca = st.button("🔭 Run PCA", use_container_width=True, key="run_pca")

    if run_pca and len(pca_cols) >= 2:
        try:
            pca_df, pca_obj, var_ratio = apply_pca(df, n_components, pca_cols)
            st.session_state["pca_result"] = pca_df
            st.session_state["pca_var_ratio"] = var_ratio.tolist()
            st.success(f"✅ PCA complete! Reduced {len(pca_cols)} features → {n_components} components")
        except Exception as e:
            st.error(f"❌ PCA error: {str(e)}")

    with col2:
        if "pca_var_ratio" in st.session_state:
            var_ratio = st.session_state["pca_var_ratio"]
            cum_var = [sum(var_ratio[:i+1]) for i in range(len(var_ratio))]
            pc_labels = [f"PC{i+1}" for i in range(len(var_ratio))]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=pc_labels, y=[v * 100 for v in var_ratio],
                name="Explained Variance",
                marker=dict(color="rgba(139,92,246,0.7)", line=dict(color="#8b5cf6", width=1)),
            ))
            fig.add_trace(go.Scatter(
                x=pc_labels, y=[v * 100 for v in cum_var],
                name="Cumulative Variance",
                line=dict(color="#06b6d4", width=2, dash="dot"),
                mode="lines+markers",
            ))
            fig.add_hline(y=95, line_dash="dash", line_color="#f59e0b",
                          annotation_text="95% threshold", annotation_font_color="#fbbf24")
            fig.update_layout(
                **PLOTLY_THEME,
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                title=dict(text="Explained Variance by Component", x=0.5, font=dict(color="#f1f5f9")),
                yaxis_title="Variance Explained (%)",
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # 2D PCA scatter
            if "pca_result" in st.session_state and "PC1" in st.session_state["pca_result"].columns:
                pca_data = st.session_state["pca_result"]
                fig2 = px.scatter(
                    pca_data, x="PC1", y="PC2",
                    color_discrete_sequence=["#8b5cf6"],
                    opacity=0.7,
                    labels={"PC1": f"PC1 ({var_ratio[0]*100:.1f}%)",
                            "PC2": f"PC2 ({var_ratio[1]*100:.1f}%)"},
                )
                fig2.update_layout(**PLOTLY_THEME, height=350,
                                   margin=dict(l=20, r=20, t=40, b=20),
                                   title=dict(text="PCA 2D Projection", x=0.5, font=dict(color="#f1f5f9")))
                fig2.update_traces(marker=dict(size=5, line=dict(width=0)))
                st.plotly_chart(fig2, use_container_width=True)

    if "pca_result" in st.session_state:
        if st.button("💾 Replace Features with PCA Components", key="apply_pca"):
            pca_data = st.session_state["pca_result"]
            pca_cols_set = set(pca_cols if "pca_cols" in st.session_state else [])
            other_cols = df.drop(columns=[c for c in pca_cols if c in df.columns], errors="ignore")
            combined = pd.concat([other_cols.reset_index(drop=True), pca_data.reset_index(drop=True)], axis=1)
            st.session_state["df_cleaned"] = combined
            log = f"Replaced {len(pca_cols)} features with {len(pca_data.columns)} PCA components"
            st.session_state.setdefault("cleaning_log", []).append(log)
            st.success(f"✅ {log}")
            st.rerun()


def _preview_tab():
    st.markdown("#### 👁️ Current Dataset Preview")
    df = st.session_state.get("df_cleaned")
    if df is None:
        st.warning("No dataset available.")
        return

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Rows", f"{len(df):,}")
    with col2: st.metric("Columns", len(df.columns))
    with col3: st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

    st.dataframe(df.head(50), use_container_width=True, height=450)

    # Dtype summary
    with st.expander("📋 Column Types Summary"):
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype": [str(df[c].dtype) for c in df.columns],
            "Non-Null": [df[c].count() for c in df.columns],
            "Unique": [df[c].nunique() for c in df.columns],
        })
        st.dataframe(dtype_df, use_container_width=True)
