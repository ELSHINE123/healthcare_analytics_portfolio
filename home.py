# home.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Homepage: Hospital Narrative Overview & Strategic Business Questions
"""

import sys
from pathlib import Path
import streamlit as st

try:
    st.set_page_config(
        page_title="Metropolitan Health System: Clinical EHR Intelligence",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.styles import inject_chart_card_css, render_page_header

inject_chart_card_css()

# ==============================================================================
# 1. HEADER & INSTITUTIONAL IDENTITY
# ==============================================================================
render_page_header(
    title="Metropolitan Health System: Clinical EHR Intelligence",
    subtitle="Value-Based Healthcare Intelligence & Actuarial Cohort Audit • Executive Decision Support • Lead Architect: Daniel Ademola Dongo"
)

# ==============================================================================
# 2. OVERVIEW OF THE HOSPITAL
# ==============================================================================
st.header("The Institutional Setting: Metropolitan Health System")

st.markdown(
    """
    **Metropolitan Health System** is a regional, integrated healthcare delivery network comprising a 
    flagship tertiary acute care hospital, three community-based ambulatory clinics, and an affiliated 
    physician practice network. Serving an urban and suburban population with significant demographic 
    and socioeconomic diversity, the health system manages an active registry of chronic disease patients 
    across cardiology, endocrinology, pulmonology, and primary care.
    
    For decades, Metropolitan Health operated under the traditional **Fee-for-Service (FFS)** paradigm—a model 
    that rewarded procedural volume, diagnostic utilization, and inpatient bed occupancy. Under this episodic structure, 
    clinical workflows were inherently reactive: clinical interventions occurred predominantly after an acute 
    health crisis, such as a hypertensive emergency, diabetic ketoacidosis, or acute asthma decompensation requiring 
    Emergency Department resuscitation or intensive inpatient admission.
    """
)

st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: left;'>
        In recent years, Metropolitan Health entered two-sided risk-bearing agreements with federal and commercial payers, 
        most notably transitioning into an <strong>Accountable Care Organization (ACO)</strong> and accepting capitated <strong>Medicare Advantage</strong> 
        contracts. Under these value-based arrangements, the health system's economic incentives inverted overnight:
    </p>
    <ul style='margin-top: 8px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Actuarial Risk Transfer</strong>: The health system is no longer reimbursed for avoidable readmissions; instead, it is held financially liable for inpatient utilization benchmarks. Every preventable hospitalization directly erodes shared savings margins and triggers risk-corridor penalties.</li>
        <li style='margin-bottom: 8px;'><strong>Quality Gatekeeping</strong>: Millions of dollars in annual performance payments are tied directly to <strong>NCQA HEDIS quality measures</strong> and <strong>CMS Five-Star Ratings</strong>, specifically metrics tracking blood pressure control, statin adherence, and chronic disease surveillance.</li>
        <li style='margin-bottom: 8px;'><strong>The Operational Reality</strong>: While the hospital's Electronic Health Record (EHR) contains extensive data across vitals, diagnoses, and medications, clinical leadership historically lacked a unified analytics engine capable of translating raw records into proactive, risk-stratified clinical outreach.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

# HIPAA Compliance & Clinical Data Ethics Banner
st.markdown(
    """
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-left: 4px solid #10B981; border-radius: 8px; padding: 14px 18px; margin-top: 14px; margin-bottom: 22px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 16px;">🛡️</span>
            <strong style="color: #0F172A; font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em;">Clinical Data Governance & HIPAA Safe Harbor Compliance Notice</strong>
        </div>
        <p style="color: #334155; font-size: 13px; line-height: 1.6; margin: 0; text-align: left;">
            To ensure patient confidentiality and regulatory integrity, all patient records within this application are derived from a 
            <strong>statistically calibrated synthetic cohort (N = 983)</strong> modeled after national epidemiological benchmarks 
            (NHANES, AHRQ HCUP, and ACC/AHA registries). This dataset strictly complies with 
            <strong>HIPAA Safe Harbor De-Identification standards (45 CFR § 164.514(b)(2))</strong>: direct identifiers 
            (names, telephone numbers, email addresses, and exact visit dates) are stripped and replaced with opaque 
            pseudonymized record IDs (<code>PT-0001</code>&ndash;<code>PT-0983</code>), binary reachability flags, and year-level timestamps. 
            Zero Protected Health Information (PHI) is collected, stored, or transmitted, ensuring complete compliance for public portfolio demonstration and technical evaluation.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 2B. EXECUTIVE REVIEW PATHWAYS
