"""
DataCleaner AI — Upload Page
Dataset upload center with animated preview and profiling.
"""

import streamlit as st
import pandas as pd
import io
from components.metrics_cards import render_metric_card, render_quality_score_card, render_issue_card
from utils.data_profiler import profile_dataset


def render_upload_page():
    """Render the dataset upload and preview page."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">📁 UPLOAD CENTER</div>
<h1 class="page-title">AI Dataset <span class="gradient-text">Upload Center</span></h1>
<p class="page-subtitle">
Upload your CSV or Excel file and let the AI instantly analyze your dataset's health.
</p>
</div>
<style>
.page-header { margin-bottom: 2rem; }
.page-badge {
display: inline-block;
background: rgba(139,92,246,0.12);
border: 1px solid rgba(139,92,246,0.3);
border-radius: 999px;
padding: 5px 16px;
font-size: 0.72rem;
font-weight: 700;
letter-spacing: 0.1em;
color: #a78bfa;
margin-bottom: 1rem;
}
.page-title {
font-family: 'Space Grotesk', sans-serif !important;
font-size: 2.4rem !important;
font-weight: 800 !important;
color: #f1f5f9 !important;
margin-bottom: 0.5rem;
}
.page-subtitle { color: #94a3b8; font-size: 1rem; }
</style>""", unsafe_allow_html=True)

    # Upload Zone - Styled Native Container
    with st.container(border=True):
        col_upload, col_sample = st.columns([3, 1])
        with col_upload:
            uploaded_file = st.file_uploader(
                "Drop your CSV or Excel file here",
                type=["csv", "xlsx", "xls"],
                help="Supported formats: CSV, XLSX, XLS. Max size: 500MB",
                label_visibility="visible",
            )
        with col_sample:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Or load a sample:**")
            sample_choice = st.selectbox(
                "Sample Datasets",
                ["None", "🚢 Titanic", "🏠 Housing Prices", "🛍️ Mall Customers", "📡 Customer Churn"],
                label_visibility="collapsed",
            )
            load_sample_btn = st.button("⚡ Load Sample", use_container_width=True)

    # Load data
    df = None
    source_name = ""

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            source_name = uploaded_file.name
            st.success(f"✅ Successfully loaded **{uploaded_file.name}**")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

    elif load_sample_btn and sample_choice != "None":
        df = load_sample_dataset(sample_choice)
        source_name = sample_choice

    # If we have data from session state
    if df is None and "df_original" in st.session_state:
        df = st.session_state.df_original
        source_name = st.session_state.get("source_name", "Loaded Dataset")

    if df is not None:
        # Save to session state
        st.session_state["df_original"] = df
        st.session_state["df_cleaned"] = df.copy()
        st.session_state["source_name"] = source_name
        st.session_state["profile_before"] = profile_dataset(df)
        st.session_state["cleaning_log"] = []

        profile = st.session_state["profile_before"]

        # Dataset info banner
        st.markdown(f"""<div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
border-radius:16px; padding:1rem 1.5rem; display:flex; align-items:center;
gap:12px; margin-bottom:1.5rem; animation:fadeInUp 0.5s ease;">
<span style="font-size:1.5rem;">✅</span>
<div>
<div style="font-weight:600; color:#34d399;">Dataset Loaded Successfully</div>
<div style="font-size:0.82rem; color:#64748b;">
Source: {source_name} &nbsp;|&nbsp;
{profile['rows']:,} rows × {profile['columns']} columns &nbsp;|&nbsp;
{profile['memory_usage_mb']:.2f} MB in memory
</div>
</div>
</div>""", unsafe_allow_html=True)

        # Key Metrics Row
        st.markdown("### 📊 Dataset Overview")
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: render_metric_card("Total Rows", f"{profile['rows']:,}", "records", "📋", "purple")
        with m2: render_metric_card("Columns", str(profile['columns']), "features", "🏛️", "cyan")
        with m3: render_metric_card("Missing Values", f"{profile['total_nulls']:,}", f"{profile['null_rate']}% null rate", "🕳️", "pink")
        with m4: render_metric_card("Duplicates", f"{profile['duplicate_rows']:,}", "duplicate rows", "♊", "orange")
        with m5: render_metric_card("Memory", f"{profile['memory_usage_mb']:.2f}", "MB in memory", "💾", "green")

        st.markdown("<br>", unsafe_allow_html=True)

        # Quality Score + Column Types
        qa_col, type_col = st.columns([1, 2])
        with qa_col:
            st.markdown("### 🎯 Quality Score")
            render_quality_score_card(profile["quality_score"])

        with type_col:
            st.markdown("### 🔬 Column Type Analysis")
            col_types = profile.get("column_types", {})
            type_counts = {}
            for t in col_types.values():
                type_counts[t] = type_counts.get(t, 0) + 1

            type_colors = {
                "numeric": "#22d3ee",
                "categorical": "#a78bfa",
                "datetime": "#34d399",
                "boolean": "#fbbf24",
                "numeric_string": "#f472b6",
            }
            for dtype, count in type_counts.items():
                color = type_colors.get(dtype, "#94a3b8")
                pct = round(count / profile["columns"] * 100)
                st.markdown(f"""<div style="margin-bottom:10px;">
<div style="display:flex; justify-content:space-between; margin-bottom:4px;">
<span style="font-size:0.85rem; color:#f1f5f9; font-weight:500;">
{dtype.replace('_',' ').title()}
</span>
<span style="font-size:0.82rem; color:{color};">{count} columns ({pct}%)</span>
</div>
<div style="background:rgba(255,255,255,0.05); border-radius:999px; height:6px; overflow:hidden;">
<div style="width:{pct}%; height:100%; background:{color};
border-radius:999px; box-shadow:0 0 8px {color}60;
transition:width 1s ease;"></div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Issues detected
        issues = profile.get("issues", [])
        if issues:
            st.markdown(f"### 🚨 Detected Issues ({len(issues)})")
            for issue in issues[:10]:  # Show top 10
                render_issue_card(issue)
            if len(issues) > 10:
                st.caption(f"... and {len(issues) - 10} more issues. Run AI Cleaning Engine to fix all.")
        else:
            st.success("🎉 No major data quality issues detected!")

        st.markdown("---")

        # Data Preview
        st.markdown("### 👁️ Dataset Preview")
        preview_rows = st.slider("Rows to preview", 5, min(100, profile['rows']), 10)
        
        # Style the dataframe
        st.dataframe(
            df.head(preview_rows),
            use_container_width=True,
            height=400,
        )

        # Column Details
        with st.expander("🔍 Detailed Column Analysis", expanded=False):
            col_detail_df = pd.DataFrame({
                "Column": df.columns,
                "Type": [str(df[c].dtype) for c in df.columns],
                "AI Type": [profile["column_types"].get(c, "unknown") for c in df.columns],
                "Non-Null": [df[c].count() for c in df.columns],
                "Null Count": [df[c].isnull().sum() for c in df.columns],
                "Null %": [f"{df[c].isnull().sum() / max(len(df), 1) * 100:.1f}%" for c in df.columns],
                "Unique": [df[c].nunique() for c in df.columns],
                "Sample": [str(df[c].dropna().iloc[0]) if df[c].count() > 0 else "N/A" for c in df.columns],
            })
            st.dataframe(col_detail_df, use_container_width=True)

    else:
        # Empty state
        st.markdown("""<div style="text-align:center; padding:4rem 2rem;
background:rgba(255,255,255,0.02); border:1px dashed rgba(255,255,255,0.08);
border-radius:24px; animation:fadeInUp 0.6s ease;">
<div style="font-size:4rem; margin-bottom:1rem; animation:float 3s ease-in-out infinite;">📂</div>
<h3 style="font-family:'Space Grotesk',sans-serif; color:#f1f5f9; margin-bottom:0.5rem;">
No Dataset Loaded
</h3>
<p style="color:#64748b; font-size:0.95rem; max-width:400px; margin:0 auto;">
Upload a CSV or Excel file above, or choose a sample dataset to get started with DataCleaner AI.
</p>
</div>""", unsafe_allow_html=True)


def load_sample_dataset(choice: str) -> pd.DataFrame:
    """Load a built-in sample dataset."""
    import os
    dataset_map = {
        "🚢 Titanic": "titanic.csv",
        "🏠 Housing Prices": "house_prices.csv",
        "🛍️ Mall Customers": "mall_customers.csv",
        "📡 Customer Churn": "customer_churn.csv",
    }
    filename = dataset_map.get(choice, "titanic.csv")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "assets", "sample_datasets", filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    # Fallback: generate synthetic data
    return _generate_synthetic_dataset(choice)


def _generate_synthetic_dataset(choice: str) -> pd.DataFrame:
    """Generate synthetic sample data if file not found."""
    import numpy as np
    np.random.seed(42)
    n = 300

    if "Titanic" in choice:
        df = pd.DataFrame({
            "PassengerId": range(1, n + 1),
            "Survived": np.random.randint(0, 2, n),
            "Pclass": np.random.choice([1, 2, 3], n, p=[0.25, 0.35, 0.4]),
            "Name": [f"Passenger_{i}" for i in range(n)],
            "Sex": np.random.choice(["male", "female"], n),
            "Age": np.where(np.random.random(n) > 0.2, np.random.normal(30, 12, n), None),
            "SibSp": np.random.randint(0, 5, n),
            "Parch": np.random.randint(0, 4, n),
            "Fare": np.random.exponential(30, n),
            "Embarked": np.where(np.random.random(n) > 0.05, np.random.choice(["S", "C", "Q"], n), None),
            "Cabin": np.where(np.random.random(n) > 0.7, [f"C{i}" for i in range(n)], None),
        })
    elif "Housing" in choice:
        df = pd.DataFrame({
            "Id": range(1, n + 1),
            "LotArea": np.random.randint(3000, 20000, n),
            "YearBuilt": np.random.randint(1900, 2023, n),
            "OverallQual": np.random.randint(1, 11, n),
            "GrLivArea": np.random.randint(500, 4000, n),
            "BedroomAbvGr": np.random.randint(0, 8, n),
            "GarageArea": np.where(np.random.random(n) > 0.1, np.random.randint(0, 900, n), None),
            "Neighborhood": np.random.choice(["NoRidge", "NridgHt", "StoneBr", "Timber"], n),
            "SalePrice": np.random.normal(180000, 60000, n).clip(50000),
        })
    elif "Mall" in choice:
        df = pd.DataFrame({
            "CustomerID": range(1, n + 1),
            "Genre": np.random.choice(["Male", "Female"], n),
            "Age": np.random.randint(18, 70, n),
            "Annual Income (k$)": np.random.randint(15, 140, n),
            "Spending Score (1-100)": np.random.randint(1, 100, n),
        })
    else:  # Churn
        df = pd.DataFrame({
            "CustomerID": range(1, n + 1),
            "Gender": np.random.choice(["Male", "Female"], n),
            "Age": np.random.randint(18, 80, n),
            "Tenure": np.random.randint(0, 72, n),
            "MonthlyCharges": np.random.normal(65, 30, n).clip(18),
            "TotalCharges": np.where(np.random.random(n) > 0.1, np.random.normal(2500, 2000, n).clip(0), None),
            "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n),
            "InternetService": np.random.choice(["DSL", "Fiber optic", "No"], n),
            "Churn": np.random.choice(["Yes", "No"], n, p=[0.27, 0.73]),
        })
    return df
