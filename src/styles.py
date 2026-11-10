# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent executive visual card containers, zero-clipping displays,
compact page headers, and typography across all pages of the Healthcare Analytics Suite.
"""

import streamlit as st

CHART_CARD_CSS = """
<style>
/* 0. Dissolve Native Streamlit Topbar into Transparent Layer (One Single Top Bar) */
header[data-testid="stHeader"] {
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-bottom: none !important;
  box-shadow: none !important;
  pointer-events: none !important;
  z-index: 999990 !important;
}

header[data-testid="stHeader"] * {
  pointer-events: auto !important;
}

/* 1. Global Block Container: Starts Flush at Viewport Top */
.block-container {
  padding-top: 0rem !important; /* Docks title header right into the top bar */
  padding-bottom: 2.5rem !important;
  max-width: 1280px !important;
}

/* 2. Unified Sticky Top Bar Architecture (One Single Bar at Top of Viewport) */
div[data-testid="stElementContainer"]:has(.sticky-page-header) {
  position: sticky !important;
  top: 0 !important;
  z-index: 995 !important;
  margin-top: 0 !important;
  margin-bottom: 20px !important;
}

.sticky-page-header {
  position: sticky !important;
  top: 0 !important;
  z-index: 995 !important;
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid #CBD5E1 !important;
  border-left: 1px solid #E2E8F0 !important;
  border-right: 1px solid #E2E8F0 !important;
  border-top: none !important;
  border-radius: 0 0 10px 10px !important;
  padding: 8px 140px 9px 18px !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
}

.sticky-page-header-inner {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
}

.sticky-title-row {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-wrap: wrap !important;
}

.sticky-page-title {
  font-size: 19px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  color: #0F172A !important;
  line-height: 1.25 !important;
  margin: 0 !important;
  padding: 0 !important;
}

.sticky-act-pill {
  background-color: #EFF6FF !important;
  color: #1D4ED8 !important;
  border: 1px solid #BFDBFE !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  padding: 2px 8px !important;
  border-radius: 9999px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  display: inline-block !important;
}

.sticky-page-caption {
  font-size: 12px !important;
  color: #64748B !important;
  font-weight: 500 !important;
  line-height: 1.3 !important;
  margin: 0 !important;
}

/* 2b. Clean Left-Aligned Typography for All Narrative Content */
p, li, .stMarkdown p {
  text-align: left !important;
  text-justify: auto !important;
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

def render_page_header(title: str, subtitle: str, act_badge: str = None):
    """
    Renders a space-efficient, sticky executive page header.
    Snaps to the screen below the top bar when scrolling so executive users always maintain navigation context.
    """
    badge_html = f'<span class="sticky-act-pill">{act_badge}</span>' if act_badge else ""
    header_html = (
        f'<div class="sticky-page-header">'
        f'<div class="sticky-page-header-inner">'
        f'<div class="sticky-title-row">'
        f'{badge_html}'
        f'<h1 class="sticky-page-title">{title}</h1>'
        f'</div>'
        f'<div class="sticky-page-caption">{subtitle}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