# ==============================================================================
with st.expander("🧭 **Executive Review Pathways**", expanded=False):
    st.caption("Select your leadership focus to view a curated 3-step review path, priority visuals, and actionable decisions:")
    tab_cmo, tab_coo, tab_cfo, tab_analyst = st.tabs([
        "🩺 Clinical Leadership (CMO / Quality)",
        "⚙️ Operations & Reach (COO / Pop Health)",
        "💰 Finance & Risk (CFO / Managed Care)",
        "📋 Care Management & Analytics"
    ])
    
    with tab_cmo:
        st.markdown(
            """
            **Focus**: Clinical Patient Safety, Care Gap Remediation, HEDIS Star Quality
            * **Step 1**: Go to **Clinical Risk & Safety** → Filter the *Bivariate Acuity Matrix* by registry and tier to inspect Stage 2 vitals.
            * **Step 2**: Scroll down to the *Medication Discordance Heatmap* → Review the 41 asthmatics prescribed Lisinopril contraindications.
            * **Step 3**: Go to **Financial Stakes** → Inspect the *HEDIS Statin Therapy Quality Scorecard* compliance gaps.
            * **Action Mandate**: Authorize standardized clinical titration protocols and pharmacy safety recalls.
            """
        )
    with tab_coo:
        st.markdown(
            """
            **Focus**: Operational Outreach Reach, Surveillance Recency, Nurse Caseload Sizing
            * **Step 1**: Go to **Operations & Reach** → Review the 145 digital blind spots (uncontactable) and 180-day surveillance decay matrix.
            * **Step 2**: Go to **ROI & Staffing Model** → Review the calibrated 7.0 RN FTE staffing model (1:60 Severe, 1:100 High Acuity).
            * **Step 3**: Go to **Strategic Roadmap** → Review the 90-day phased operational implementation plan.
            * **Action Mandate**: Re-allocate intake staff for phone/email capture and mobilize the 7.0 RN care management unit.
            """
        )
    with tab_cfo:
        st.markdown(
            """
            **Focus**: Avoidable Inpatient Liability, Downside ACO Risk, ROI & Margin Payback
            * **Step 1**: Go to **Executive Summary** → Review the $3.18M annual gross inpatient exposure.
            * **Step 2**: Go to **Financial Stakes** → Simulate AHRQ HCUP inpatient admission benchmark costs ($10K to $16K).
            * **Step 3**: Go to **ROI Workbench** → Test the 2D Sensitivity Breakeven Frontier (+$392K net margin, 159% self-funding ratio).
            * **Action Mandate**: Approve the $665K care coordination budget backed by certified 4.8-month payback certainty.
            """
        )
    with tab_analyst:
        st.markdown(
            """
            **Focus**: Daily Worklist Triage, Individual EHR Chart Auditing, CSV Roster Exports
            * **Step 1**: Go to **Clinical Risk & Safety** → Filter the interactive patient worklist by Severe Acuity and unmedicated status.
            * **Step 2**: Use the **Sidebar Export Center** → Download the Care Gap Audit Roster (CSV) for clinical queue import.
            * **Step 3**: Go to **Terminology Lexicon** → Look up specific clinical formulas, HEDIS definitions, and national benchmarks.
            * **Action Mandate**: Export daily priority patient rosters for ambulatory nurse follow-up.
            """
        )

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. THE STRATEGIC BUSINESS QUESTIONS
# ==============================================================================
st.header("Executive Decision Framework & Study Objectives")

st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: left;'>
        To navigate this transition and safeguard both patient health and operating margins, 
        executive leadership commissioned an in-depth audit of a <strong>983-patient chronic disease cohort</strong>. 
        This analytics study evaluates core priorities spanning clinical risk, operational feasibility, 
        financial exposure, and care management economics:
    </p>
    """,
    unsafe_allow_html=True
)

st.subheader("1. Clinical Acuity & Pharmacotherapy Care Gaps")
st.markdown(
    """
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Vascular & Metabolic Staging</strong>: When evaluated against standardized medical guidelines (<strong>2017 ACC/AHA High Blood Pressure Guidelines</strong> and <strong>NCEP ATP III Cholesterol Cutoffs</strong>), what proportion of our chronic disease panel is uncontrolled, and how is clinical risk distributed across age groups and disease categories?</li>
        <li style='margin-bottom: 8px;'><strong>Therapeutic Discordance</strong>: How many chronic disease patients are currently unmedicated or receiving pharmacotherapy that fails to address their documented diagnosis (such as diabetic patients without glycemic control or hypertensive patients without anti-hypertensives)?</li>
        <li style='margin-bottom: 8px;'><strong>Polypharmacy & Compounding Acuity</strong>: Which high-acuity patients are exposed to compounding clinical risk due to multi-morbidity and uncoordinated prescribing patterns across disconnected ambulatory care settings?</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.subheader("2. Operational Outreach, Contactability & Data Integrity")
