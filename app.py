# app.py
"""
Clinical EHR Analytics & Value-Based Healthcare Intelligence
Author: Daniel Ademola Dongo
Master Application Entrypoint (Defined Steel-Slate Rail with Definite Contrast & White Canvas)
"""

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.export_engine import generate_board_memorandum_pdf, generate_care_gap_roster_csv
from src.glossary_data import GLOSSARY_TERMS

st.set_page_config(
    page_title="Healthcare Intelligence Suite",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# DEFINED CONTRAST LIGHT RAIL + ELEVATION SHADOW + CRISP WHITE CANVAS
# ==============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* 1. Global Typography & Refined Scale */
html, body, .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, label {
  font-family: "Be Vietnam Pro", -apple-system, BlinkMacSystemFont, sans-serif !important;
}

h1 {
  font-size: 26px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  line-height: 1.25 !important;
  color: #0F172A !important;
  margin-bottom: 4px !important;
}

h2 {
  font-size: 20px !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  line-height: 1.3 !important;
  color: #0F172A !important;
  margin-top: 20px !important;
  margin-bottom: 8px !important;
}

h3 {
  font-size: 16px !important;
  font-weight: 600 !important;
  line-height: 1.35 !important;
  color: #1E293B !important;
  margin-top: 14px !important;
  margin-bottom: 6px !important;
}

h4 {
  font-size: 14px !important;
  font-weight: 600 !important;
  color: #334155 !important;
  margin-top: 10px !important;
  margin-bottom: 4px !important;
}

p, li {
  font-size: 14.5px !important;
  line-height: 1.65 !important;
  color: #334155 !important;
  text-align: justify !important;
  text-justify: inter-word !important;
}

/* Inspector Side-Panel Text (Refined, Compact Scale) */
.inspector-text, .inspector-text p, .inspector-text div {
  font-size: 13px !important;
  line-height: 1.6 !important;
  color: #334155 !important;
  text-align: justify !important;
  text-justify: inter-word !important;
}

/* 2. Protect Icon Fonts */
[data-testid*="Icon"],
[class*="material-symbols"],
[class*="material-icons"],
button[data-testid="stSidebarCollapseButton"] span,
button[data-testid="stSidebarCollapseButton"] i,
div[data-testid="collapsedControl"] span {
  font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
}

/* 3. Main Canvas (Micro-Dot Tech Grid) */
.stApp {
  background-color: #F8FAFC !important;
  background-image: radial-gradient(#CBD5E1 1.1px, transparent 1.1px) !important;
  background-size: 24px 24px !important;
  color: #0F172A !important;
}

/* 3b. Frosted Glass Top Header for Smooth Scroll Transition */
header[data-testid="stHeader"] {
  background: rgba(248, 250, 252, 0.8) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7) !important;
}

/* 4. Distinct Steel-Slate Sidebar (Noticeably Defined, Not Heavy or Dark) */
section[data-testid="stSidebar"]:not([aria-expanded="false"]) {
  width: 268px !important;
  min-width: 268px !important;
}

section[data-testid="stSidebar"] {
  background-color: #E2E8F0 !important; /* Defined Cool Slate */
  border-right: 1px solid #CBD5E1 !important; /* Firm boundary line */
  box-shadow: 6px 0 24px -2px rgba(15, 23, 42, 0.09) !important; /* Prominent elevation shadow */
  padding-top: 10px !important;
}

/* Ensure smooth, visible scrollbar on the sidebar at all times */
section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] > div {
  scrollbar-width: thin !important;
  scrollbar-color: #94A3B8 #E2E8F0 !important;
  overflow-y: auto !important;
}

section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"]::-webkit-scrollbar,
section[data-testid="stSidebar"] > div::-webkit-scrollbar {
  width: 6px !important;
}

