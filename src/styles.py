# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent executive visual card containers, zero-clipping displays,
compact flush top bar page headers, and responsive typography across all pages 
of the Healthcare Analytics Suite on both desktop and mobile devices.
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
  height: 0 !important;
  z-index: 999990 !important;
}

header[data-testid="stHeader"] * {
  pointer-events: auto !important;
}

/* 1. Global Viewport & Container Settings: Zero Top Space & Overflow Protection */
html, body, .stApp, .main, section.main {
  overflow-x: hidden !important;
  max-width: 100vw !important;
}

.main, section.main {
  width: 100% !important;
  max-width: 100% !important;
}

/* 1b. Hide any empty stElementContainer (such as invisible <style> tags) to ensure zero top gap */
div[data-testid="stElementContainer"]:empty,
div[data-testid="stElementContainer"]:has(> div:empty),
div[data-testid="stElementContainer"]:has(style:only-child) {
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* Force full widescreen expansion across all elements when sidebar collapses */
[data-testid="stSidebar"][aria-expanded="false"] ~ .main,
[data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container,
.stApp:has([data-testid="collapsedControl"]) .main,
.stApp:has([data-testid="collapsedControl"]) .main .block-container {
  width: 100% !important;
  max-width: 100% !important;
}

/* 2. Unified Sticky Top Bar Container */
div[data-testid="stElementContainer"]:has(.sticky-page-header) {
  position: sticky !important;
  top: 0 !important;
  z-index: 995 !important;
  margin-top: 0 !important;
  margin-bottom: 20px !important;
  padding-top: 0 !important;
  width: 100% !important;
}

.sticky-page-header {
  position: sticky !important;
  top: 0 !important;
  z-index: 995 !important;
  background: rgba(255, 255, 255, 0.98) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid #CBD5E1 !important;
  border-top: none !important;
  border-left: none !important;
  border-right: none !important;
  border-radius: 0 !important; /* Full bleed edge-to-edge topbar */
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
  box-sizing: border-box !important;
}

.sticky-page-header-inner {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
  width: 100% !important;
  max-width: 1400px !important;
}

.sticky-title-row {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-wrap: wrap !important;
}

/* Clean Left-Aligned Typography for All Narrative Content */
p, li, .stMarkdown p {
  text-align: left !important;
  text-justify: auto !important;
}

/* Compact Subtitle / Caption */
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

/* Streamlined Section Headings */
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

/* Allow Plotly SVG to scale naturally to 100% of its parent */
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

/* ==============================================================================
   DESKTOP SCREEN CALIBRATION (>= 769px)
   ============================================================================== */
@media (min-width: 769px) {
  .main .block-container,
  div.block-container,
  .block-container {
    padding-top: 0rem !important; /* Zero space at top */
    padding-bottom: 2.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    width: 100% !important;
    max-width: 100% !important; /* Spans full length of main page */
    box-sizing: border-box !important;
  }

  .sticky-page-header {
    margin-left: -2.5rem !important;
    margin-right: -2.5rem !important;
    width: calc(100% + 5rem) !important; /* Full-bleed edge-to-edge breakout */
    padding: 10px 140px 11px 2.5rem !important;
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

  .sticky-page-caption {
    font-size: 12px !important;
    color: #64748B !important;
    font-weight: 500 !important;
    line-height: 1.3 !important;
    margin: 0 !important;
  }
}

/* ==============================================================================
   TABLET & MOBILE PHONE CALIBRATION (< 769px)
   ============================================================================== */
@media (max-width: 768px) {
  .main .block-container,
  div.block-container,
  .block-container {
    padding-top: 0rem !important; /* Zero space at top */
    padding-bottom: 2rem !important;
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  div[data-testid="stElementContainer"]:has(.sticky-page-header) {
    margin-bottom: 14px !important;
  }

  .sticky-page-header {
    margin-left: -0.75rem !important;
    margin-right: -0.75rem !important;
    width: calc(100% + 1.5rem) !important; /* Mobile full-bleed breakout */
    padding: 8px 48px 8px 44px !important; /* 44px clears mobile sidebar hamburger; 48px clears top right menu */
  }

  .sticky-page-title {
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    color: #0F172A !important;
    line-height: 1.25 !important;
    margin: 0 !important;
    padding: 0 !important;
    word-break: break-word !important;
  }

  .sticky-page-caption {
    font-size: 11px !important;
    color: #64748B !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    margin: 0 !important;
    word-break: break-word !important;
  }

  /* Responsive Visual Cards & Plotly on Mobile */
  div[data-testid="stPlotlyChart"] {
    padding: 10px 8px !important;
    margin-bottom: 12px !important;
    border-radius: 10px !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }

  /* Responsive Metric Cards on Mobile */
  .kpi-metric-card {
    min-height: auto !important;
    padding: 10px 12px !important;
    margin-bottom: 8px !important;
    width: 100% !important;
  }

  /* Mobile Flex Wrapping for Columns */
  div[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 8px !important;
  }

  /* Touch Scrollable DataFrames & Tables */
  div[data-testid="stDataFrame"],
  .stTable,
  table {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    width: 100% !important;
    display: block !important;
  }
}

/* ==============================================================================
   COMPACT SMARTPHONE CALIBRATION (< 480px)
   ============================================================================== */
@media (max-width: 480px) {
  .main .block-container,
  div.block-container,
  .block-container {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    padding-bottom: 1.5rem !important;
  }

  .sticky-page-header {
    margin-left: -0.5rem !important;
    margin-right: -0.5rem !important;
    width: calc(100% + 1rem) !important;
    padding: 7px 42px 7px 40px !important;
  }

  .sticky-page-title {
    font-size: 13.5px !important;
    line-height: 1.25 !important;
  }

  .sticky-page-caption {
    font-size: 10px !important;
    line-height: 1.3 !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
  }
}
</style>
"""

def inject_chart_card_css():
    """Injects chart card container CSS ensuring all visual content is 100% visible without internal scrolling."""
    st.markdown(CHART_CARD_CSS, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str, *args, **kwargs):
    """
    Renders a space-efficient, sticky executive page header.
    Snaps to the top bar when scrolling so executive users always maintain navigation context.
    """
    header_html = (
        f'<div class="sticky-page-header">'
        f'<div class="sticky-page-header-inner">'
        f'<div class="sticky-title-row">'
        f'<h1 class="sticky-page-title">{title}</h1>'
        f'</div>'
        f'<div class="sticky-page-caption">{subtitle}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
