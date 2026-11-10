# pages/6_glossary.py
"""
Clinical & Value-Based Care Terminology Lexicon & Knowledge Base
Author: Daniel Ademola Dongo
Master Domain Glossary for Metropolitan Health System Population Health Analytics
Provides accessible definitions, clinical context, and cross-references for all acronyms.
"""

from pathlib import Path
import sys
import streamlit as st
try:
    st.set_page_config(layout="wide")
except Exception:
    pass

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.styles import inject_chart_card_css, render_page_header
from src.glossary_data import GLOSSARY_TERMS, CATEGORIES

# Inject unified styling
inject_chart_card_css()

# Scoped custom styling for glossary cards
st.markdown(
    """
    <style>
    .glossary-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .glossary-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }
    .glossary-term-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        font-weight: 800;
        font-size: 14px;
        padding: 3px 10px;
        border-radius: 6px;
        letter-spacing: -0.01em;
    }
    .glossary-cat-badge {
        display: inline-block;
        background-color: #F8FAFC;
        color: #64748B;
        border: 1px solid #E2E8F0;
        font-weight: 600;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-left: 8px;
    }
    .glossary-full-name {
        font-size: 17px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 8px;
        margin-bottom: 6px;
    }
    .glossary-def {
        font-size: 14px;
        line-height: 1.6;
        color: #334155;
        margin-bottom: 10px;
    }
    .glossary-project-box {
        background-color: #F8FAFC;
        border-left: 3px solid #2563EB;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        font-size: 13px;
        line-height: 1.55;
        color: #1E293B;
    }
    .glossary-tag-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 10px;
        font-size: 11.5px;
        color: #64748B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 1. PAGE HEADER & EXECUTIVE METADATA
# ==============================================================================
render_page_header(
    title="Healthcare & Value-Based Care Terminology Lexicon",
    subtitle="Interactive Reference Guide to Clinical Guidelines, HEDIS Measures, Actuarial Economics & Healthcare Acronyms",
    act_badge="Lexicon"
)

st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: left;'>
        Healthcare analytics operates at the intersection of clinical medicine, actuarial economics, federal quality regulations, 
        and health informatics. Use this searchable knowledge base to look up acronyms, guideline standards, 
        pharmacology mechanisms, and economic models referenced across the <strong>Metropolitan Health System Intelligence Suite</strong>.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 2. INTERACTIVE SEARCH & FILTERING CONTROLS
# ==============================================================================
col_search, col_cat, col_rst = st.columns([1.5, 1.0, 0.5], gap="medium")

with col_search:
    search_query = st.text_input(
        "🔍 Search Term, Acronym, Drug, or Concept",
        value=st.session_state.get("glossary_search", ""),
        key="glossary_search",
        placeholder="e.g., HEDIS, Lisinopril, ACO, HCUP, SBP, Star Ratings, FTE...",
        help="Type any acronym or keyword to filter the dictionary in real time."
    ).strip().lower()

with col_cat:
    cur_cat = st.session_state.get("glossary_category", "All Categories")
    selected_category = st.selectbox(
        "Domain Category Filter",
        options=CATEGORIES,
        index=CATEGORIES.index(cur_cat) if cur_cat in CATEGORIES else 0,
        key="glossary_category",
        help="Filter terms by clinical, economic, or regulatory specialization."
    )

with col_rst:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("↺ Clear", key="btn_clear_glossary", help="Clear search keyword and reset category filter.", use_container_width=True):
        st.session_state["glossary_search"] = ""
        st.session_state["glossary_category"] = "All Categories"
        st.rerun()

# Filter logic
filtered_terms = []
for item in GLOSSARY_TERMS:
    # Category check
    if selected_category != "All Categories" and item["category"] != selected_category:
        continue
    # Search query check
    if search_query:
        term_text = f"{item['term']} {item['full_name']} {item['definition']} {item['project_context']}".lower()
        if search_query not in term_text:
            continue
    filtered_terms.append(item)

# Summary stats metric row
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown(
        f"""
        <div class="kpi-metric-card" style="min-height: 75px; padding: 10px 14px;">
            <div class="kpi-card-title">Matching Terms</div>
            <div class="kpi-card-value" style="font-size: 22px; color: #2563EB;">{len(filtered_terms)} / {len(GLOSSARY_TERMS)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col2:
    st.markdown(
        f"""
        <div class="kpi-metric-card" style="min-height: 75px; padding: 10px 14px;">
            <div class="kpi-card-title">Domain Scope</div>
            <div class="kpi-card-value" style="font-size: 20px; color: #0F172A;">{selected_category}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col3:
    st.markdown(
        """
        <div class="kpi-metric-card" style="min-height: 75px; padding: 10px 14px;">
            <div class="kpi-card-title">Guideline Standards</div>
            <div class="kpi-card-value" style="font-size: 20px; color: #10B981;">NCQA • CMS • AHA</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. GLOSSARY TERM CARD CAROUSEL / GRID
# ==============================================================================
if filtered_terms:
    for item in filtered_terms:
        st.markdown(
            f"""
            <div class="glossary-card">
                <div>
                    <span class="glossary-term-badge">{item['term']}</span>
                    <span class="glossary-cat-badge">{item['category']}</span>
                </div>
                <div class="glossary-full-name">{item['full_name']}</div>
                <div class="glossary-def">{item['definition']}</div>
                <div class="glossary-project-box">
                    <strong>Role in this Project:</strong> {item['project_context']}
                </div>
                <div class="glossary-tag-row">
                    <span>📌 Referenced in: <strong>{item['page_label']}</strong></span>
                    <span style="color: #94A3B8;">Healthcare Intelligence Suite</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info(
        f"No terminology found matching **'{search_query}'** in **{selected_category}**. "
        "Try searching for broader keywords like 'HEDIS', 'ACO', 'Statin', or select 'All Categories'."
    )

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; text-align: center;'>
        <em>Metropolitan Health System Population Health Analytics Suite • Certified by Daniel Ademola Dongo • Standards: NCQA HEDIS, 2017 ACC/AHA, AHRQ HCUP</em>
    </p>
    """,
    unsafe_allow_html=True
)

