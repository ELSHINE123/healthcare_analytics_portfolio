# src/styles.py
"""
Shared Styling & Visual Card Architecture Utilities
Ensures consistent executive visual card containers, zero-clipping displays,
compact sticky headers, and typography across all pages of the Healthcare Analytics Suite.
"""

import streamlit as st

CHART_CARD_CSS = """
<style>
/* 1. Global Block Container & Navigable Space Optimization */
.block-container {
  padding-top: 1.2rem !important;
  padding-bottom: 2.2rem !important;
  max-width: 1280px !important;
}

/* 2. Global Heading Scale (Compact & Executive) */
h1 {
  font-size: 20px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  color: #0F172A !important;
  margin-top: 4px !important;
  margin-bottom: 4px !important;
  line-height: 1.25 !important;
}

h2 {
  font-size: 17.5px !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  color: #0F172A !important;
  margin-top: 16px !important;
  margin-bottom: 6px !important;
  line-height: 1.3 !important;
}

h3 {
  font-size: 15px !important;
  font-weight: 600 !important;
  color: #1E293B !important;
  margin-top: 12px !important;
  margin-bottom: 4px !important;
}

/* 3. Compact & Sticky Executive Page Header Architecture */
div[data-testid="stElementContainer"]:has(.sticky-page-header) {
  position: sticky !important;
  top: 2.875rem !important; /* Docks right below Streamlit native topbar */
  z-index: 995 !important;
  margin-top: -6px !important;
  margin-bottom: 12px !important;
}

.sticky-page-header {
  position: sticky !important;
  top: 2.875rem !important;
  z-index: 995 !important;
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border-bottom: 1px solid #E2E8F0 !important;
  padding: 8px 12px 9px 12px !important;
  border-radius: 0 0 10px 10px !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
}

.sticky-page-header-inner {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
}

.sticky-title-row {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
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
  font-size: 10px !important;
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

/* 4. Executive Visual Card Architecture: Non-Clipping, Fully Visible Containers */
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
    Snaps to the top of the viewport when scrolling so executive users always maintain navigation context.
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
