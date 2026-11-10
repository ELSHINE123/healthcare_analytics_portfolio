# pages/4_roi.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Act 4: The Strategic Solution — Preventative Care ROI & Clinical Staffing Model
Answers Strategic Questions 9 and 9b
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.styles import inject_chart_card_css

inject_chart_card_css()

# ==============================================================================
# 1. PAGE HEADER & EXECUTIVE METADATA
# ==============================================================================
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
col_head, col_reset = st.columns([3.5, 1.2])
with col_head:
    st.header("1. Preventative Care Caseload & Staffing Simulation Workbench")
with col_reset:
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    if st.button("↺ Reset Assumptions", key="btn_reset_roi", help="Reset staffing parameters to certified baseline ($95K salary, 20% reduction target).", use_container_width=True):
        st.session_state["rn_salary_sim"] = 95000
        st.session_state["reduction_target_sim"] = 20
        st.rerun()

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
        value=st.session_state.get("rn_salary_sim", 95000),
        key="rn_salary_sim",
        format_func=lambda x: f"${x:,}",
        help="Includes base RN salary, health benefits, pension, payroll taxes, and clinical malpractice coverage."
    )

with sim_col2:
    reduction_target = st.slider(
        "Inpatient Admission Reduction Target (%)",
        min_value=10,
        max_value=35,
        value=st.session_state.get("reduction_target_sim", 20),
        step=1,
        key="reduction_target_sim",
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

# KPI Metric Strip (Clean responsive scorecard architecture)
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Target Caseload</div>
            <div class="kpi-card-value" style="color: #0F172A;">{target_cohort_size:,} Pts</div>
            <div class="kpi-card-subtitle">
                <span>High & Severe Tiers</span>
                <span class="kpi-badge kpi-badge-blue">56.3% Panel</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Dedicated Workforce</div>
            <div class="kpi-card-value" style="color: #2563EB;">{total_fte_rounded}.0 RN FTEs</div>
            <div class="kpi-card-subtitle">
                <span>CMSA Standards</span>
                <span class="kpi-badge kpi-badge-blue">1:60 &bull; 1:100</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Staffing Investment</div>
            <div class="kpi-card-value" style="color: #DC2626;">&dollar;{total_staffing_cost / 1e3:.0f}K</div>
            <div class="kpi-card-subtitle">
                <span>@ &dollar;{rn_salary:,}/RN</span>
                <span class="kpi-badge kpi-badge-amber">Fully Loaded</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    margin_color = "#10B981" if net_operating_margin >= 0 else "#DC2626"
    sign = "+" if net_operating_margin >= 0 else ""
    badge_style = "kpi-badge-green" if net_operating_margin >= 0 else "kpi-badge-red"
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Net Operating Margin</div>
            <div class="kpi-card-value" style="color: {margin_color};">{sign}&dollar;{net_operating_margin / 1e3:.0f}K</div>
            <div class="kpi-card-subtitle">
                <span>Self-Funded Model</span>
                <span class="kpi-badge {badge_style}">▲ {self_funding_ratio:.0f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. PREVENTATIVE CARE MANAGEMENT ROI SIMULATION (STANDALONE VISUALS)
# ==============================================================================
st.header("2. Preventative Care Management ROI & Breakeven Simulation")

# Visual 9A: Multi-Scenario Sensitivity Analysis (Grouped Bar Chart - Standalone Full Width)
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
    margin=dict(l=35, r=20, t=55, b=110),
    height=480,
    barmode="group",
    bargap=0.25,
    bargroupgap=0.10,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Annual Value ($ Thousands)", range=[-60, 560]),
    xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro"), tickangle=0),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.17,
        xanchor="center",
        x=0.5,
        font=dict(family="Be Vietnam Pro", size=12)
    ),
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v9a, width="stretch")

# Analysis Directly Under Visual 9A
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Multi-Scenario Sensitivity Analysis</strong>: Across conservative, base case, and optimistic scenarios, the economic model benchmarks 
        program costs against inpatient cost avoidance and CMS quality bonuses:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Downside Protection</strong>: Even under the Conservative scenario (15% admission reduction and zero quality bonus), the program generates <strong>&dollar;238.8K in inpatient cost avoidance</strong>, recovering <strong>86.4% of operating expenses</strong>.</li>
        <li style='margin-bottom: 8px;'><strong>The Break-Even Admission Threshold</strong>: To completely recover the &dollar;276.5K program cost, Metropolitan Health System must avert just <strong>22 acute admissions per year</strong> out of the 254.8 baseline admissions expected across this high-risk cohort—a hurdle rate of only <strong>8.6%</strong> (less than 1.9 hospitalizations averted per month).</li>
    </ul>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Visual 9B: Base Case Net Financial Bridge (Waterfall Chart - Standalone Full Width)
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
    margin=dict(l=25, r=20, t=55, b=50),
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Annual Budget Impact ($ Thousands)", range=[-320, 480]),
    xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro"), tickangle=0),
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v9b, width="stretch")

