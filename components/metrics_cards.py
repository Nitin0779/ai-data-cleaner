"""
DataCleaner AI — Metrics Cards Component
Renders animated bento-grid metric cards.
"""

import streamlit as st
from typing import List, Dict, Any


def render_metric_card(title: str, value: Any, subtitle: str = "", 
                        icon: str = "📊", color: str = "purple",
                        delta: str = None):
    """Render a single animated metric card."""
    color_map = {
        "purple": ("rgba(139,92,246,0.15)", "rgba(139,92,246,0.4)", "#a78bfa"),
        "cyan":   ("rgba(6,182,212,0.15)",  "rgba(6,182,212,0.4)",  "#22d3ee"),
        "pink":   ("rgba(236,72,153,0.15)", "rgba(236,72,153,0.4)", "#f472b6"),
        "green":  ("rgba(16,185,129,0.15)", "rgba(16,185,129,0.4)", "#34d399"),
        "orange": ("rgba(245,158,11,0.15)", "rgba(245,158,11,0.4)", "#fbbf24"),
    }
    bg, border, text = color_map.get(color, color_map["purple"])
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""

    st.markdown(f"""<div class="metric-card" style="background:{bg}; border-color:{border};">
<div class="metric-icon">{icon}</div>
<div class="metric-content">
<div class="metric-title">{title}</div>
<div class="metric-value" style="color:{text};">{value}</div>
<div class="metric-subtitle">{subtitle}</div>
{delta_html}
</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def render_quality_score_card(score: int):
    """Render the circular quality score card."""
    if score >= 80:
        color = "#10b981"
        label = "Excellent"
        glow = "rgba(16,185,129,0.4)"
    elif score >= 60:
        color = "#f59e0b"
        label = "Good"
        glow = "rgba(245,158,11,0.4)"
    elif score >= 40:
        color = "#f97316"
        label = "Fair"
        glow = "rgba(249,115,22,0.4)"
    else:
        color = "#ef4444"
        label = "Poor"
        glow = "rgba(239,68,68,0.4)"

    circumference = 2 * 3.14159 * 54
    offset = circumference * (1 - score / 100)

    st.markdown(f"""<div class="quality-card" style="--glow-color:{glow};">
<div class="quality-ring-wrap">
<svg width="140" height="140" viewBox="0 0 140 140">
<circle cx="70" cy="70" r="54" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="12"/>
<circle cx="70" cy="70" r="54" fill="none"
stroke="{color}" stroke-width="12"
stroke-dasharray="{circumference:.1f}"
stroke-dashoffset="{offset:.1f}"
stroke-linecap="round"
transform="rotate(-90 70 70)"
style="filter: drop-shadow(0 0 8px {glow}); transition: stroke-dashoffset 1s ease;"/>
<text x="70" y="65" text-anchor="middle"
font-family="Space Grotesk" font-size="28" font-weight="800" fill="{color}">{score}</text>
<text x="70" y="84" text-anchor="middle"
font-family="Inter" font-size="11" fill="#94a3b8">/ 100</text>
</svg>
</div>
<div class="quality-info">
<div class="quality-label" style="color:{color};">{label}</div>
<div class="quality-desc">Dataset Quality Score</div>
</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)


def render_issue_card(issue: Dict):
    """Render a single data quality issue card."""
    severity_colors = {
        "high": ("#ef4444", "rgba(239,68,68,0.15)", "rgba(239,68,68,0.3)"),
        "medium": ("#f59e0b", "rgba(245,158,11,0.15)", "rgba(245,158,11,0.3)"),
        "low": ("#06b6d4", "rgba(6,182,212,0.15)", "rgba(6,182,212,0.3)"),
    }
    severity_icons = {"high": "🔴", "medium": "🟡", "low": "🔵"}
    sev = issue.get("severity", "low")
    text_color, bg, border = severity_colors.get(sev, severity_colors["low"])
    icon = severity_icons.get(sev, "ℹ️")
    issue_type = issue.get("type", "").replace("_", " ").title()

    st.markdown(f"""<div class="issue-card" style="background:{bg}; border-color:{border};">
<div class="issue-left">
<span class="issue-icon">{icon}</span>
<div>
<div class="issue-type">{issue_type}</div>
<div class="issue-col">Column: <code style="color:{text_color};">{issue.get("column","")}</code></div>
</div>
</div>
<div class="issue-right">
<div class="issue-desc">{issue.get("description","")}</div>
<span class="issue-badge" style="background:{bg}; color:{text_color}; border-color:{border};">{sev.upper()}</span>
</div>
</div>""".replace('\n', ' '), unsafe_allow_html=True)
