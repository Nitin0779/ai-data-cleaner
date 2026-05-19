"""
DataCleaner AI — Header Component
Renders the top navigation bar with logo and status.
"""

import streamlit as st


def render_header(current_page: str = "Home"):
    """Render the premium animated header."""
    st.markdown("""<div class="app-header">
<div class="header-left">
<div class="logo-container">
<div class="logo-icon">
<svg width="28" height="28" viewBox="0 0 28 28" fill="none">
<rect width="28" height="28" rx="8" fill="url(#logo-gradient)"/>
<path d="M8 14L12 10L16 16L20 12" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="8" cy="14" r="2" fill="white" opacity="0.9"/>
<circle cx="20" cy="12" r="2" fill="white" opacity="0.9"/>
<defs>
<linearGradient id="logo-gradient" x1="0" y1="0" x2="28" y2="28">
<stop offset="0%" stop-color="#8b5cf6"/>
<stop offset="100%" stop-color="#06b6d4"/>
</linearGradient>
</defs>
</svg>
</div>
<div class="logo-text">
<span class="logo-name">DataCleaner</span>
<span class="logo-ai">AI</span>
</div>
</div>
</div>
<div class="header-right">
<div class="status-badge">
<span class="status-dot"></span>
<span>AI Engine Active</span>
</div>
<div class="version-badge">v2.0 Pro</div>
</div>
</div>

<style>
.app-header {
display: flex;
align-items: center;
justify-content: space-between;
padding: 16px 24px;
background: rgba(10, 15, 46, 0.6);
backdrop-filter: blur(24px);
-webkit-backdrop-filter: blur(24px);
border: 1px solid rgba(255,255,255,0.06);
border-radius: 20px;
margin-bottom: 24px;
animation: fadeInUp 0.5s ease forwards;
}

.header-left { display: flex; align-items: center; }
.header-right { display: flex; align-items: center; gap: 12px; }

.logo-container {
display: flex;
align-items: center;
gap: 12px;
}

.logo-icon {
animation: float 3s ease-in-out infinite;
}

.logo-text {
display: flex;
align-items: baseline;
gap: 4px;
}

.logo-name {
font-family: 'Space Grotesk', sans-serif;
font-size: 1.4rem;
font-weight: 700;
color: #f1f5f9;
}

.logo-ai {
font-family: 'Space Grotesk', sans-serif;
font-size: 1.4rem;
font-weight: 800;
background: linear-gradient(135deg, #8b5cf6, #06b6d4);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}

.status-badge {
display: flex;
align-items: center;
gap: 8px;
background: rgba(16, 185, 129, 0.1);
border: 1px solid rgba(16, 185, 129, 0.3);
border-radius: 999px;
padding: 6px 14px;
font-size: 0.8rem;
font-weight: 500;
color: #34d399;
}

.status-dot {
width: 8px;
height: 8px;
background: #10b981;
border-radius: 50%;
box-shadow: 0 0 8px #10b981;
animation: pulse 2s ease infinite;
}

@keyframes pulse {
0%, 100% { transform: scale(1); opacity: 1; }
50%       { transform: scale(1.3); opacity: 0.8; }
}

.version-badge {
background: rgba(139, 92, 246, 0.15);
border: 1px solid rgba(139, 92, 246, 0.3);
border-radius: 999px;
padding: 6px 14px;
font-size: 0.8rem;
font-weight: 600;
color: #a78bfa;
}
</style>
""", unsafe_allow_html=True)
