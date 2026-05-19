"""
DataCleaner AI — AI Cleaning Engine Page
Auto-detect and fix data quality issues with animated workflow.
"""

import streamlit as st
import time
import pandas as pd
from components.metrics_cards import render_metric_card, render_issue_card
from utils.data_profiler import profile_dataset, detect_issues
from utils.missing_handler import handle_missing_values
from utils.feature_engineer import (
    fix_datatypes, remove_constant_columns, remove_duplicate_rows
)


def render_cleaning_engine():
    """Render the AI cleaning engine page."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">⚡ AI ENGINE</div>
<h1 class="page-title">AI Data <span class="gradient-text">Cleaning Engine</span></h1>
<p class="page-subtitle">
Intelligent detection and automated repair of all data quality issues.
</p>
</div>""".replace('\n', ' '), unsafe_allow_html=True)

    if "df_original" not in st.session_state:
        st.markdown("""<div style="text-align:center; padding:3rem; background:rgba(245,158,11,0.08);
border:1px solid rgba(245,158,11,0.2); border-radius:20px;">
<div style="font-size:3rem;">⚠️</div>
<h3 style="color:#fbbf24; font-family:'Space Grotesk',sans-serif;">No Dataset Loaded</h3>
<p style="color:#94a3b8;">Please upload a dataset first from the Upload Center.</p>
</div>""".replace('\n', ' '), unsafe_allow_html=True)
        return

    df = st.session_state.get("df_cleaned", st.session_state["df_original"]).copy()
    profile = profile_dataset(df)
    issues = profile.get("issues", [])

    # AI Suggestions Panel
    st.markdown("### 🤖 AI-Generated Cleaning Suggestions")
    if not issues:
        st.success("🎉 Your dataset is already clean! No critical issues detected.")
    else:
        st.markdown(f"""<div style="background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.2);
border-radius:16px; padding:1.2rem 1.5rem; margin-bottom:1.5rem;
animation:fadeInUp 0.5s ease;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;">
<span style="font-size:1.5rem;">🧠</span>
<span style="font-weight:700; color:#f1f5f9; font-size:1.05rem;">
AI has detected {len(issues)} data quality issues
</span>
</div>
<p style="color:#94a3b8; font-size:0.88rem; margin:0;">
Review the suggestions below and apply fixes individually or use Auto-Clean for one-click repair.
</p>
</div>""".replace('\n', ' '), unsafe_allow_html=True)

        for issue in issues:
            render_issue_card(issue)

    st.markdown("---")

    # Manual Controls
    st.markdown("### 🎛️ Manual Cleaning Controls")

    tab1, tab2, tab3, tab4 = st.tabs(["🕳️ Missing Values", "♊ Duplicates", "🔧 Datatypes", "📉 Constant Cols"])

    with tab1:
        st.markdown("**Missing Value Strategy**")
        null_cols = [c for c in df.columns if df[c].isnull().sum() > 0]
        if null_cols:
            null_strategy = st.selectbox(
                "Global strategy",
                ["auto", "mean", "median", "mode", "ffill", "bfill", "drop_rows", "zero"],
                format_func=lambda x: {
                    "auto": "🤖 Auto (median for numeric, mode for categorical)",
                    "mean": "📊 Mean imputation",
                    "median": "📊 Median imputation",
                    "mode": "📊 Mode (most frequent)",
                    "ffill": "⬆️ Forward Fill",
                    "bfill": "⬇️ Backward Fill",
                    "drop_rows": "🗑️ Drop rows with nulls",
                    "zero": "0️⃣ Fill with 0 / 'Unknown'",
                }[x],
            )
            if st.button("🔧 Fix Missing Values", use_container_width=True):
                with st.spinner("Applying missing value treatment..."):
                    df_fixed, report = handle_missing_values(df, strategy=null_strategy)
                    st.session_state["df_cleaned"] = df_fixed
                    log = f"Fixed {report.get('nulls_before', 0)} missing values using {null_strategy} strategy"
                    _add_to_log(log)
                    st.success(f"✅ {log}")
                    st.rerun()
        else:
            st.success("✅ No missing values found!")

    with tab2:
        dup_count = df.duplicated().sum()
        st.markdown(f"**{dup_count} duplicate rows** found in dataset")
        if dup_count > 0:
            if st.button("🗑️ Remove Duplicate Rows", use_container_width=True):
                df_dedup, removed = remove_duplicate_rows(df)
                st.session_state["df_cleaned"] = df_dedup
                log = f"Removed {removed} duplicate rows"
                _add_to_log(log)
                st.success(f"✅ {log}")
                st.rerun()
        else:
            st.success("✅ No duplicate rows found!")

    with tab3:
        from utils.data_profiler import classify_columns
        col_types = classify_columns(df)
        wrong_types = [c for c, t in col_types.items() if t == "numeric_string"]
        if wrong_types:
            st.markdown(f"**{len(wrong_types)} columns** have numeric data stored as strings:")
            st.write(wrong_types)
            if st.button("🔄 Fix Datatypes", use_container_width=True):
                df_fixed, fixed_cols = fix_datatypes(df)
                st.session_state["df_cleaned"] = df_fixed
                log = f"Fixed datatypes for columns: {', '.join(fixed_cols)}"
                _add_to_log(log)
                st.success(f"✅ {log}")
                st.rerun()
        else:
            st.success("✅ All column datatypes are correct!")

    with tab4:
        const_cols = [c for c in df.columns if df[c].nunique() <= 1]
        if const_cols:
            st.markdown(f"**{len(const_cols)} constant columns** detected (zero predictive value):")
            st.write(const_cols)
            if st.button("🗑️ Remove Constant Columns", use_container_width=True):
                df_fixed, removed = remove_constant_columns(df)
                st.session_state["df_cleaned"] = df_fixed
                log = f"Removed constant columns: {', '.join(removed)}"
                _add_to_log(log)
                st.success(f"✅ {log}")
                st.rerun()
        else:
            st.success("✅ No constant columns found!")

    st.markdown("---")

    # AUTO CLEAN BUTTON
    st.markdown("""<div style="text-align:center; margin: 1rem 0 0.5rem;">
<h3 style="font-family:'Space Grotesk',sans-serif; color:#f1f5f9;">One-Click AI Auto Clean</h3>
<p style="color:#94a3b8; font-size:0.9rem;">
Automatically apply the best cleaning strategy for every detected issue.
</p>
</div>""".replace('\n', ' '), unsafe_allow_html=True)

    auto_col = st.columns([1, 2, 1])[1]
    with auto_col:
        if st.button("🚀 AUTO CLEAN DATASET", use_container_width=True, type="primary"):
            _run_auto_clean()

    # Current Dataset Stats
    st.markdown("---")
    st.markdown("### 📊 Current Dataset Status")
    current_df = st.session_state.get("df_cleaned", df)
    c_profile = profile_dataset(current_df)

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Rows", f"{c_profile['rows']:,}", "after cleaning", "📋", "green")
    with c2: render_metric_card("Nulls", f"{c_profile['total_nulls']:,}", "remaining", "🕳️",
                                 "green" if c_profile['total_nulls'] == 0 else "pink")
    with c3: render_metric_card("Duplicates", f"{c_profile['duplicate_rows']:,}", "remaining", "♊",
                                  "green" if c_profile['duplicate_rows'] == 0 else "orange")
    with c4: render_metric_card("Quality", f"{c_profile['quality_score']}/100", "dataset score", "🎯", "purple")

    # Cleaning log
    cleaning_log = st.session_state.get("cleaning_log", [])
    if cleaning_log:
        with st.expander(f"📋 Cleaning Log ({len(cleaning_log)} operations)", expanded=False):
            for i, entry in enumerate(cleaning_log, 1):
                st.markdown(f"""<div style="display:flex; align-items:center; gap:10px; padding:8px 12px;
background:rgba(16,185,129,0.06); border-radius:8px; margin-bottom:6px;">
<span style="color:#34d399; font-weight:700; font-size:0.85rem;">#{i:02d}</span>
<span style="color:#94a3b8; font-size:0.85rem;">{entry}</span>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def _add_to_log(entry: str):
    """Add an entry to the cleaning log."""
    if "cleaning_log" not in st.session_state:
        st.session_state["cleaning_log"] = []
    st.session_state["cleaning_log"].append(entry)


def _run_auto_clean():
    """Execute the full auto-clean pipeline."""
    df = st.session_state.get("df_original", None)
    if df is None:
        st.error("No dataset loaded.")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()
    logs = []

    steps = [
        (10, "🔍 Analyzing dataset quality...", None),
        (25, "🗑️ Removing duplicate rows...", "duplicates"),
        (40, "🔧 Fixing column datatypes...", "dtypes"),
        (55, "📉 Removing constant columns...", "constants"),
        (70, "🕳️ Filling missing values (auto strategy)...", "missing"),
        (90, "✅ Finalizing cleaned dataset...", None),
        (100, "🎉 Auto-clean complete!", None),
    ]

    df_clean = df.copy()

    for pct, msg, action in steps:
        status_text.markdown(f"""<div style="text-align:center; padding:1rem; background:rgba(139,92,246,0.08);
border:1px solid rgba(139,92,246,0.2); border-radius:12px;">
<span style="font-size:1.1rem; color:#f1f5f9;">{msg}</span>
</div>""".replace('\n', ' '), unsafe_allow_html=True)
        progress_bar.progress(pct / 100)
        time.sleep(0.4)

        if action == "duplicates":
            df_clean, n_removed = remove_duplicate_rows(df_clean)
            if n_removed > 0:
                logs.append(f"Removed {n_removed} duplicate rows")

        elif action == "dtypes":
            df_clean, fixed = fix_datatypes(df_clean)
            if fixed:
                logs.append(f"Fixed datatypes: {', '.join(fixed)}")

        elif action == "constants":
            df_clean, removed = remove_constant_columns(df_clean)
            if removed:
                logs.append(f"Removed constant columns: {', '.join(removed)}")

        elif action == "missing":
            df_clean, report = handle_missing_values(df_clean, strategy="auto")
            nulls_fixed = report.get("nulls_before", 0) - report.get("nulls_after", 0)
            if nulls_fixed > 0:
                logs.append(f"Fixed {nulls_fixed} missing values (auto strategy)")

    st.session_state["df_cleaned"] = df_clean
    st.session_state["profile_after"] = profile_dataset(df_clean)
    if "cleaning_log" not in st.session_state:
        st.session_state["cleaning_log"] = []
    st.session_state["cleaning_log"].extend(logs)
    logs.append("✅ Auto-clean pipeline completed")

    status_text.empty()
    progress_bar.empty()
    st.success(f"🎉 Auto-clean complete! Applied {len(logs)} operations.")
    st.rerun()
