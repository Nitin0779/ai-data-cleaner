"""
DataCleaner AI — Export System Page
Download cleaned dataset, reports, and visualizations.
"""

import streamlit as st
import pandas as pd
import io
import json
from datetime import datetime
from utils.data_profiler import profile_dataset
from utils.report_generator import generate_json_report, generate_pdf_report


def render_export():
    """Render the export system page."""

    st.markdown("""<div class="page-header fade-in-up">
<div class="page-badge">📤 EXPORT</div>
<h1 class="page-title">Export <span class="gradient-text">System</span></h1>
<p class="page-subtitle">
Download your cleaned dataset, preprocessing reports, and share your results.
</p>
</div>""", unsafe_allow_html=True)

    if "df_cleaned" not in st.session_state:
        st.warning("⚠️ Please upload and clean a dataset first.")
        return

    df_orig  = st.session_state.get("df_original", pd.DataFrame())
    df_clean = st.session_state["df_cleaned"]
    cleaning_log = st.session_state.get("cleaning_log", [])
    p_before = st.session_state.get("profile_before", profile_dataset(df_orig))
    p_after  = profile_dataset(df_clean)

    # ── EXPORT OVERVIEW ────────────────────────────────────────────────
    rows_saved   = p_after["rows"]
    cols_saved   = p_after["columns"]
    nulls_fixed  = p_before.get("total_nulls", 0) - p_after["total_nulls"]
    ops_count    = len(cleaning_log)

    st.markdown(f"""<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:1rem;
margin-bottom:2rem; animation:fadeInUp 0.6s ease;">
{"".join([_stat_card(icon, val, label, color) for icon, val, label, color in [
("📋", f"{rows_saved:,}", "Rows in Clean Dataset", "#8b5cf6"),
("🏛️", str(cols_saved), "Features Retained", "#06b6d4"),
("✅", f"{nulls_fixed:,}", "Issues Fixed", "#10b981"),
("⚙️", str(ops_count), "Operations Applied", "#f59e0b"),
]])}
</div>""", unsafe_allow_html=True)

    # ── DOWNLOAD CARDS ─────────────────────────────────────────────────
    st.markdown("### 📦 Download Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        _render_download_card(
            "🟢", "Cleaned Dataset",
            "Download your fully cleaned and preprocessed dataset as a CSV file.",
            "CSV File",
            _get_csv_bytes(df_clean),
            f"datacleaner_cleaned_{_timestamp()}.csv",
            "text/csv",
            "#10b981",
        )

    with col2:
        _render_download_card(
            "🔵", "JSON Report",
            "Comprehensive machine-readable report of all cleaning operations and statistics.",
            "JSON File",
            _get_json_bytes(df_orig, df_clean, p_before, p_after, cleaning_log),
            f"datacleaner_report_{_timestamp()}.json",
            "application/json",
            "#06b6d4",
        )

    with col3:
        _render_download_card(
            "🟣", "PDF Report",
            "Professional PDF report with full dataset comparison, suitable for sharing.",
            "PDF File",
            _get_pdf_bytes(df_orig, df_clean, p_before, p_after, cleaning_log),
            f"datacleaner_report_{_timestamp()}.pdf",
            "application/pdf",
            "#8b5cf6",
        )

    st.markdown("---")

    # ── ORIGINAL DATASET DOWNLOAD ──────────────────────────────────────
    st.markdown("### 📁 Additional Downloads")
    c1, c2 = st.columns(2)

    with c1:
        orig_csv = _get_csv_bytes(df_orig)
        st.download_button(
            "⬇️ Download Original Dataset (CSV)",
            data=orig_csv,
            file_name=f"datacleaner_original_{_timestamp()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with c2:
        # Cleaning log as TXT
        log_txt = "\n".join([f"{i+1}. {entry}" for i, entry in enumerate(cleaning_log)])
        log_txt = f"DataCleaner AI — Cleaning Log\nGenerated: {datetime.now()}\n\n{log_txt}"
        st.download_button(
            "⬇️ Download Cleaning Log (TXT)",
            data=log_txt.encode("utf-8"),
            file_name=f"cleaning_log_{_timestamp()}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")

    # ── DATA PREVIEW ───────────────────────────────────────────────────
    st.markdown("### 👁️ Cleaned Dataset Preview")
    st.dataframe(df_clean.head(20), use_container_width=True, height=400)

    # ── SHARE SECTION ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="text-align:center; padding:2rem; background:rgba(139,92,246,0.06);
border:1px solid rgba(139,92,246,0.2); border-radius:20px; animation:fadeInUp 0.6s ease;">
<div style="font-size:2rem; margin-bottom:0.8rem;">🚀</div>
<h3 style="font-family:'Space Grotesk',sans-serif; color:#f1f5f9; margin-bottom:0.5rem;">
Share Your Work
</h3>
<p style="color:#94a3b8; font-size:0.9rem; max-width:500px; margin:0 auto 1.2rem;">
Built with DataCleaner AI — a premium open-source data preprocessing platform.
Star us on GitHub and share your experience!
</p>
<div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
<div class="share-btn" style="background:rgba(139,92,246,0.15);
border:1px solid rgba(139,92,246,0.3); color:#a78bfa;">
⭐ Star on GitHub
</div>
<div class="share-btn" style="background:rgba(6,182,212,0.15);
border:1px solid rgba(6,182,212,0.3); color:#22d3ee;">
🔗 Share on LinkedIn
</div>
</div>
</div>
<style>
.share-btn {
padding: 10px 20px; border-radius: 999px;
font-size: 0.88rem; font-weight: 600;
cursor: default; transition: all 0.2s ease;
}
.share-btn:hover { transform: translateY(-2px); filter: brightness(1.2); }
</style>""", unsafe_allow_html=True)


def _stat_card(icon, value, label, color):
    return f"""<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
border-top:3px solid {color}; border-radius:16px; padding:1.2rem; text-align:center;">
<div style="font-size:1.8rem; margin-bottom:6px;">{icon}</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.6rem;
font-weight:800; color:{color}; line-height:1;">{value}</div>
<div style="font-size:0.75rem; color:#64748b; margin-top:4px;">{label}</div>
</div>"""


def _render_download_card(dot, title, desc, format_label, data, filename, mime, color):
    """Render a styled download card."""
    st.markdown(f"""<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
border-radius:20px; padding:1.5rem; margin-bottom:0.5rem;
border-top:3px solid {color}; animation:fadeInUp 0.5s ease; transition:all 0.3s ease;"
onmouseover="this.style.transform='translateY(-4px)'"
onmouseout="this.style.transform='translateY(0)'">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
<span style="font-size:1.5rem;">{dot}</span>
<div>
<div style="font-weight:700; color:#f1f5f9; font-size:1rem;">{title}</div>
<div style="font-size:0.72rem; color:{color}; font-weight:600;">{format_label}</div>
</div>
</div>
<div style="font-size:0.82rem; color:#64748b; line-height:1.5; margin-bottom:1rem;">{desc}</div>
</div>""", unsafe_allow_html=True)

    st.download_button(
        f"⬇️ Download {title}",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True,
    )


def _get_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def _get_json_bytes(df_orig, df_clean, p_before, p_after, cleaning_log) -> bytes:
    report = generate_json_report(df_orig, df_clean, p_before, p_after, cleaning_log)
    return report.encode("utf-8")


def _get_pdf_bytes(df_orig, df_clean, p_before, p_after, cleaning_log) -> bytes:
    return generate_pdf_report(df_orig, df_clean, p_before, p_after, cleaning_log)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