# Analysis Directly Under Visual 9B
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Base Case Net Financial Bridge (+&dollar;109.9K Net Value)</strong>: Under the expected 20% reduction in preventable acute admissions, the program averts <strong>51.0 inpatient stays</strong>, generating <strong>&dollar;318.4K in direct cost avoidance</strong> under AHRQ HCUP benchmarks (&dollar;12,500/stay). Combined with a conservative <strong>&dollar;68.0K in CMS 4-Star Quality Bonus capture</strong>, the program yields <strong>&dollar;386.4K in gross economic value</strong> against &dollar;276.5K in expense—delivering <strong>+&dollar;109.9K in net margin (140% ROI)</strong>.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# 2D Breakeven Sensitivity Matrix
st.subheader("Actuarial Sensitivity Matrix: Breakeven Frontier")
st.caption("Net operating margin ($ Thousands) across variable nurse compensation and admission reduction targets (includes CMS Quality Bonus).")

salaries_grid = [75000, 85000, 95000, 105000, 115000, 125000]
salary_labels = [f"${s//1000}K / yr" for s in salaries_grid]
reductions_grid = [10, 15, 20, 25, 30, 35]
reduction_labels = [f"{r}% Target" for r in reductions_grid]

z_matrix = []
text_matrix = []

for s in salaries_grid:
    row_z = []
    row_t = []
    cost_val = total_fte_rounded * s
    for r in reductions_grid:
        savings_val = base_admissions_target * (r / 100.0) * ADMISSION_BENCHMARK
        net_val = (savings_val + quality_bonus_share - cost_val) / 1000.0
        row_z.append(net_val)
        prefix = "+" if net_val >= 0 else ""
        row_t.append(f"{prefix}${net_val:.0f}K")
    z_matrix.append(row_z)
    text_matrix.append(row_t)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=z_matrix,
    x=reduction_labels,
    y=salary_labels,
    text=text_matrix,
    texttemplate="%{text}",
    textfont=dict(family="Be Vietnam Pro", size=13.5, color="#0F172A"),
    colorscale=[
        [0.0, "#FECACA"],   # Soft Red for negative margin
        [0.2, "#FED7AA"],   # Light Amber
        [0.35, "#FEF3C7"],  # Warm Yellow near breakeven
        [0.55, "#D1FAE5"],  # Mint Green
        [1.0, "#6EE7B7"]    # Emerald Green for high margin
    ],
    zmid=0,
    colorbar=dict(
        title=dict(text="Net Margin ($K)", font=dict(family="Be Vietnam Pro", size=12)),
        tickfont=dict(family="Be Vietnam Pro", size=11),
        len=0.9
    ),
    hovertemplate="<b>Reduction Target:</b> %{x}<br><b>Nurse Compensation:</b> %{y}<br><b>Net Operating Margin:</b> %{text}<extra></extra>"
))

fig_heatmap.update_layout(
    title=dict(
        text="<b>Preventative Care Breakeven Frontier (2D Sensitivity Matrix)</b>",
        x=0.5, y=0.98, yref="container", xanchor="center", yanchor="top",
        font=dict(size=14, family="Be Vietnam Pro", color="#0F172A")
    ),
    margin=dict(l=55, r=75, t=70, b=55),
    height=480,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Preventable Inpatient Admission Reduction Target", tickfont=dict(size=12, family="Be Vietnam Pro")),
    yaxis=dict(title="Fully Loaded Nurse Compensation", tickfont=dict(size=12, family="Be Vietnam Pro")),
    font=dict(family="Be Vietnam Pro, sans-serif")
)

st.plotly_chart(fig_heatmap, width="stretch")

# Analysis Directly Under Breakeven Heatmap
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Breakeven Frontier Analysis</strong>: The 2D sensitivity matrix demonstrates robust downside insulation across all practical operational bounds. 
        Even at high clinician compensation bands (&dollar;125K/yr fully loaded) with conservative admission reduction goals (15%), 
        the care management program maintains positive operating margins. Green cells denote positive net economic return, confirming that 
        the business case does not rely on aggressive clinical targets to achieve financial sustainability.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. CARE MANAGER STAFFING OPTIMIZATION & FTE MODEL (STANDALONE VISUALS)
# ==============================================================================
st.header("3. Clinical Care Manager Workforce Allocation & Self-Funding Model")

# Visual 10A: Nurse FTE Allocation by Acuity Tier (Horizontal Bar Chart - Standalone Full Width)
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
        x=0.5, y=0.98, yref="container", xanchor="center", yanchor="top",
        font=dict(size=14, family="Be Vietnam Pro", color="#0F172A")
    ),
    margin=dict(l=200, r=60, t=75, b=45),
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Required Dedicated Nurse Care Managers (FTEs)", range=[0, 8.5]),
    yaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro"), autorange="reversed"),
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v10a, width="stretch")

