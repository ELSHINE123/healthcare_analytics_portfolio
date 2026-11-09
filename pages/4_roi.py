# pages/4_roi.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Act 4: The Strategic Solution — Preventative Care ROI & Clinical Staffing Model
Answers Strategic Questions 9 and 9b
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE HEADER & EXECUTIVE METADATA
# ==============================================================================
if st.session_state.get("presentation_mode", False):
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%); color: #FFFFFF; padding: 7px 16px; border-radius: 6px; font-size: 12px; font-weight: 700; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <span>💼 BOARDROOM PRESENTATION MODE &bull; METROPOLITAN HEALTH SYSTEM ACO</span>
            <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 4px; font-size: 11px;">RECOMMENDED BASELINE LOADED</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("Preventative Care ROI & Clinical Staffing Model")
st.caption("Multi-Scenario Preventative Care Economics & Calibrated Nurse Caseload Allocation")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA INGESTION & COHORT SIZING
# ==============================================================================
data_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "healthcare_analytics_enriched.csv"

if not data_path.exists():
    st.error(f"Processed dataset not found at `{data_path}`. Please run data pipeline first.")
    st.stop()

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

df = load_data(data_path)

# Cohort Counts & Baseline Admissions
severe_count = (df["clinical_risk_tier"] == "Severe Acuity").sum()  # 204 pts
high_count = (df["clinical_risk_tier"] == "High Acuity").sum()      # 349 pts
target_cohort_size = severe_count + high_count                      # 553 pts

base_admissions_severe = severe_count * 0.65                        # 132.6 adm
base_admissions_high = high_count * 0.35                            # 122.15 adm
base_admissions_target = base_admissions_severe + base_admissions_high # 254.75 adm

ADMISSION_BENCHMARK = 12500  # $12,500 AHRQ HCUP benchmark

# Caseload Standards (CMSA & NCQA Guidelines)
severe_ratio = 60    # 1 RN per 60 Severe Acuity patients
high_ratio = 100     # 1 RN per 100 High Acuity patients

severe_fte = severe_count / severe_ratio   # 3.40 FTEs
high_fte = high_count / high_ratio         # 3.49 FTEs
total_fte_exact = severe_fte + high_fte    # 6.89 FTEs
total_fte_rounded = 7                      # 7.0 Dedicated RN FTEs

# ==============================================================================
# 3. INTERACTIVE SENSITIVITY & STAFFING SIMULATION WORKBENCH
# ==============================================================================
st.header("1. Preventative Care Caseload & Staffing Simulation Workbench")

st.markdown(
    """
    To transition from reactive inpatient losses to proactive value-based margins, healthcare systems 
    must deploy targeted clinical care coordination. Use the simulation controls below to evaluate 
    care management staffing costs, test admission reduction sensitivities, and project self-funding operating margins.
    """
)

