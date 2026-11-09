# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent scrollable visual card containers, custom scrollbars,
and typography across all pages of the Healthcare Analytics Suite.
"""

import streamlit as st

CHART_CARD_CSS = """
<style>
/* Executive Visual Card Architecture (Scrollable Containers) */
div[data-testid="stPlotlyChart"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 12px !important;
  padding: 16px 20px 16px 20px !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
  box-sizing: border-box !important;
  margin-top: 8px !important;
  margin-bottom: 18px !important;
  overflow-x: auto !important;
  overflow-y: auto !important;
  max-width: 100% !important;
  scrollbar-width: thin !important;
  scrollbar-color: #CBD5E1 #F1F5F9 !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Custom Webkit scrollbar for visual containers */
div[data-testid="stPlotlyChart"]::-webkit-scrollbar {
  width: 7px !important;
  height: 7px !important;
}
div[data-testid="stPlotlyChart"]::-webkit-scrollbar-track {
  background: #F1F5F9 !important;
  border-radius: 6px !important;
}
div[data-testid="stPlotlyChart"]::-webkit-scrollbar-thumb {
  background: #CBD5E1 !important;
  border-radius: 6px !important;
}
div[data-testid="stPlotlyChart"]::-webkit-scrollbar-thumb:hover {
  background: #94A3B8 !important;
}

div[data-testid="stPlotlyChart"]:hover {
  border-color: #CBD5E1 !important;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07) !important;
}

/* Ensure inner Plotly container preserves min-width so chart elements never get squashed */
div[data-testid="stPlotlyChart"] > div {
  border-radius: 10px !important;
  min-width: 620px !important;
  width: 100% !important;
  overflow: visible !important;
}

div[data-testid="stPlotlyChart"] .js-plotly-plot,
div[data-testid="stPlotlyChart"] .plot-container,
div[data-testid="stPlotlyChart"] .user-select-none.svg-container {
  overflow: visible !important;
}
</style>
"""

def inject_chart_card_css():
    """Injects chart card container CSS with horizontal and vertical scroll support."""
    st.markdown(CHART_CARD_CSS, unsafe_allow_html=True)
