"""
DataCleaner AI — Main Application Entry Point
Premium AI-powered data preprocessing platform.

Author: DataCleaner AI Team
Version: 2.0 Pro
"""

import streamlit as st
import os

# ── PAGE CONFIG (must be first Streamlit call) ─────────────────────────
st.set_page_config(
    page_title="DataCleaner AI — Premium Data Preprocessing",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "DataCleaner AI v2.0 Pro — Premium AI Data Preprocessing Platform",
    },
)

# ── LOAD CSS ────────────────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

# ── GOOGLE FONTS ────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ── IMPORT VIEWS ────────────────────────────────────────────────────────
from views.home              import render_home
from views.upload_page       import render_upload_page
from views.cleaning_engine   import render_cleaning_engine
from views.visualization_lab import render_visualization_lab
from views.outlier_detection  import render_outlier_detection
from views.feature_engineering import render_feature_engineering
from views.ai_insights_page  import render_ai_insights
from views.before_after      import render_before_after
from views.export            import render_export
from components.header       import render_header

# ── SESSION STATE INIT ─────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"
if "cleaning_log" not in st.session_state:
    st.session_state["cleaning_log"] = []

# ── SIDEBAR ─────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Logo ──────────────────────────────────────────────────────────
    st.markdown("""<div style="padding:1.2rem 0.5rem 0.8rem; text-align:center;">
<div style="display:flex;align-items:center;justify-content:center;gap:10px;">
<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
<rect width="32" height="32" rx="10" fill="url(#lg1)"/>
<path d="M9 16L13 11L18 18L23 13" stroke="white" stroke-width="2.5"
stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="9" cy="16" r="2.5" fill="white" opacity="0.9"/>
<circle cx="23" cy="13" r="2.5" fill="white" opacity="0.9"/>
<defs>
<linearGradient id="lg1" x1="0" y1="0" x2="32" y2="32">
<stop offset="0%" stop-color="#8b5cf6"/>
<stop offset="100%" stop-color="#06b6d4"/>
</linearGradient>
</defs>
</svg>
<div>
<div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;
font-weight:800;color:#f1f5f9;line-height:1;">DataCleaner</div>
<div style="font-family:'Space Grotesk',sans-serif;font-size:0.65rem;
color:#8b5cf6;font-weight:700;letter-spacing:0.15em;">AI PLATFORM</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # ── Dataset status ────────────────────────────────────────────────
    has_data = "df_cleaned" in st.session_state
    if has_data:
        df_info = st.session_state["df_cleaned"]
        st.markdown(f"""<div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);
border-radius:12px;padding:10px 14px;margin-bottom:1rem;font-size:0.8rem;">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
<span style="width:7px;height:7px;background:#10b981;border-radius:50%;
box-shadow:0 0 6px #10b981;display:inline-block;"></span>
<span style="color:#34d399;font-weight:600;">Dataset Active</span>
</div>
<div style="color:#64748b;">{len(df_info):,} rows x {len(df_info.columns)} cols</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background:rgba(100,116,139,0.1);border:1px solid rgba(100,116,139,0.2);
border-radius:12px;padding:10px 14px;margin-bottom:1rem;font-size:0.8rem;">
<div style="color:#64748b;font-weight:500;">No dataset loaded</div>
</div>""", unsafe_allow_html=True)

    # ── Nav label ─────────────────────────────────────────────────────
    st.markdown("""<div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;
color:#475569;font-weight:600;padding:0 0.5rem;margin-bottom:0.4rem;">
Navigation
</div>""", unsafe_allow_html=True)

    # ── Navigation items ──────────────────────────────────────────────
    nav_items = [
        ("Home",               "Home",          True),
        ("Upload Dataset",     "Upload",         True),
        ("AI Cleaning Engine", "Cleaning",       has_data),
        ("Visualization Lab",  "Visualization",  has_data),
        ("Outlier Detection",  "Outliers",       has_data),
        ("Feature Engineering","Features",       has_data),
        ("AI Insights",        "Insights",       has_data),
        ("Before vs After",    "Comparison",     has_data),
        ("Export & Download",  "Export",         has_data),
    ]

    icons = {
        "Home": "🏠", "Upload": "📁", "Cleaning": "⚡",
        "Visualization": "📊", "Outliers": "🚨", "Features": "🧬",
        "Insights": "🤖", "Comparison": "📈", "Export": "📤",
    }

    for label, page_key, enabled in nav_items:
        icon = icons.get(page_key, "•")
        is_active = st.session_state["current_page"] == page_key
        btn_type = "primary" if is_active else "secondary"

        # Standard Streamlit button, which is 100% reliable
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{page_key}",
            use_container_width=True,
            type=btn_type,
            disabled=not enabled,
        ):
            st.session_state["current_page"] = page_key
            st.rerun()

    # CSS to style the sidebar buttons beautifully (premium glassmorphism theme)
    st.markdown("""<style>
/* Styling the sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
background: transparent !important;
color: #94a3b8 !important;
border: 1px solid rgba(255, 255, 255, 0.04) !important;
border-radius: 10px !important;
padding: 10px 14px !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 0.88rem !important;
font-weight: 500 !important;
text-align: left !important;
display: flex !important;
align-items: center !important;
justify-content: flex-start !important;
width: 100% !important;
height: 42px !important;
margin-top: 0 !important;
box-shadow: none !important;
transition: all 0.2s ease !important;
cursor: pointer !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
background: rgba(255, 255, 255, 0.05) !important;
color: #f1f5f9 !important;
border-color: rgba(139, 92, 246, 0.3) !important;
box-shadow: 0 0 10px rgba(139, 92, 246, 0.15) !important;
}

/* Styled active (primary) button */
[data-testid="stSidebar"] .stButton > button[data-testid^="stBaseButton-primary"] {
background: rgba(139, 92, 246, 0.15) !important;
color: #f1f5f9 !important;
border: 1px solid rgba(139, 92, 246, 0.35) !important;
font-weight: 600 !important;
box-shadow: 0 0 15px rgba(139, 92, 246, 0.2) !important;
}

/* Disabled buttons */
[data-testid="stSidebar"] .stButton > button:disabled {
opacity: 0.38 !important;
cursor: not-allowed !important;
pointer-events: none !important;
border-color: transparent !important;
background: transparent !important;
color: #64748b !important;
}
</style>""", unsafe_allow_html=True)

    st.markdown("---")

    # Footer
    st.markdown("""<div style="padding:0.5rem;text-align:center;">
<div style="font-size:0.72rem;color:#475569;line-height:1.6;">
<div style="margin-bottom:4px;">
<span style="color:#8b5cf6;">&#9679;</span> DataCleaner AI v2.0 Pro
</div>
<div>Built for Data Scientists &amp; ML Engineers</div>
</div>
</div>""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────
render_header(st.session_state["current_page"])

# ── PAGE ROUTER ─────────────────────────────────────────────────────────
page = st.session_state["current_page"]

page_map = {
    "Home":          render_home,
    "Upload":        render_upload_page,
    "Cleaning":      render_cleaning_engine,
    "Visualization": render_visualization_lab,
    "Outliers":      render_outlier_detection,
    "Features":      render_feature_engineering,
    "Insights":      render_ai_insights,
    "Comparison":    render_before_after,
    "Export":        render_export,
}

page_map.get(page, render_home)()
