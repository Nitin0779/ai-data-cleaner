"""
DataCleaner AI — Home Page
Landing page with hero section and feature overview.
"""

import streamlit as st
from components.metrics_cards import render_quality_score_card


def render_home():
    """Render the home/landing page."""

    # Hero Section
    st.markdown("""<div class="hero-section">
<div class="hero-badge">
<span class="hero-badge-dot"></span>
Powered by Advanced AI Engine
</div>
<h1 class="hero-title">
Clean. Analyze.<br>
<span class="hero-gradient">Transform Data.</span>
</h1>
<p class="hero-subtitle">
The most advanced AI-powered data preprocessing platform.<br>
Built for data scientists, ML engineers, and analysts who demand excellence.
</p>
<div class="hero-cta">
<div class="cta-pill">
<span>🚀</span> Start Cleaning Your Dataset
</div>
<div class="hero-stats">
<div class="hero-stat"><span class="stat-num">99.8%</span><span class="stat-label">Accuracy</span></div>
<div class="hero-divider"></div>
<div class="hero-stat"><span class="stat-num">50ms</span><span class="stat-label">Processing</span></div>
<div class="hero-divider"></div>
<div class="hero-stat"><span class="stat-num">8+</span><span class="stat-label">AI Algorithms</span></div>
</div>
</div>
</div>

<style>
.hero-section {
    text-align: center;
    padding: 3rem 1rem 2rem;
    animation: fadeInUp 0.8s ease forwards;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 999px;
    padding: 8px 20px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #a78bfa;
    margin-bottom: 1.5rem;
    animation: glow 3s ease-in-out infinite;
}
.hero-badge-dot {
    width: 8px; height: 8px;
    background: #8b5cf6;
    border-radius: 50%;
    box-shadow: 0 0 10px #8b5cf6;
    animation: pulse 2s ease infinite;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    color: #f1f5f9 !important;
    margin-bottom: 1.2rem;
}
.hero-gradient {
    background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 600px;
    margin: 0 auto 2rem;
}
.hero-cta { display: flex; flex-direction: column; align-items: center; gap: 1.5rem; }
.cta-pill {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    color: white;
    padding: 14px 32px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 1rem;
    cursor: default;
    box-shadow: 0 8px 40px rgba(139,92,246,0.4);
    animation: float 3s ease-in-out infinite;
    transition: all 0.3s ease;
}
.hero-stats {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 12px 28px;
}
.hero-stat { display: flex; flex-direction: column; align-items: center; }
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label { font-size: 0.72rem; color: #64748b; font-weight: 500; }
.hero-divider { width: 1px; height: 28px; background: rgba(255,255,255,0.08); }
</style>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature Cards
    st.markdown("""<div class="section-header" style="text-align:center; margin-bottom:2rem;">
<h2 style="font-size:2rem; font-weight:700;">Everything You Need to<br>
<span style="background:linear-gradient(135deg,#8b5cf6,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
Prepare Perfect Data</span></h2>
<p style="color:#94a3b8; margin-top:0.5rem;">Eight powerful AI modules working in harmony</p>
</div>""", unsafe_allow_html=True)

    features = [
        ("🧠", "AI Cleaning Engine", "Auto-detect and fix missing values, duplicates, type errors, and constant columns in one click.", "purple"),
        ("📊", "Visualization Lab", "Interactive Plotly charts — heatmaps, 3D scatter, violin plots, PCA, and more.", "cyan"),
        ("🚨", "Outlier Detection", "Z-Score, IQR, and Isolation Forest anomaly detection with live threshold sliders.", "pink"),
        ("🧬", "Feature Engineering", "Label encoding, one-hot encoding, standardization, normalization, and PCA.", "green"),
        ("🤖", "AI Insights", "Dataset quality scoring, feature importance, correlation alerts, and ML type prediction.", "orange"),
        ("📈", "Before vs After", "Animated comparison dashboard showing exactly how much your data improved.", "purple"),
        ("📤", "Export System", "Download cleaned CSV, PDF reports, and visualization exports.", "cyan"),
        ("⚡", "Real-time Preview", "Live data table updates as you apply transformations — no page reloads needed.", "pink"),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc, color) in enumerate(features):
        color_map = {
            "purple": ("rgba(139,92,246,0.1)", "rgba(139,92,246,0.3)", "#a78bfa"),
            "cyan":   ("rgba(6,182,212,0.1)",  "rgba(6,182,212,0.3)",  "#22d3ee"),
            "pink":   ("rgba(236,72,153,0.1)", "rgba(236,72,153,0.3)", "#f472b6"),
            "green":  ("rgba(16,185,129,0.1)", "rgba(16,185,129,0.3)", "#34d399"),
            "orange": ("rgba(245,158,11,0.1)", "rgba(245,158,11,0.3)", "#fbbf24"),
        }
        bg, border, text = color_map.get(color, color_map["purple"])
        with cols[i % 4]:
            st.markdown(f"""<div class="feature-card" style="border-color:{border}; background:{bg};">
<div class="feature-icon">{icon}</div>
<div class="feature-title" style="color:{text};">{title}</div>
<div class="feature-desc">{desc}</div>
</div>
<style>
.feature-card {{
    border: 1px solid;
    border-radius: 18px;
    padding: 1.3rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease {i*0.08}s both;
    cursor: default;
}}
.feature-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}}
.feature-icon {{ font-size: 2rem; margin-bottom: 10px; }}
.feature-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 8px;
}}
.feature-desc {{
    font-size: 0.82rem;
    color: #64748b;
    line-height: 1.5;
}}
</style>""", unsafe_allow_html=True)

    st.markdown("---")

    # Quick start guide
    st.markdown("""<div style="text-align:center; margin: 2rem 0 1rem;">
            Get Started in 3 Steps
        </h3>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    steps = [
        ("01", "Upload Dataset", "Drag & drop your CSV or XLSX file. Supports datasets up to 500MB.", "📁", "purple"),
        ("02", "AI Auto-Clean", "Let the AI engine detect and fix all data quality issues automatically.", "🤖", "cyan"),
        ("03", "Export Results", "Download your clean dataset and comprehensive preprocessing report.", "📤", "pink"),
    ]
    for col, (num, title, desc, icon, color) in zip([c1, c2, c3], steps):
        color_map = {
            "purple": ("rgba(139,92,246,0.1)", "rgba(139,92,246,0.3)", "#a78bfa"),
            "cyan":   ("rgba(6,182,212,0.1)",  "rgba(6,182,212,0.3)",  "#22d3ee"),
            "pink":   ("rgba(236,72,153,0.1)", "rgba(236,72,153,0.3)", "#f472b6"),
        }
        bg, border, text = color_map[color]
        with col:
            st.markdown(f"""<div class="step-card" style="background:{bg}; border-color:{border};">
<div class="step-num" style="color:{text};">{num}</div>
<div class="step-icon">{icon}</div>
<div class="step-title">{title}</div>
<div class="step-desc">{desc}</div>
</div>
<style>
.step-card {{
    border: 1px solid; border-radius: 20px; padding: 1.5rem;
    text-align: center; animation: fadeInUp 0.6s ease;
    transition: all 0.3s ease;
}}
.step-card:hover {{ transform: translateY(-4px); }}
.step-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem; font-weight: 900;
    opacity: 0.4; line-height: 1; margin-bottom: 8px;
}}
.step-icon {{ font-size: 2rem; margin-bottom: 10px; }}
.step-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 700;
    color: #f1f5f9; margin-bottom: 8px;
}}
.step-desc {{ font-size: 0.83rem; color: #64748b; line-height: 1.5; }}
</style>""", unsafe_allow_html=True)

    # Bottom navigation hint
    st.markdown("""<div style="text-align:center; margin-top:2rem; padding:1.5rem;
background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.2);
border-radius:16px; animation: fadeInUp 0.8s ease 0.3s both;">
<p style="color:#94a3b8; font-size:0.9rem; margin:0;">
👈 Use the <strong style="color:#a78bfa;">sidebar navigation</strong> to explore all features.<br>
Start with <strong style="color:#22d3ee;">📁 Upload Dataset</strong> to begin your AI-powered data journey.
</p>
</div>""", unsafe_allow_html=True)
