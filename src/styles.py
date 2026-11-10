# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent executive visual card containers, zero-clipping displays,
and typography across all pages of the Healthcare Analytics Suite.
"""

import streamlit as st

CHART_CARD_CSS = """
<style>
/* Executive Visual Card Architecture: Non-Clipping, Fully Visible Containers */
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