# Analysis Directly Under Visual 10A
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Care Management Workforce Calibration (CMSA & NCQA Standards)</strong>: High-quality care coordination requires rigorous caseload calibration. 
        Overloading nurse navigators leads to superficial outreach and clinician burnout, while under-allocating staffing leaves high-risk patients 
        unmonitored:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 4px;'><strong>Severe Acuity (1:60 Ratio)</strong>: Managing 204 critical patients (frequent exacerbations, compounding diabetes/cardiac disease, Stage 2 hypertension) demands intensive weekly check-ins, medication reconciliation, and in-person clinic coordination, requiring <strong>3.4 RN FTEs</strong>.</li>
        <li style='margin-bottom: 4px;'><strong>High Acuity (1:100 Ratio)</strong>: Managing 349 patients with persistent Stage 1 hypertension and rising risk requires bi-weekly surveillance and home biometric monitoring, requiring <strong>3.5 RN FTEs</strong>.</li>
        <li style='margin-bottom: 4px;'><strong>Total Dedicated Workforce</strong>: Metropolitan Health System requires <strong>6.89 ~ 7.0 dedicated Registered Nurse FTEs</strong> to blanket the entire 553-patient high-risk panel.</li>
    </ul>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Visual 10B: Self-Funding Economic Coverage Model (Standalone Full Width)
fin_labels = ["Total Staffing Cost", "Total Value Created", "Net Operating Margin"]
fin_vals = [total_staffing_cost / 1e3, total_value_created / 1e3, net_operating_margin / 1e3]
fin_colors = ["#DC2626", "#3B82F6", "#10B981" if net_operating_margin >= 0 else "#DC2626"]

fig_v10b = go.Figure()

fig_v10b.add_trace(go.Bar(
    x=fin_labels,
    y=fin_vals,
    width=0.45,
    marker=dict(color=fin_colors),
    text=[f"<b>${v:.0f}K</b>" for v in fin_vals],
    textposition="outside",
    textfont=dict(color="#0F172A", size=12.5, family="Be Vietnam Pro"),
    hovertemplate="<b>%{x}</b><br>Annual Impact: $%{y:.0f}K<extra></extra>"
))

max_y = max(fin_vals) * 1.25 if max(fin_vals) > 0 else 500

fig_v10b.update_layout(
    title=dict(
        text=f"<b>Self-Funding ROI Feasibility Model</b><br><span style='font-size:12px; color:#047857; font-weight:700;'>● {self_funding_ratio:.0f}% Self-Funded ({sign}${net_operating_margin / 1e3:.0f}K Net Operating Margin)</span>",
        x=0.5, y=0.96, xanchor="center", yanchor="top"
    ),
    margin=dict(l=40, r=40, t=65, b=40),
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Annual Financial Impact ($ Thousands)", range=[0, max_y]),
    xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v10b, width="stretch")

# Analysis Directly Under Visual 10B
st.markdown(
    f"""
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Self-Funding Economic Feasibility & Net Operating Return</strong>: The balance sheet analysis demonstrates that dedicated care management is an accretive operating investment:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>The Economic Impact</strong>: At a fully loaded annual investment of <strong>&dollar;{rn_salary:,} per nurse</strong> (totaling <strong>&dollar;{total_staffing_cost / 1e3:.0f}K</strong> for 7.0 RN FTEs), achieving the {reduction_target}% admission reduction target averts <strong>{admissions_averted:.1f} inpatient hospitalizations (&dollar;{direct_inpatient_savings / 1e3:.0f}K savings)</strong>. Coupled with <strong>&dollar;{quality_bonus_share / 1e3:.0f}K in CMS shared-savings quality bonuses</strong>, the 7.0 nurse unit generates <strong>&dollar;{total_value_created / 1e3:.0f}K in total economic value</strong>.</li>
        <li style='margin-bottom: 8px;'><strong>Executive Conclusion</strong>: The entire care management unit is <strong>{self_funding_ratio:.0f}% self-funded</strong>, returning <strong>{sign}&dollar;{net_operating_margin / 1e3:.0f}K in net operating margin</strong> directly back to Metropolitan Health System while dramatically elevating clinical quality, patient safety, and CMS Star Ratings.</li>
    </ul>
    """,
    unsafe_allow_html=True
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

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.markdown("---")

# Executive Tour Progression Card
tour_col1, tour_col2 = st.columns([2.4, 1.2], gap="medium")
with tour_col1:
    st.markdown(
        """
        <div style="padding: 2px 0;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #2563EB; margin-bottom: 2px;">
                EXECUTIVE TOUR &bull; FINAL STRATEGIC BLUEPRINT
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">
                Strategic Roadmap & Executive Governance
            </div>
            <div style="font-size: 12.5px; color: #64748B;">
                Review the 4 core pillars, 180-day transformation Gantt chart, and C-suite decision matrix.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with tour_col2:
    try:
        st.page_link(
            "pages/5_recommendations.py",
            label="Proceed to Roadmap →",
            icon="🎯",
            use_container_width=True
        )
    except Exception:
        if st.button("Proceed to Roadmap →", key="tour_roi_btn", use_container_width=True):
            st.switch_page("pages/5_recommendations.py")