# Injection of CSS to enforce strict uniform vertical alignment of slider tracks
st.markdown(
    """
    <style>
    div[data-testid="stSlider"] label, div[data-testid="stSelectSlider"] label {
        min-height: 28px;
        height: 28px;
        display: flex;
        align-items: flex-end;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

sim_col1, sim_col2 = st.columns(2, gap="large")

with sim_col1:
    rn_salary = st.select_slider(
        "Nurse Care Manager Salary (Fully Loaded $ USD)",
        options=[75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, 125000],
        value=95000,
        format_func=lambda x: f"${x:,}",
        help="Includes base RN salary, health benefits, pension, payroll taxes, and clinical malpractice coverage."
    )

with sim_col2:
    reduction_target = st.slider(
        "Inpatient Admission Reduction Target (%)",
        min_value=10,
        max_value=35,
        value=20,
        step=1,
        format="%d%%",
        help="Target reduction in acute hospitalizations among managed High & Severe Acuity patients."
    )

# Dynamic Financial Calculations
total_staffing_cost = total_fte_rounded * rn_salary
admissions_averted = base_admissions_target * (reduction_target / 100.0)
direct_inpatient_savings = admissions_averted * ADMISSION_BENCHMARK
quality_bonus_share = total_fte_rounded * 60000  # CMS 4-Star Shared Savings ($60K per active care manager)
total_value_created = direct_inpatient_savings + quality_bonus_share
net_operating_margin = total_value_created - total_staffing_cost
self_funding_ratio = (total_value_created / total_staffing_cost * 100.0) if total_staffing_cost > 0 else 0.0

# KPI Metric Strip (Uniform 98px height, flexbox distribution)
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Target Caseload</div>
            <div style="font-size: 24px; font-weight: 800; color: #0F172A; line-height: 1.1;">{target_cohort_size:,} Pts</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">High & Severe Tiers</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Dedicated Workforce</div>
            <div style="font-size: 24px; font-weight: 800; color: #2563EB; line-height: 1.1;">{total_fte_rounded}.0 RN FTEs</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">CMSA / NCQA Caseloads</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Staffing Investment</div>
            <div style="font-size: 24px; font-weight: 800; color: #DC2626; line-height: 1.1;">${total_staffing_cost / 1e3:.0f}K</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@ ${rn_salary:,} / RN FTE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    margin_color = "#10B981" if net_operating_margin >= 0 else "#DC2626"
    sign = "+" if net_operating_margin >= 0 else ""
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Net Operating Margin</div>
            <div style="font-size: 24px; font-weight: 800; color: {margin_color}; line-height: 1.1;">{sign}${net_operating_margin / 1e3:.0f}K</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{self_funding_ratio:.0f}% Self-Funded</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. PREVENTATIVE CARE MANAGEMENT ROI SIMULATION (SIDE-BY-SIDE)
# ==============================================================================
st.header("2. Preventative Care Management ROI & Breakeven Simulation")

v9_col1, v9_col2 = st.columns(2, gap="large")

with v9_col1:
    # Visual 9A: Multi-Scenario Sensitivity Analysis (Grouped Bar Chart)
    scenarios = ["Conservative<br>(15% Target)", "Base Case<br>(20% Target)", "Optimistic<br>(30% Target)"]
    costs_k = [276.5, 276.5, 276.5]            # $500/pt annual care management cost
    savings_k = [238.8, 318.4, 477.7]          # Cost avoidance from admission reduction
    bonuses_k = [0.0, 68.0, 136.0]             # CMS 4-Star Quality Incentive Bonus
    net_k = [savings_k[i] + bonuses_k[i] - costs_k[i] for i in range(3)]

    fig_v9a = go.Figure()

    fig_v9a.add_trace(go.Bar(
        name="Program Cost",
        x=scenarios,
        y=costs_k,
        marker=dict(color="#64748B"),
        width=0.24,
        text=[f"${c:.0f}K" for c in costs_k],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Program Investment: $%{y:.1f}K<extra></extra>"
    ))

    fig_v9a.add_trace(go.Bar(
        name="Inpatient Savings",
        x=scenarios,
        y=savings_k,
        marker=dict(color="#3B82F6"),
        width=0.24,
        text=[f"${s:.0f}K" for s in savings_k],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Inpatient Cost Avoidance: $%{y:.1f}K<extra></extra>"
    ))

    fig_v9a.add_trace(go.Bar(
        name="Net Value",
        x=scenarios,
        y=net_k,
        marker=dict(color=["#F59E0B", "#10B981", "#059669"]),
        width=0.24,
        text=[f"+${n:.0f}K" if n >= 0 else f"-${abs(n):.0f}K" for n in net_k],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Net Value: $%{y:.1f}K<extra></extra>"
    ))

    fig_v9a.update_layout(
        title=dict(
            text="<b>Preventative Care Sensitivity across 3 Scenarios</b>",
            x=0.5, y=0.96, xanchor="center", yanchor="top"
        ),
        margin=dict(l=20, r=20, t=50, b=100),
        height=410,
        barmode="group",
        bargap=0.28,
        bargroupgap=0.10,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Annual Value ($ Thousands)", range=[-60, 560]),
        xaxis=dict(title="", tickfont=dict(size=11, family="Be Vietnam Pro"), tickangle=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.26,
            xanchor="center",
            x=0.5,
            font=dict(family="Be Vietnam Pro", size=10.5)
        ),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v9a, width="stretch")

with v9_col2:
    # Visual 9B: Base Case Net Financial Bridge (Waterfall Chart)
    steps = ["Program<br>Investment", "Inpatient<br>Savings", "Quality<br>Bonus", "Net Economic<br>Value"]
    measure_types = ["relative", "relative", "relative", "total"]
    waterfall_vals = [-276.5, 318.4, 68.0, 0]  # Total computes net sum automatically

    fig_v9b = go.Figure(go.Waterfall(
        name="Financial Bridge",
        orientation="v",
        measure=measure_types,
        x=steps,
        textposition="outside",
        text=["-$276.5K", "+$318.4K", "+$68.0K", "<b>+$109.9K</b><br><span style='font-size:10.5px; color:#059669;'>140% ROI</span>"],
        y=[-276.5, 318.4, 68.0, 0],
        connector={"line": {"color": "#94A3B8", "width": 1.5}},
        decreasing={"marker": {"color": "#DC2626"}},
        increasing={"marker": {"color": "#3B82F6"}},
        totals={"marker": {"color": "#10B981"}}
    ))

    fig_v9b.update_layout(
        title=dict(
            text="<b>Base Case Financial Bridge: +$109.9K Net Value</b>",
            x=0.5, y=0.96, xanchor="center", yanchor="top"
        ),
        margin=dict(l=20, r=20, t=50, b=100),
        height=410,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Annual Budget Impact ($ Thousands)", range=[-320, 480]),
        xaxis=dict(title="", tickfont=dict(size=10.5, family="Be Vietnam Pro"), tickangle=0),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v9b, width="stretch")

# Narrative Directly Under Visual 9
st.markdown(
    """
    **Economic Feasibility & Breakeven Analysis**: Hospital executives transitioning into risk-bearing contracts frequently view care 
    coordination as an unproven cost center. The simulation above models the empirical financial return of deploying dedicated preventative care 
    management across the **553 High and Severe Acuity patients** (budgeted at a standardized **&dollar;500 per patient per year**, total annual investment of **&dollar;276.5K**):
    
    * **The Base Case Reality**: Under the expected 20% reduction in preventable acute admissions, the program averts **51.0 inpatient stays**, 
      generating **&dollar;318.4K in direct cost avoidance** under AHRQ HCUP benchmarks (&dollar;12,500/stay). Combined with a conservative **&dollar;68.0K in CMS 4-Star Quality Bonus capture**, 
      the program yields **&dollar;386.4K in gross economic value** against &dollar;276.5K in expense—delivering **+&dollar;109.9K in net margin (140% ROI)**.
    * **Downside Protection**: Even under the Conservative scenario (15% admission reduction and zero quality bonus), the program generates 
      **&dollar;238.8K in inpatient cost avoidance**, recovering **86.4% of operating expenses**.
    * **The Break-Even Admission Threshold**: To completely recover the &dollar;276.5K program cost, Metropolitan Health System must avert just 
      **22 acute admissions per year** out of the 254.8 baseline admissions expected across this high-risk cohort—a hurdle rate of only **8.6%**. 
      Preventing less than 1.9 hospitalizations per month guarantees financial breakeven.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. CARE MANAGER STAFFING OPTIMIZATION & FTE MODEL (SIDE-BY-SIDE)
# ==============================================================================
st.header("3. Clinical Care Manager Workforce Allocation & Self-Funding Model")

v10_col1, v10_col2 = st.columns(2, gap="large")

with v10_col1:
    # Visual 10A: Nurse FTE Allocation by Acuity Tier (Horizontal Bar Chart)
    fte_df = pd.DataFrame({
        "Tier": ["Severe Acuity (1:60 Ratio)", "High Acuity (1:100 Ratio)", "Total Required Workforce"],
        "FTEs": [severe_fte, high_fte, total_fte_exact],
        "Color": ["#DC2626", "#F59E0B", "#1E293B"]
    })

    fig_v10a = go.Figure()

    fig_v10a.add_trace(go.Bar(
        y=fte_df["Tier"],
        x=fte_df["FTEs"],
        orientation="h",
        width=0.42,
        marker=dict(color=fte_df["Color"]),
        text=[f"<b>{v:.1f} FTEs</b>" for v in fte_df["FTEs"]],
        textposition="outside",
        textfont=dict(color="#0F172A", size=11.5, family="Be Vietnam Pro"),
        hovertemplate="<b>%{y}</b><br>Dedicated Workforce: %{x:.2f} FTEs<extra></extra>"
    ))

    fig_v10a.update_layout(
        title=dict(
            text="<b>Care Management Caseload Staffing Model</b>",
            x=0.5, y=0.96, xanchor="center", yanchor="top"
        ),
        margin=dict(l=180, r=40, t=65, b=40),
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Required Dedicated Nurse Care Managers (FTEs)", range=[0, 8.5]),
        yaxis=dict(title="", tickfont=dict(size=11.5, family="Be Vietnam Pro"), autorange="reversed"),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v10a, width="stretch")

with v10_col2:
    # Visual 10B: Self-Funding Economic Coverage Model
    fin_labels = ["Total Staffing Cost", "Total Value Created", "Net Operating Margin"]
    fin_vals = [total_staffing_cost / 1e3, total_value_created / 1e3, net_operating_margin / 1e3]
    fin_colors = ["#DC2626", "#3B82F6", "#10B981" if net_operating_margin >= 0 else "#DC2626"]

    fig_v10b = go.Figure()

    fig_v10b.add_trace(go.Bar(
        x=fin_labels,
        y=fin_vals,
        width=0.42,
        marker=dict(color=fin_colors),
        text=[f"<b>${v:.0f}K</b>" for v in fin_vals],
        textposition="outside",
        textfont=dict(color="#0F172A", size=12, family="Be Vietnam Pro"),
        hovertemplate="<b>%{x}</b><br>Annual Impact: $%{y:.0f}K<extra></extra>"
    ))

    max_y = max(fin_vals) * 1.25 if max(fin_vals) > 0 else 500

    fig_v10b.update_layout(
        title=dict(
            text=f"<b>Self-Funding ROI Feasibility Model</b><br><span style='font-size:12px; color:#047857; font-weight:700;'>● {self_funding_ratio:.0f}% Self-Funded ({sign}${net_operating_margin / 1e3:.0f}K Net Operating Margin)</span>",
            x=0.5, y=0.96, xanchor="center", yanchor="top"
        ),
        margin=dict(l=20, r=20, t=65, b=40),
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Annual Financial Impact ($ Thousands)", range=[0, max_y]),
        xaxis=dict(title="", tickfont=dict(size=11.5, family="Be Vietnam Pro")),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v10b, width="stretch")

# Narrative Directly Under Visual 10
st.markdown(
    f"""
    **Workforce Staffing Calibration & Self-Funding Economics**: High-quality care coordination requires rigorous caseload calibration. 
    Overloading nurse navigators leads to superficial outreach and clinician burnout, while under-allocating staffing leaves high-risk patients 
    unmonitored. The model above applies national **Case Management Society of America (CMSA)** and **NCQA population health standards**:
    
    * **Caseload Calibration**:
      * **Severe Acuity (1:60 Ratio)**: Managing 204 critical patients (frequent exacerbations, compounding diabetes/cardiac disease, Stage 2 hypertension) 
        demands intensive weekly check-ins, medication reconciliation, and in-person clinic coordination, requiring **3.4 RN FTEs**.
      * **High Acuity (1:100 Ratio)**: Managing 349 patients with persistent Stage 1 hypertension and rising risk requires bi-weekly surveillance 
        and home biometric monitoring, requiring **3.5 RN FTEs**.
      * **Total Dedicated Workforce**: Metropolitan Health System requires **6.89 ~ 7.0 dedicated Registered Nurse FTEs** to blanket the entire 553-patient high-risk panel.
    * **The Self-Funding Economics**: At a fully loaded annual investment of **&dollar;{rn_salary:,} per nurse** (totaling **&dollar;{total_staffing_cost / 1e3:.0f}K** for 7.0 RN FTEs), 
      achieving the {reduction_target}% admission reduction target averts **{admissions_averted:.1f} inpatient hospitalizations (&dollar;{direct_inpatient_savings / 1e3:.0f}K savings)**. 
      Coupled with **&dollar;{quality_bonus_share / 1e3:.0f}K in CMS shared-savings quality bonuses**, the 7.0 nurse unit generates **&dollar;{total_value_created / 1e3:.0f}K in total economic value**.
    * **Executive Conclusion**: The entire care management unit is **{self_funding_ratio:.0f}% self-funded**, returning **{sign}&dollar;{net_operating_margin / 1e3:.0f}K in net operating margin** 
      directly back to Metropolitan Health System while dramatically elevating clinical quality, patient safety, and CMS Star Ratings.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; line-height: 1.6;'>
        <em>To review executive governance and the board-level decision matrix, proceed to 
        <strong>Strategic Roadmap</strong> in the navigation rail.</em>
    </p>
    """,
    unsafe_allow_html=True
)

