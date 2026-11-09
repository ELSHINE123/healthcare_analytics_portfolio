# home.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Homepage: Hospital Narrative Overview & Strategic Business Questions
"""

import streamlit as st

# ==============================================================================
# 1. HEADER & INSTITUTIONAL IDENTITY
# ==============================================================================
st.title("Metropolitan Health System: Clinical EHR Intelligence")
st.caption("Value-Based Healthcare Intelligence & Actuarial Cohort Audit • Executive Decision Support • Lead Architect: Daniel Ademola Dongo")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

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
    ### The Value-Based Paradigm Shift
    In recent years, Metropolitan Health entered two-sided risk-bearing agreements with federal and commercial payers, 
    most notably transitioning into an **Accountable Care Organization (ACO)** and accepting capitated **Medicare Advantage** 
    contracts. 
    
    Under these value-based arrangements, the health system's economic incentives inverted overnight:
    
    * **Actuarial Risk Transfer**: The health system is no longer reimbursed for avoidable readmissions; instead, it is 
      held financially liable for inpatient utilization benchmarks. Every preventable hospitalization directly erodes shared 
      savings margins and triggers risk-corridor penalties.
    * **Quality Gatekeeping**: Millions of dollars in annual performance payments are tied directly to **NCQA HEDIS quality measures** 
      and **CMS Five-Star Ratings**, specifically metrics tracking blood pressure control, statin adherence, and chronic disease surveillance.
    * **The Data Reality**: While the hospital's Electronic Health Record (EHR) contains millions of data points across vitals, 
      diagnoses, and medications, clinical leadership historically lacked a unified analytics engine capable of translating raw 
      EHR data into proactive, risk-stratified clinical outreach.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. THE STRATEGIC BUSINESS QUESTIONS
# ==============================================================================
st.header("Executive Decision Framework & Study Objectives")

st.markdown(
    """
    To navigate this transition and safeguard both patient health and operating margins, 
    executive leadership commissioned an in-depth audit of a **983-patient chronic disease cohort**. 
    This analytics study was formulated to evaluate core priorities spanning clinical risk, 
    operational feasibility, financial exposure, and care management economics:
    """
)

st.subheader("1. Clinical Acuity & Pharmacotherapy Care Gaps")
st.markdown(
    """
    * **Vascular & Metabolic Staging**: When evaluated against standardized medical guidelines (**2017 ACC/AHA High Blood Pressure 
      Guidelines** and **NCEP ATP III Cholesterol Cutoffs**), what proportion of our chronic disease panel is uncontrolled, 
      and how is clinical risk distributed across age groups and disease categories?
    * **Therapeutic Discordance**: How many chronic disease patients are currently unmedicated or receiving pharmacotherapy that 
      fails to address their documented diagnosis (such as diabetic patients without glycemic control or hypertensive patients without anti-hypertensives)?
    * **Polypharmacy & Compounding Acuity**: Which high-acuity patients are exposed to compounding clinical risk due to multi-morbidity 
      and uncoordinated prescribing patterns across disconnected ambulatory care settings?
    """
)

st.subheader("2. Operational Outreach, Contactability & Data Integrity")
st.markdown(
    """
    * **Patient Contactability Funnel**: When clinical care coordinators prepare recall and adherence campaigns, what percentage 
      of the vulnerable cohort is genuinely reachable via verified electronic channels (phone, email, or both)?
    * **Operational Blind Spots**: How many patients represent complete operational dead ends—lacking both a working phone number 
      and email address—and how severe is their underlying clinical risk compared to reachable cohorts?
    * **Surveillance Delays & Recall Velocity**: How long has it been since our highest-risk patients last completed an in-person or 
      telehealth consultation, and where are the greatest drop-offs in routine chronic monitoring?
    * **EHR Imputation Exposure**: When missing vitals (blood pressure and cholesterol) are imputed using statistical medians, how much 
      clinical distortion and diagnostic misclassification is introduced into population risk tiers?
    """
)

st.subheader("3. Financial Exposure & Quality Incentive Stakes")
st.markdown(
    """
    * **Avoidable Inpatient Cost Exposure**: Under national **AHRQ HCUP benchmarks** (&dollar;12,500 average cost per acute chronic admission), 
      what is the hospital's gross financial liability across our uncontrolled patient panel?
    * **High-Cost Outlier Concentration**: Does our inpatient risk follow a Pareto distribution, with a small fraction (e.g., top 10–20%) 
      of multi-morbid patients driving the vast majority of anticipated hospitalizations and financial liability?
    * **HEDIS Star Rating Financial Upside**: What is the quantifiable revenue opportunity of closing blood pressure and statin adherence 
      gaps to achieve 4-star and 5-star performance thresholds under CMS Medicare Advantage incentive contracts?
    """
)

st.subheader("4. Care Management ROI & Clinical Staffing Feasibility")
st.markdown(
    """
    * **The Self-Funding Care Coordination Model**: Can an investment in a dedicated ambulatory nurse care management team 
      (projected at **7.0 Registered Nurse FTEs**) pay for itself strictly through shared-savings revenue generated by averted hospitalizations?
    * **Break-Even & Payback Velocity**: Exactly how many acute inpatient admissions must the nurse care coordination team prevent each year 
      to break even on operational payroll and benefits, and what is the projected net return under conservative, expected, and aggressive clinical scenarios?
    """
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