section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"]::-webkit-scrollbar-track,
section[data-testid="stSidebar"] > div::-webkit-scrollbar-track {
  background: #E2E8F0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"]::-webkit-scrollbar-thumb,
section[data-testid="stSidebar"] > div::-webkit-scrollbar-thumb {
  background-color: #94A3B8 !important;
  border-radius: 4px !important;
}

section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"]::-webkit-scrollbar-thumb:hover,
section[data-testid="stSidebar"] > div::-webkit-scrollbar-thumb:hover {
  background-color: #64748B !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
  color: #0F172A !important;
}

/* 5. Minimalist Category Label */
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"]::before {
  content: "ANALYTICS SUITE";
  display: block;
  font-family: "Be Vietnam Pro", sans-serif;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .09em;
  color: #475569;
  padding: 6px 10px 4px 10px;
}

/* 6. Navigation Link Rows (Proportioned for 268px Rail) */
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li div a {
  min-height: 31px !important;
  padding: 0 8px !important;
  border-radius: 6px !important;
  margin: 1px 3px !important;
  display: flex !important;
  align-items: center !important;
  gap: 7px !important;
  color: #334155 !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  white-space: nowrap !important;
  border: 1px solid transparent !important;
  transition: background-color 0.15s ease, color 0.15s ease !important;
}

/* Stationary Hover */
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li div a:hover {
  background-color: #CBD5E1 !important;
  color: #0F172A !important;
}

/* Active Page State: Floating White Card on Slate */
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li div a[aria-current="page"] {
  background-color: #FFFFFF !important; /* Crisp White Floating Pill */
  color: #1D4ED8 !important;            /* Royal Blue Text */
  font-weight: 700 !important;
  border-left: 3px solid #2563EB !important;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
}

/* Sidebar Custom Action Buttons */
section[data-testid="stSidebar"] div.stDownloadButton button {
  background-color: #FFFFFF !important;
  color: #1E293B !important;
  border: 1px solid #CBD5E1 !important;
  border-radius: 7px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  padding: 5px 8px !important;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
  transition: all 0.15s ease !important;
}
section[data-testid="stSidebar"] div.stDownloadButton button:hover {
  background-color: #EFF6FF !important;
  border-color: #93C5FD !important;
  color: #1D4ED8 !important;
  box-shadow: 0 2px 5px rgba(37, 99, 235, 0.12) !important;
}

/* 7. Refined Sidebar Collapse Button */
button[data-testid="stSidebarCollapseButton"] {
  background-color: transparent !important;
  color: #475569 !important;
  border-radius: 6px !important;
}
button[data-testid="stSidebarCollapseButton"]:hover {
  background-color: #CBD5E1 !important;
  color: #0F172A !important;
}

/* 8. Crisp Cards on Canvas */
[data-testid="stVerticalBlockBorderWrapper"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 12px !important;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04) !important;
}

.block-container {
  padding-top: 1.8rem !important;
  padding-bottom: 2.5rem !important;
  max-width: 1250px !important;
}

/* 9. Executive KPI Scorecard Architecture */
.kpi-metric-card {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 10px !important;
  padding: 14px 16px !important;
  min-height: 102px !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
  transition: all 0.2s ease !important;
}

.kpi-card-title {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #64748B !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  line-height: 1.2 !important;
}

.kpi-card-value {
  font-size: 26px !important;
  font-weight: 800 !important;
  line-height: 1.15 !important;
  letter-spacing: -0.02em !important;
}

.kpi-card-subtitle {
  font-size: 11.5px !important;
  color: #64748B !important;
  white-space: normal !important;
  overflow: visible !important;
  line-height: 1.35 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 4px !important;
  flex-wrap: wrap !important;
}

