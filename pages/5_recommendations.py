# pages/5_recommendations.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Strategic Recommendations & Executive Implementation Roadmap
Synthesizes Findings from Acts 1-4 and Strategic Questions 1-10
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Data Ingestion for Export Engine
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "healthcare_analytics_enriched.csv"

@st.cache_data
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

df = load_data()

# ==============================================================================
# 1. PAGE HEADER & EXECUTIVE METADATA
# ==============================================================================
st.title("Strategic Recommendations & Executive Implementation Roadmap")
st.caption("Board-Level Governance, Clinical Protocolization & 180-Day Phased Execution Plan")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    The empirical audit of Metropolitan Health System's 983 chronic disease patients across Acts 1 through 4 
    reveals a clear mandate: **unmanaged clinical risk directly erodes the health system's balance sheet under two-sided ACO risk contracts**. 
    With 56.3% of the cohort in High or Severe Acuity, 220 actionable medication gaps, and 145 patients completely uncontactable, 
    maintaining the status quo guarantees acute avoidable hospitalizations and severe CMS Star Rating penalty clawbacks.
    
    This final chapter synthesizes the analytical findings into **Four Core Strategic Pillars** and a concrete, 
    milestone-driven **180-Day Executive Implementation Roadmap** to transition Metropolitan Health from reactive inpatient loss 
    to proactive, self-funding clinical excellence.
    """
)

# ==============================================================================
# 2. EXECUTIVE SCORECARD / STRATEGIC IMPACT STRIP
# ==============================================================================
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Clinical Action</div>
            <div style="font-size: 24px; font-weight: 800; color: #2563EB; line-height: 1.1;">220 Care Gaps</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Immediate GDMT Titration</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Workforce Scale</div>
            <div style="font-size: 24px; font-weight: 800; color: #7C3AED; line-height: 1.1;">7.0 RN FTEs</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Caseload-Calibrated Unit</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Net Economic Return</div>
            <div style="font-size: 24px; font-weight: 800; color: #10B981; line-height: 1.1;">+$392K / yr</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">159% Self-Funded Model</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Quality Benchmark</div>
            <div style="font-size: 24px; font-weight: 800; color: #059669; line-height: 1.1;">4.5 Stars</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">CMS Quality Bonus Target</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. SECTION 1: THE FOUR CORE STRATEGIC PILLARS
# ==============================================================================
st.header("1. The Four Pillars of Population Health Transformation")

st.markdown(
    """
    To achieve sustainable clinical and actuarial outcomes, Metropolitan Health System must deploy 
    coordinated interventions across four interdependent operational domains:
    """
)

# Scoped CSS for full-width equal tab distribution across the screen
st.markdown(
    """
    <style>
    /* Full-width equal distribution across the canvas without overflow */
    div[data-testid="stTabs"] div[role="tablist"] {
        display: flex !important;
        width: 100% !important;
        gap: 6px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding-bottom: 0px !important;
    }
    div[data-testid="stTabs"] div[role="tablist"] button[role="tab"],
    button[data-testid="stBaseButton-tab"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        border-radius: 6px 6px 0 0 !important;
        background-color: transparent !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stTabs"] div[role="tablist"] button[role="tab"]:hover,
    button[data-testid="stBaseButton-tab"]:hover {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
    }
    div[data-testid="stTabs"] div[role="tablist"] button[role="tab"][aria-selected="true"],
    button[data-testid="stBaseButton-tab"][aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
        font-weight: 700 !important;
        background-color: #F8FAFC !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

pillar_tab1, pillar_tab2, pillar_tab3, pillar_tab4 = st.tabs([
    "🩺 1. Clinical Protocols",
    "⚙️ 2. Operational Reach",
    "👥 3. Workforce Pods",
    "💰 4. Value Governance"
])

with pillar_tab1:
    st.subheader("Pillar 1: Guideline-Directed Medical Therapy (GDMT) & Protocolization")
    st.markdown(
        """
        * **Automated EHR Clinical Decision Support (CDS)**: Configure real-time best-practice alerts in the EHR that trigger 
          whenever a diabetic patient (N = 204) or coronary heart disease patient (N = 207) presents without an active statin prescription, 
          directly addressing the severe HEDIS deficits (**19.6%** in diabetes and **26.6%** in cardiac disease).
        * **Nurse-Led Titration Standing Orders**: Empower the care coordination unit under Chief Medical Officer approved protocols 
          to initiate and titrate guideline-concordant therapies (e.g., Atorvastatin 20–80 mg, ACE inhibitors, ARBs) without requiring a separate 
          physician visit for each dosage step.
        * **Eliminate Therapeutic Discordance**: Systematically review the 111 patients on discordant medications to ensure secondary prevention 
          targets (SBP <130 mmHg, LDL-C <70 mg/dL) are aggressively pursued.
        """
    )

with pillar_tab2:
    st.subheader("Pillar 2: Eradicating Operational Blind Spots & Surveillance Lags")
    st.markdown(
        """
        * **Front-Desk Intake Demographic Verification**: Institute mandatory phone and email verification workflows at clinic check-in 
          to systematically eliminate the **145 digital blind spots** (14.8% of panel). Front-line registrars will receive weekly compliance scorecards.
        * **Community Health Worker (CHW) Field Engagement**: Deploy mobile community navigators to perform in-person welfare visits and 
          portal onboarding for the 145 uncontactable patients who cannot be reached via SMS or telephonic outreach.
        * **Automated Surveillance Recall**: Connect the EHR database to an automated recall engine that flags patients exceeding 180 days 
          since their last clinical encounter, triaging the **462 overdue patients** before decompensation triggers emergency room utilization.
        * **Laboratory Data Provenance Assurance**: Partner with commercial lab vendors to replace simulated/unimputed lab values with 
          automated bidirectional HL7/FHIR feeds and point-of-care lipid/A1c testing at all primary care clinics.
        """
    )

with pillar_tab3:
    st.subheader("Pillar 3: High-Risk Workforce Calibration & Pod-Based Staffing")
    st.markdown(
        """
        * **Formalize the 7.0 RN FTE Care Management Unit**: Finance and deploy 7 full-time dedicated Registered Nurse Care Managers 
          calibrated strictly to national **Case Management Society of America (CMSA)** caseload standards.
        * **Acuity-Stratified Panel Distribution**:
          * **3.4 FTEs dedicated to 204 Severe Acuity Patients (1:60 ratio)**: Weekly biometric check-ins, medication reconciliation, and in-person navigation.
          * **3.5 FTEs dedicated to 349 High Acuity Patients (1:100 ratio)**: Bi-weekly surveillance, remote monitoring oversight, and appointment adherence.
        * **Zero Dilution Policy**: Prohibit care managers from carrying Low or Moderate Acuity panels. Preserving the 80/20 Pareto principle 
          concentrates 100% of nurse capacity on the top two tiers that account for **83.2% of the health system's financial liability**.
        """
    )

with pillar_tab4:
    st.subheader("Pillar 4: Value-Based Financial Governance & Risk Optimization")
    st.markdown(
        """
        * **Reinvest Operating Margin into Remote Monitoring (RPM)**: Channel a portion of the projected **&dollar;392.5K annual net operating margin** 
          into cellular-connected blood pressure cuffs and continuous glucose monitors for the 204 Severe Acuity patients.
        * **Real-Time Admission Discharge Transfer (ADT) Feeds**: Integrate regional health information exchange (HIE) feeds to alert nurse 
          care managers within 60 minutes of any panel patient presenting to an acute emergency department, capturing patients before inpatient admission.
        * **Transition to Higher-Reward Two-Sided Risk Contracts**: Leverage demonstrated quality benchmark superiority (HEDIS CBP >76%, 
          remediated statin adherence >60%) to negotiate larger shared-savings percentages (from 50% to 75%) with commercial Medicare Advantage payers.
        """
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. SECTION 2: 180-DAY EXECUTIVE IMPLEMENTATION ROADMAP
# ==============================================================================
st.header("2. 180-Day Phased Executive Implementation Roadmap")

st.markdown(
    """
    To translate strategic recommendations into measurable clinical and financial milestones, 
    the following phased roadmap outlines operational execution over the next two fiscal quarters:
    """
)

# Build Gantt Roadmap Data
roadmap_tasks = [
    {
        "Phase": "Phase 1: Foundation (Days 1–30)",
        "Task": "EHR Clinical Decision Support (CDS) & Gap Alerts",
        "Start": 1,
        "Duration": 30,
        "Owner": "Chief Information Officer / IT",
        "Deliverable": "Hard-stop statin alerts active in EHR",
        "Color": "#3B82F6"
    },
    {
        "Phase": "Phase 1: Foundation (Days 1–30)",
        "Task": "Mandatory Demographic Registration Audit",
        "Start": 5,
        "Duration": 25,
        "Owner": "Chief Operating Officer / Clinic Intake",
        "Deliverable": "100% check-in phone/email verification",
        "Color": "#3B82F6"
    },
    {
        "Phase": "Phase 2: Workforce (Days 31–60)",
        "Task": "Recruit & Onboard 7.0 RN Care Managers",
        "Start": 31,
        "Duration": 30,
        "Owner": "Chief Nursing Officer / HR",
        "Deliverable": "Full clinical care unit hired & trained",
        "Color": "#7C3AED"
    },
    {
        "Phase": "Phase 2: Workforce (Days 31–60)",
        "Task": "Calibrate Panels & Assign High-Risk Pods",
        "Start": 40,
        "Duration": 20,
        "Owner": "VP of Population Health",
        "Deliverable": "553 patients assigned (1:60 / 1:100)",
        "Color": "#7C3AED"
    },
    {
        "Phase": "Phase 3: Surveillance (Days 61–90)",
        "Task": "Deploy Multi-Modal Recall for Overdue Cohort",
        "Start": 61,
        "Duration": 30,
        "Owner": "Care Management Unit & CHWs",
        "Deliverable": "462 overdue patients contacted",
        "Color": "#F59E0B"
    },
    {
        "Phase": "Phase 3: Surveillance (Days 61–90)",
        "Task": "Protocolized Statin Titration Campaign",
        "Start": 65,
        "Duration": 25,
        "Owner": "Chief Medical Officer / Nursing",
        "Deliverable": "50% statin care gap closure reached",
        "Color": "#F59E0B"
    },
    {
        "Phase": "Phase 4: Value (Days 91–180)",
        "Task": "HEDIS Quality Scorecard & Star Rating Audit",
        "Start": 91,
        "Duration": 90,
        "Owner": "Director of Quality & Compliance",
        "Deliverable": "4.5 CMS Star Rating threshold achieved",
        "Color": "#10B981"
    },
    {
        "Phase": "Phase 4: Value (Days 91–180)",
        "Task": "Admission Reduction & Shared Savings Audit",
        "Start": 105,
        "Duration": 75,
        "Owner": "Chief Financial Officer",
        "Deliverable": "20% admission reduction & +$392K net",
        "Color": "#10B981"
    }
]

roadmap_df = pd.DataFrame(roadmap_tasks)

fig_roadmap = go.Figure()

for _, row in roadmap_df.iterrows():
    fig_roadmap.add_trace(go.Bar(
        x=[row["Duration"]],
        y=[row["Task"]],
        base=[row["Start"]],
        orientation="h",
        marker=dict(color=row["Color"]),
        width=0.45,
        text=f"Days {row['Start']}–{row['Start'] + row['Duration']}",
        textposition="inside",
        insidetextanchor="middle",
        insidetextfont=dict(color="#FFFFFF", size=10.5, family="Be Vietnam Pro"),
        hovertemplate=f"<b>{row['Task']}</b><br>Phase: {row['Phase']}<br>Timeline: Days {row['Start']} to {row['Start'] + row['Duration']}<br>Lead Stakeholder: {row['Owner']}<br>Milestone: {row['Deliverable']}<extra></extra>",
        showlegend=False
    ))

fig_roadmap.update_layout(
    title=dict(
        text="<b>Metropolitan Health System: 180-Day Population Health Transformation Gantt</b>",
        x=0.5, y=0.96, xanchor="center", yanchor="top"
    ),
    margin=dict(l=260, r=40, t=55, b=50),
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title="Execution Timeline (Days from Board Approval)",
        range=[0, 185],
        tickvals=[1, 30, 60, 90, 120, 150, 180],
        ticktext=["Day 1", "Day 30", "Day 60", "Day 90", "Day 120", "Day 150", "Day 180"],
        showgrid=True,
        gridcolor="#E2E8F0"
    ),
    yaxis=dict(title="", tickfont=dict(size=11, family="Be Vietnam Pro"), autorange="reversed"),
    font=dict(family="Be Vietnam Pro, sans-serif")
)

st.plotly_chart(fig_roadmap, width="stretch")

st.markdown("---")

# ==============================================================================
# 5. SECTION 3: SENIOR LEADERSHIP GOVERNANCE & DECISION MATRIX
# ==============================================================================
st.header("3. Senior Leadership Governance & Executive Decision Matrix")

st.markdown(
    """
    Immediate organizational commitment is required across the senior executive team to authorize 
    workforce appropriations, clinical protocol revisions, and payer contract adjustments:
    """
)

# Governance Decision Matrix Table (Custom Styled to match 12.5px-13px Editorial Typography)
gov_rows_html = """
<div style="overflow-x: auto; margin-top: 12px; margin-bottom: 24px; border: 1px solid #E2E8F0; border-radius: 8px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);">
  <table style="width: 100%; border-collapse: collapse; font-family: 'Be Vietnam Pro', sans-serif; font-size: 12.5px; line-height: 1.5; color: #1E293B; background-color: #FFFFFF;">
    <thead>
      <tr style="background-color: #F8FAFC; border-bottom: 2px solid #E2E8F0; text-align: left;">
        <th style="padding: 10px 14px; font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; width: 22%;">C-Suite Stakeholder</th>
        <th style="padding: 10px 14px; font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; width: 23%;">Core Mandate</th>
        <th style="padding: 10px 14px; font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; width: 38%;">Action Required</th>
        <th style="padding: 10px 14px; font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; width: 17%;">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #F1F5F9;">
        <td style="padding: 12px 14px; font-weight: 700; color: #0F172A; vertical-align: top;">Chief Executive Officer (CEO)</td>
        <td style="padding: 12px 14px; font-weight: 600; color: #334155; vertical-align: top;">Strategic Alignment & Sponsorship</td>
        <td style="padding: 12px 14px; color: #475569; vertical-align: top;">Charter the Value-Based Transformation Taskforce; sponsor clinical shift from fee-for-service volume to panel health outcomes.</td>
        <td style="padding: 12px 14px; vertical-align: top;"><span style="background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap;">Decision Pending</span></td>
      </tr>
      <tr style="border-bottom: 1px solid #F1F5F9; background-color: #FAFAFA;">
        <td style="padding: 12px 14px; font-weight: 700; color: #0F172A; vertical-align: top;">Chief Medical Officer (CMO)</td>
        <td style="padding: 12px 14px; font-weight: 600; color: #334155; vertical-align: top;">Clinical Protocolization</td>
        <td style="padding: 12px 14px; color: #475569; vertical-align: top;">Authorize nurse-led standing orders for statin initiation and titration; review clinical discordance cases with department chairs.</td>
        <td style="padding: 12px 14px; vertical-align: top;"><span style="background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap;">Protocol Drafted</span></td>
      </tr>
      <tr style="border-bottom: 1px solid #F1F5F9;">
        <td style="padding: 12px 14px; font-weight: 700; color: #0F172A; vertical-align: top;">Chief Financial Officer (CFO)</td>
        <td style="padding: 12px 14px; font-weight: 600; color: #334155; vertical-align: top;">Budget & Risk Negotiation</td>
        <td style="padding: 12px 14px; color: #475569; vertical-align: top;">Approve $665,000 annual staffing appropriation for 7.0 RN FTEs; negotiate two-sided risk corridors and shared savings bonuses with payers.</td>
        <td style="padding: 12px 14px; vertical-align: top;"><span style="background-color: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap;">ROI Verified (159%)</span></td>
      </tr>
      <tr style="border-bottom: 1px solid #F1F5F9; background-color: #FAFAFA;">
        <td style="padding: 12px 14px; font-weight: 700; color: #0F172A; vertical-align: top;">Chief Operating Officer (COO)</td>
        <td style="padding: 12px 14px; font-weight: 600; color: #334155; vertical-align: top;">Intake & Outreach Infrastructure</td>
        <td style="padding: 12px 14px; color: #475569; vertical-align: top;">Implement front-desk demographic audit workflows; deploy community health workers to resolve 145 digital blind spot patients.</td>
        <td style="padding: 12px 14px; vertical-align: top;"><span style="background-color: #F5F3FF; color: #5B21B6; border: 1px solid #DDD6FE; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap;">Workflows Designed</span></td>
      </tr>
      <tr>
        <td style="padding: 12px 14px; font-weight: 700; color: #0F172A; vertical-align: top;">Chief Information Officer (CIO)</td>
        <td style="padding: 12px 14px; font-weight: 600; color: #334155; vertical-align: top;">EHR CDS & Provenance Sync</td>
        <td style="padding: 12px 14px; color: #475569; vertical-align: top;">Activate EHR CDS alerts for statin care gaps; establish automated HIE feeds for regional hospital admission alerts and direct lab integration.</td>
        <td style="padding: 12px 14px; vertical-align: top;"><span style="background-color: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600; display: inline-block; white-space: nowrap;">Scope Approved</span></td>
      </tr>
    </tbody>
  </table>
</div>
"""

st.markdown(gov_rows_html, unsafe_allow_html=True)

st.markdown(
    """
    **Executive Summary Conclusion**: Metropolitan Health System stands at a decisive strategic crossroads. 
    Passive management of its chronic panel carries an unmitigated balance sheet liability exceeding **&dollar;3.83M in gross acute inpatient exposure**. 
    Conversely, investing **&dollar;665K in a 7.0 RN FTE care coordination unit** averts 51 avoidable acute hospitalizations, secures 
    CMS 4.5-Star Quality Bonus incentives, and returns a verified **+&dollar;392.5K in net operating margin (159% self-funding ratio)**. 
    The clinical, operational, and financial evidence conclusively supports immediate board approval of the 180-Day Implementation Plan.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Executive Export Bar
import sys
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

from src.export_engine import generate_board_memorandum, generate_care_gap_roster_csv

memo_text = generate_board_memorandum(df)
csv_text = generate_care_gap_roster_csv(df)

rec_col1, rec_col2 = st.columns(2, gap="medium")

with rec_col1:
    st.download_button(
        "📄 Export Board of Directors Memorandum (.md)",
        data=memo_text,
        file_name="Metropolitan_Health_Board_Memorandum.md",
        mime="text/markdown",
        use_container_width=True,
        help="Export the complete board-certified strategic memorandum."
    )

with rec_col2:
    st.download_button(
        "📊 Export High-Risk Care Gap Registry (.csv)",
        data=csv_text,
        file_name="Metropolitan_Health_Care_Gap_Registry.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the actionable 553 high-risk patient roster for care management."
    )