st.markdown(
    """
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Patient Contactability Funnel</strong>: When clinical care coordinators prepare recall and adherence campaigns, what percentage of the vulnerable cohort is genuinely reachable via verified electronic channels (phone, email, or both)?</li>
        <li style='margin-bottom: 8px;'><strong>Operational Blind Spots</strong>: How many patients represent complete operational dead ends—lacking both a working phone number and email address—and how severe is their underlying clinical risk compared to reachable cohorts?</li>
        <li style='margin-bottom: 8px;'><strong>Surveillance Delays & Recall Velocity</strong>: How long has it been since our highest-risk patients last completed an in-person or telehealth consultation, and where are the greatest drop-offs in routine chronic monitoring?</li>
        <li style='margin-bottom: 8px;'><strong>Laboratory Provenance & Vital Sign Integrity</strong>: When missing biometric measurements (blood pressure and cholesterol) rely on estimated values rather than direct laboratory draws, how much clinical misclassification is introduced into population risk tiers?</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.subheader("3. Financial Exposure & Quality Incentive Stakes")
st.markdown(
    """
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Avoidable Inpatient Cost Exposure</strong>: Under national <strong>AHRQ HCUP benchmarks</strong> (&dollar;12,500 average cost per acute chronic admission), what is the hospital's gross financial liability across our uncontrolled patient panel?</li>
        <li style='margin-bottom: 8px;'><strong>High-Cost Outlier Concentration</strong>: Does our inpatient risk follow a Pareto distribution, with a small fraction (e.g., top 10–20%) of multi-morbid patients driving the vast majority of anticipated hospitalizations and financial liability?</li>
        <li style='margin-bottom: 8px;'><strong>HEDIS Star Rating Financial Upside</strong>: What is the quantifiable revenue opportunity of closing blood pressure and statin adherence gaps to achieve 4-star and 5-star performance thresholds under CMS Medicare Advantage incentive contracts?</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.subheader("4. Care Management ROI & Clinical Staffing Feasibility")
st.markdown(
    """
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>The Self-Funding Care Coordination Model</strong>: Can an investment in a dedicated ambulatory nurse care management team (projected at <strong>7.0 Registered Nurse FTEs</strong>) pay for itself strictly through shared-savings revenue generated by averted hospitalizations?</li>
        <li style='margin-bottom: 8px;'><strong>Break-Even & Payback Velocity</strong>: Exactly how many acute inpatient admissions must the nurse care coordination team prevent each year to break even on operational payroll and benefits, and what is the projected net return under conservative, expected, and aggressive clinical scenarios?</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; line-height: 1.6;'>
        <em>This study establishes the evidentiary baseline for Metropolitan Health System's value-based strategy. 
        Each of the deep-dive modules accessible in the navigation sidebar provides the empirical data, 
        interactive visualizations, and statistical models answering these core questions—culminating in the 
        final <strong>Strategic Roadmap</strong> for executive governance.</em>
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.markdown("---")

# Executive Tour Progression Card
tour_col1, tour_col2 = st.columns([2.4, 1.2], gap="medium")
with tour_col1:
    st.markdown(
        """
        <div style="padding: 2px 0;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #2563EB; margin-bottom: 2px;">
                EXECUTIVE TOUR &bull; NEXT STEP
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">
                Executive Summary: Population Health Intelligence
            </div>
            <div style="font-size: 12.5px; color: #64748B;">
                Synthesizes clinical risk, operational blind spots, and self-funding economics.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with tour_col2:
    try:
        st.page_link(
            "pages/0_executive_summary.py",
            label="Begin Executive Tour →",
            icon="📊",
            use_container_width=True
        )
    except Exception:
        if st.button("Begin Executive Tour →", key="tour_home_btn", use_container_width=True):
            st.switch_page("pages/0_executive_summary.py")