/* 10. Contextual Trend Pills & Benchmark Micro-Badges */
.kpi-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 3px !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  padding: 1.5px 6px !important;
  border-radius: 4px !important;
  letter-spacing: 0.02em !important;
  white-space: nowrap !important;
  line-height: 1.2 !important;
  flex-shrink: 0 !important;
}
.kpi-badge-green {
  background-color: #ECFDF5 !important;
  color: #065F46 !important;
  border: 1px solid #A7F3D0 !important;
}
.kpi-badge-blue {
  background-color: #EFF6FF !important;
  color: #1E40AF !important;
  border: 1px solid #BFDBFE !important;
}
.kpi-badge-amber {
  background-color: #FEF3C7 !important;
  color: #92400E !important;
  border: 1px solid #FDE68A !important;
}
.kpi-badge-red {
  background-color: #FEF2F2 !important;
  color: #991B1B !important;
  border: 1px solid #FECACA !important;
}

/* 11. Narrative Tour Progression Card */
.nav-progression-card {
  background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%) !important;
  border: 1px solid #CBD5E1 !important;
  border-radius: 12px !important;
  padding: 16px 20px !important;
  margin-top: 24px !important;
  margin-bottom: 12px !important;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
}
.nav-progression-title {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  color: #2563EB !important;
  margin-bottom: 3px !important;
}
.nav-progression-desc {
  font-size: 14px !important;
  font-weight: 600 !important;
  color: #0F172A !important;
}

/* 12. Global Responsive Tab Navigation */
div[data-testid="stTabs"] div[role="tablist"] {
  overflow-x: auto !important;
  flex-wrap: nowrap !important;
  scrollbar-width: thin !important;
  -webkit-overflow-scrolling: touch !important;
  gap: 4px !important;
}
div[data-testid="stTabs"] div[role="tablist"] button[role="tab"],
button[data-testid="stBaseButton-tab"] {
  white-space: nowrap !important;
  flex-shrink: 0 !important;
  line-height: 1.3 !important;
}

/* 13. Executive Visual Card Architecture (Standalone Dashboards & Scrollable Containers) */
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

/* 14. Mobile & Tablet Responsiveness */
@media (max-width: 768px) {
  /* Dynamic Mobile Sidebar Drawer */
  section[data-testid="stSidebar"]:not([aria-expanded="false"]) {
    width: 85vw !important;
    max-width: 300px !important;
  }
  
  /* Compact Canvas Padding */
  .block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
  }

  /* Responsive Headings */
  h1 { font-size: 22px !important; line-height: 1.25 !important; }
  h2 { font-size: 18px !important; line-height: 1.3 !important; }
  h3 { font-size: 15px !important; line-height: 1.35 !important; }
  p, li { font-size: 13.5px !important; }

  /* Stacked Full-Width KPI Cards */
  .kpi-metric-card {
    min-height: auto !important;
    padding: 12px 14px !important;
    margin-bottom: 8px !important;
  }
  .kpi-card-value {
    font-size: 24px !important;
  }
  .kpi-card-subtitle {
    font-size: 11px !important;
  }

  /* Tour Progression Card Responsive Layout */
  .nav-progression-card {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 12px !important;
    padding: 14px 16px !important;
  }

  /* Data Table & Decision Matrix Touch Scroll */
  div[data-testid="stDataFrame"],
  .decision-matrix-container {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    width: 100% !important;
  }
}

