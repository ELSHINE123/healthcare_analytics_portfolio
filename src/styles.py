# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent executive visual card containers, zero-clipping displays,
compact page headers, and typography across all pages of the Healthcare Analytics Suite.
"""

import streamlit as st

CHART_CARD_CSS = """
<style>
/* 1. Global Block Container & Navigable Space Optimization */
.block-container {
  padding-top: 1.4rem !important;
  padding-bottom: 2.2rem !important;
  max-width: 1280px !important;
}

/* 2. Compact & Elegant Page Title Scale (Recovers ~100px+ of Vertical Space) */
h1, [data-testid="stHeading"] h1 {
  font-size: 22px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  color: #0F172A !important;
  margin-top: 0 !important;
  margin-bottom: 2px !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  line-height: 1.25 !important;
}

/* 3. Compact Subtitle / Caption */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
  font-size: 13px !important;
  color: #64748B !important;
  font-weight: 500 !important;
  margin-top: 0 !important;
  margin-bottom: 12px !important;
  padding-top: 0 !important;
  line-height: 1.35 !important;
}

/* 4. Streamlined Section Headings */
h2, [data-testid="stHeading"] h2 {
  font-size: 17.5px !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  color: #0F172A !important;
  margin-top: 16px !important;
  margin-bottom: 6px !important;
  line-height: 1.3 !important;
}

h3, [data-testid="stHeading"] h3 {
  font-size: 15px !important;
  font-weight: 600 !important;
  color: #1E293B !important;
  margin-top: 12px !important;
  margin-bottom: 4px !important;
}

/* 5. Executive Visual Card Architecture: Non-Clipping, Fully Visible Containers */
div[data-testid="stPlotlyChart"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
  box-sizing: border-box !important;
  margin-top: 8px !important;
  margin-bottom: 18px !important;
  overflow: visible !important;
  overflow-x: visible !important;
  overflow-y: visible !important;
  width: 100% !important;
  max-width: 100% !important;
}

div[data-testid="stPlotlyChart"]:hover {
  border-color: #CBD5E1 !important;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07) !important;
}

/* Allow Plotly SVG to scale naturally to 100% of its parent without forced minimum width */
div[data-testid="stPlotlyChart"] > div {
  border-radius: 10px !important;
  width: 100% !important;
  max-width: 100% !important;
  overflow: visible !important;
}

div[data-testid="stPlotlyChart"] .js-plotly-plot,
div[data-testid="stPlotlyChart"] .plot-container,
div[data-testid="stPlotlyChart"] .user-select-none.svg-container {
  overflow: visible !important;
  width: 100% !important;
}
</style>
"""

def inject_chart_card_css():
    """Injects chart card container CSS ensuring all visual content is 100% visible without internal scrolling."""
    st.markdown(CHART_CARD_CSS, unsafe_allow_html=True)