@media (max-width: 480px) {
  .kpi-card-value {
    font-size: 22px !important;
  }
  .kpi-metric-card {
    padding: 10px 12px !important;
  }
  div[data-testid="stTabs"] div[role="tablist"] button[role="tab"],
  button[data-testid="stBaseButton-tab"] {
    font-size: 12px !important;
    padding: 6px 10px !important;
  }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# BOARDROOM PRESENTATION MODE & EXECUTIVE ACTION CENTER
# ==============================================================================
DATA_PATH = Path(__file__).resolve().parent / "data" / "processed" / "healthcare_analytics_enriched.csv"

@st.cache_data
def get_export_data():
    if DATA_PATH.exists():
        df_exp = pd.read_csv(DATA_PATH)
        pdf_bytes = generate_board_memorandum_pdf(df_exp)
        csv_text = generate_care_gap_roster_csv(df_exp)
        return pdf_bytes, csv_text
    return b"", ""

pdf_data, csv_data = get_export_data()

with st.sidebar:
    st.markdown(
        """
        <div style="font-family: 'Be Vietnam Pro', sans-serif; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .09em; color: #475569; padding: 10px 0 6px 0; border-top: 1px solid #CBD5E1; margin-top: 6px;">
            ⚡ EXECUTIVE COMMAND & EXPORTS
        </div>
        """,
        unsafe_allow_html=True
    )
    pres_mode = st.toggle(
        "💼 Boardroom Mode",
        key="presentation_mode",
        help="Expands canvas width, scales typography, and increases contrast for boardroom displays."
    )
    
    if pdf_data and csv_data:
        st.download_button(
            "📄 Board Memorandum (PDF)",
            data=pdf_data,
            file_name="Metropolitan_Health_Board_Memorandum.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download the certified executive memorandum formatted for boardroom presentation."
        )
        st.download_button(
            "📊 Care Gap Audit Roster (CSV)",
            data=csv_data,
            file_name="Metropolitan_Health_Care_Gap_Registry.csv",
            mime="text/csv",
            use_container_width=True,
            help="Export the 553 high/severe acuity patient roster with care gaps."
        )

    if st.button(
        "↺ Reset All Models to Baseline",
        key="btn_global_reset",
        use_container_width=True,
        help="Reset all interactive financial, staffing, clinical, and search filters across the entire suite to baseline defaults."
    ):
        st.session_state["rn_salary_sim"] = 95000
        st.session_state["reduction_target_sim"] = 20
        st.session_state["fin_service"] = "All Disease Registries"
        st.session_state["fin_admission_cost"] = 12500
        st.session_state["fin_remediation_rate"] = 0
        st.session_state["fin_star_target"] = 4.0
        st.session_state["clin_condition"] = "All Conditions"
        st.session_state["clin_tier"] = "All Acuity Tiers"
        st.session_state["triage_reg"] = "All Registries"
        st.session_state["triage_acuity"] = "All Acuity Tiers"
        st.session_state["triage_gap"] = "All Patients"
        st.session_state["triage_search"] = ""
        st.session_state["glossary_search"] = ""
        st.session_state["glossary_category"] = "All Categories"
        st.toast("✅ All interactive models and filters reset to baseline assumptions!")
        st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    with st.expander("📖 Terminology Lookup", expanded=False):
        st.caption("Look up any healthcare acronym or economic term:")
        term_options = [f"{t['term']} — {t['full_name']}" for t in GLOSSARY_TERMS]
        sel_idx = st.selectbox(
            "Select Term or Acronym:",
            options=range(len(term_options)),
            format_func=lambda i: term_options[i],
            label_visibility="collapsed"
        )
        selected_item = GLOSSARY_TERMS[sel_idx]
        st.markdown(
            f"""
            <div style="font-size: 11.5px; line-height: 1.45; color: #1E293B; margin-top: 2px;">
                <div style="font-weight: 700; color: #1D4ED8;">{selected_item['term']}</div>
                <div style="font-weight: 600; color: #0F172A; font-size: 12px; margin-bottom: 3px;">{selected_item['full_name']}</div>
                <div style="margin-bottom: 5px; color: #334155; font-size: 11px;">{selected_item['definition']}</div>
                <div style="background: #F1F5F9; padding: 5px 7px; border-radius: 4px; border-left: 2px solid #2563EB; font-size: 10.5px; color: #0F172A;">
                    <strong>Project Role:</strong> {selected_item['project_context']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Lead Data Analyst Professional Badge
    st.markdown(
        """
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #CBD5E1;">
            <div style="font-family: 'Be Vietnam Pro', sans-serif; font-size: 9.5px; font-weight: 800; text-transform: uppercase; letter-spacing: .09em; color: #475569; margin-bottom: 6px;">
                PROJECT LEAD & ARCHITECT
            </div>
            <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px; box-shadow: 0 1px 3px rgba(15,23,42,0.05);">
                <div style="font-size: 13px; font-weight: 700; color: #0F172A;">Daniel Ademola Dongo</div>
                <div style="font-size: 10.5px; color: #2563EB; font-weight: 600; margin-bottom: 2px;">Healthcare Data Analyst & BI Developer</div>
                <div style="font-size: 10.5px; color: #475569; line-height: 1.4; margin-bottom: 8px;">
                    Population Health Analytics &bull; Actuarial Cost Modeling
                </div>
                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                    <a href="https://linkedin.com" target="_blank" style="text-decoration: none; font-size: 10.5px; font-weight: 600; color: #1D4ED8; background: #EFF6FF; border: 1px solid #BFDBFE; padding: 2px 7px; border-radius: 4px;">
                        💼 LinkedIn
                    </a>
                    <a href="https://github.com" target="_blank" style="text-decoration: none; font-size: 10.5px; font-weight: 600; color: #334155; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 7px; border-radius: 4px;">
                        💻 GitHub
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.get("presentation_mode", False):
    st.markdown("""
    <style>
    .block-container {
      max-width: 95% !important;
      padding-top: 1.2rem !important;
    }
    h1 {
      font-size: 29px !important;
    }
    h2 {
      font-size: 22px !important;
    }
    p, li {
      font-size: 15px !important;
      line-height: 1.7 !important;
    }
    /* Boardroom Calibrated KPI Metric Cards */
    .kpi-metric-card {
      border: 1.5px solid #CBD5E1 !important;
      border-radius: 12px !important;
      padding: 16px 20px !important;
      min-height: 116px !important;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
    }
    .kpi-card-title {
      font-size: 12.5px !important;
      letter-spacing: 0.06em !important;
      color: #475569 !important;
    }
    .kpi-card-value {
      font-size: 32px !important;
      line-height: 1.1 !important;
    }
    .kpi-card-subtitle {
      font-size: 13.5px !important;
      color: #475569 !important;
    }
    /* Boardroom Calibrated Standalone Visual Cards */
    div[data-testid="stPlotlyChart"] {
      border: 1.5px solid #CBD5E1 !important;
      border-radius: 14px !important;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
      padding: 20px 24px 16px 24px !important;
      margin-bottom: 22px !important;
    }
    /* Boardroom Table Typography */
    table th {
      font-size: 12px !important;
      padding: 12px 16px !important;
    }
    table td {
      font-size: 13.5px !important;
      padding: 14px 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%); color: #FFFFFF; padding: 8px 18px; border-radius: 8px; font-size: 12.5px; font-weight: 700; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);">
            <span>💼 BOARDROOM PRESENTATION MODE &bull; METROPOLITAN HEALTH SYSTEM ACO</span>
            <span style="background: rgba(255,255,255,0.22); padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 700;">WIDESCREEN ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# MASTER NAVIGATION ROUTING (Punchy Titles that fit the slim rail)
# ==============================================================================
pg = st.navigation([
    st.Page("home.py", title="Hospital Overview", icon="🏛️"),
    st.Page("pages/0_executive_summary.py", title="Executive Summary", icon="📊"),
    st.Page("pages/1_clinical.py", title="Clinical Risk & Safety", icon="🩺"),
    st.Page("pages/2_operations.py", title="Operations & Reach", icon="⚙️"),
    st.Page("pages/3_financial.py", title="Financial Stakes", icon="💰"),
    st.Page("pages/4_roi.py", title="ROI & Staffing Model", icon="📈"),
    st.Page("pages/5_recommendations.py", title="Strategic Roadmap", icon="🎯"),
    st.Page("pages/6_glossary.py", title="Terminology Lexicon", icon="📖"),
])

pg.run()
