# pages/3_financial.py
"""
Clinical EHR Analytics: Value-Based Care & Financial ROI
Author: Daniel Ademola Dongo
Act 3: The Financial Stakes — Inpatient Exposure & Benchmark Penalties
Answers Strategic Questions 7 and 10
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
st.title("Financial Liability & Quality Benchmark Penalties")
st.caption("Actuarial Acute Inpatient Exposure Modeling & National HEDIS Quality Scorecard Audit")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA INGESTION
# ==============================================================================
data_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "healthcare_analytics_enriched.csv"

if not data_path.exists():
    st.error(f"Processed dataset not found at `{data_path}`. Please run data pipeline first.")
    st.stop()

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

df = load_data(data_path)

acuity_order = ["Low Acuity", "Moderate Acuity", "High Acuity", "Severe Acuity"]
acuity_colors = {
    "Low Acuity": "#10B981",       # Emerald Green
    "Moderate Acuity": "#3B82F6",  # Blue
    "High Acuity": "#F59E0B",      # Amber
    "Severe Acuity": "#DC2626"     # Crimson Red
}

ADMISSION_PROBABILITIES = {
    "Low Acuity": 0.05,
    "Moderate Acuity": 0.15,
    "High Acuity": 0.35,
    "Severe Acuity": 0.65
}

# ==============================================================================
# 3. INTERACTIVE SIMULATION WORKBENCH (ACTUARIAL SENSITIVITY CONTROLS)
# ==============================================================================
st.header("1. Inpatient Liability Modeling & Actuarial Sensitivity Workbench")

st.markdown(
    """
    Under two-sided risk Accountable Care Organization (ACO) contracts and Medicare Advantage capitation, 
    every preventable inpatient admission erodes operating margin dollar-for-dollar. Use the simulation controls 
    below to model financial exposure across clinical service lines and test sensitivity against regional cost benchmarks.
    """
)

# Injection of CSS to enforce strict uniform vertical alignment of control labels
st.markdown(
    """
    <style>
    div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label, div[data-testid="stSelectSlider"] label {
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

# Simulation Controls Row
ctrl_col1, ctrl_col2 = st.columns(2, gap="large")

with ctrl_col1:
    service_options = ["All Disease Registries", "Heart Disease", "Diabetes", "Hypertension", "Asthma"]
    selected_service = st.selectbox(
        "Clinical Service Line Filter",
        options=service_options,
        index=0,
        help="Filter cohort to evaluate disease-specific inpatient financial exposure."
    )

with ctrl_col2:
    admission_cost = st.select_slider(
        "AHRQ HCUP Benchmark Cost per Inpatient Stay ($ USD)",
        options=[8000, 9000, 10000, 11000, 12000, 12500, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000],
        value=12500,
        format_func=lambda x: f"${x:,}",
        help="National Healthcare Cost and Utilization Project (HCUP) average cost for an acute chronic disease admission."
    )

# Slice DataFrame based on selected service line
if selected_service == "All Disease Registries":
    filtered_df = df.copy()
else:
    filtered_df = df[df["condition"].astype(str).str.strip().str.lower() == selected_service.lower()].copy()

# Recalculate Actuarial Inpatient Projections
tier_counts = filtered_df["clinical_risk_tier"].value_counts().reindex(acuity_order, fill_value=0)

cost_data = []
for tier in acuity_order:
    count = int(tier_counts[tier])
    prob = ADMISSION_PROBABILITIES[tier]
    exp_adm = count * prob
    tot_cost = exp_adm * admission_cost
    cost_data.append({
        "clinical_risk_tier": tier,
        "patient_count": count,
        "admission_prob": prob,
        "expected_admissions": exp_adm,
        "cost_exposure": tot_cost,
        "cost_millions": tot_cost / 1_000_000
    })

cost_df = pd.DataFrame(cost_data)

total_patients = len(filtered_df)
total_projected_admissions = cost_df["expected_admissions"].sum()
total_financial_exposure = cost_df["cost_exposure"].sum()

high_severe_cost = cost_df[cost_df["clinical_risk_tier"].isin(["High Acuity", "Severe Acuity"])]["cost_exposure"].sum()
low_mod_cost = cost_df[cost_df["clinical_risk_tier"].isin(["Low Acuity", "Moderate Acuity"])]["cost_exposure"].sum()
pareto_share = (high_severe_cost / total_financial_exposure * 100) if total_financial_exposure > 0 else 0.0

# KPI Metric Strip (Clean minimal styling, no box-farms)
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Audited Cohort</div>
            <div style="font-size: 24px; font-weight: 800; color: #0F172A; line-height: 1.1;">{total_patients:,}</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{selected_service}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Projected Admissions</div>
            <div style="font-size: 24px; font-weight: 800; color: #2563EB; line-height: 1.1;">{total_projected_admissions:.1f}</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Annual Inpatient Events</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Financial Liability</div>
            <div style="font-size: 24px; font-weight: 800; color: #DC2626; line-height: 1.1;">${total_financial_exposure / 1e6:.2f}M</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@ ${admission_cost:,} / Stay</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; min-height: 98px; height: 98px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Pareto Concentration</div>
            <div style="font-size: 24px; font-weight: 800; color: #7C3AED; line-height: 1.1;">{pareto_share:.1f}%</div>
            <div style="font-size: 12px; color: #64748B; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">High & Severe Tiers</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. INPATIENT COST EXPOSURE & PARETO CONCENTRATION (SIDE-BY-SIDE)
# ==============================================================================
st.header("2. Annual Inpatient Financial Liability & 80/20 Risk Concentration")

v7_col1, v7_col2 = st.columns(2, gap="large")

with v7_col1:
    # Visual 7A: Cost Exposure by Acuity Tier (Horizontal Bar)
    fig_v7a = go.Figure()

    fig_v7a.add_trace(go.Bar(
        y=cost_df["clinical_risk_tier"],
        x=cost_df["cost_millions"],
        orientation="h",
        width=0.42,
        marker=dict(color=[acuity_colors[t] for t in cost_df["clinical_risk_tier"]]),
        text=[f"<b>${c:.2f}M</b> ({adm:.1f} adm)" for c, adm in zip(cost_df["cost_millions"], cost_df["expected_admissions"])],
        textposition="outside",
        textfont=dict(color="#0F172A", size=11.5, family="Be Vietnam Pro"),
        hovertemplate="<b>%{y}</b><br>Projected Cost: $%{x:.3f}M<br>Expected Admissions: %{customdata[0]:.1f}<br>Patient Count: %{customdata[1]:,}<extra></extra>",
        customdata=cost_df[["expected_admissions", "patient_count"]].values
    ))

    max_x = max(cost_df["cost_millions"]) * 1.45 if max(cost_df["cost_millions"]) > 0 else 1.0

    fig_v7a.update_layout(
        title=dict(text="<b>Annual Inpatient Cost Exposure by Acuity Tier</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
        margin=dict(l=120, r=30, t=50, b=40),
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Projected Acute Inpatient Exposure ($ Millions)", range=[0, max_x]),
        yaxis=dict(title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v7a, width="stretch")

with v7_col2:
    # Visual 7B: Pareto Risk Concentration Donut
    pareto_df = pd.DataFrame({
        "Tier Group": ["High & Severe Acuity", "Low & Moderate Acuity"],
        "Cost": [high_severe_cost, low_mod_cost],
        "Share": [pareto_share, 100.0 - pareto_share]
    })

    fig_v7b = go.Figure(data=[go.Pie(
        labels=pareto_df["Tier Group"],
        values=pareto_df["Cost"],
        hole=0.55,
        domain=dict(y=[0.22, 1.0]),
        marker=dict(colors=["#DC2626", "#3B82F6"]),
        textinfo="percent",
        textposition="inside",
        insidetextfont=dict(color="#FFFFFF", size=13, family="Be Vietnam Pro"),
        hovertemplate="<b>%{label}</b><br>Cost Exposure: $%{value:,.0f}<br>Proportion: %{percent}<extra></extra>"
    )])

    # Center Text in Donut Hole
    fig_v7b.add_annotation(
        text=f"<b>${total_financial_exposure / 1e6:.2f}M</b><br><span style='font-size:10px; color:#64748B;'>Total Annual<br>Cost Exposure</span>",
        x=0.5, y=0.61,
        showarrow=False,
        font=dict(size=14, color="#0F172A", family="Be Vietnam Pro")
    )

    fig_v7b.update_layout(
        title=dict(text="<b>80/20 Pareto Financial Risk Concentration</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
        margin=dict(l=10, r=10, t=50, b=40),
        legend=dict(orientation="h", yanchor="top", y=0.15, xanchor="center", x=0.5, font=dict(family="Be Vietnam Pro", size=11)),
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Be Vietnam Pro, sans-serif")
    )
    st.plotly_chart(fig_v7b, width="stretch")

# Narrative Directly Under Visual 7
severe_cost = cost_df.loc[cost_df['clinical_risk_tier'] == 'Severe Acuity', 'cost_exposure'].values[0]

st.markdown(
    f"""
    **Actuarial Inpatient Risk Assessment**: In value-based ACO contracts, acute inpatient admissions represent the single largest 
    source of avoidable medical expense. Applying national **AHRQ HCUP benchmarks** (&dollar;{admission_cost:,} average cost per acute chronic stay) 
    against actuarial admission probabilities (5% for Low Acuity, 15% for Moderate, 35% for High, and 65% for Severe), 
    Metropolitan Health System faces a baseline inpatient exposure of **&dollar;{total_financial_exposure / 1e6:.2f}M across {total_projected_admissions:.1f} projected admissions** 
    in this cohort alone.
    
    The Pareto decomposition on the right illustrates the classic **80/20 risk asymmetry of population health**:
    * **The Critical Driver**: The High and Severe Acuity tiers account for **&dollar;{high_severe_cost / 1e6:.2f}M ({pareto_share:.1f}%)** of the entire 
      health system's financial liability. Specifically, the 204 Severe Acuity patients (mean SBP ≥140 mmHg or total cholesterol ≥240 mg/dL) 
      generate **&dollar;{severe_cost / 1e6:.2f}M** in exposure alone, with a staggering 65% annual admission probability.
    * **Strategic ROI Focus**: Traditional disease management programs dilute resources by broadcasting educational materials across the entire panel. 
      These actuarial figures prove that care management resources must be intensely concentrated: deploying nurse navigators to stabilize 
      the top two acuity tiers controls over four-fifths of the system's total balance sheet exposure.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. HEDIS QUALITY BENCHMARKS & STATIN REMEDIATION SIMULATOR
# ==============================================================================
st.header("3. National HEDIS Quality Benchmark Audit & Remediation Simulator")

st.markdown(
    """
    Beyond direct inpatient admissions, value-based contracts tie significant quality incentive bonuses and penalty clawbacks 
    to **NCQA HEDIS quality measures** and **CMS Star Ratings**. Auditing the 983-patient cohort against national clinical standards 
    uncovers a critical dichotomy: while hypertension blood pressure control surpasses federal targets, statin adherence exhibits 
    alarming double-digit quality deficits.
    """
)

# Interactive Remediation Simulator Slider
sim_col1, sim_col2 = st.columns([1.5, 1.0], gap="large")

with sim_col1:
    remediation_rate = st.slider(
        "Simulate Statin Care Gap Closure Rate (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        format="%d%%",
        help="Simulate the impact of proactive nurse-led medication titration closing statin prescription gaps."
    )

with sim_col2:
    if remediation_rate == 0:
        sim_status = "Baseline Audit (0% Remediation)"
        badge_style = "background-color: #FEF2F2; color: #991B1B; border: 1px solid #FCA5A5;"
    elif remediation_rate < 50:
        sim_status = f"Active Remediation ({remediation_rate}% Closed)"
        badge_style = "background-color: #FFFBEB; color: #92400E; border: 1px solid #FCD34D;"
    else:
        sim_status = f"Aggressive Outreach ({remediation_rate}% Closed)"
        badge_style = "background-color: #ECFDF5; color: #047857; border: 1px solid #6EE7B7;"

    st.markdown(
        f"""
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Simulation Mode</div>
        <div style="{badge_style} border-radius: 6px; padding: 10px 14px; font-size: 12.5px; font-weight: 600;">
            {sim_status}
        </div>
        """,
        unsafe_allow_html=True
    )

# Compute HEDIS Performance Metrics
cond_clean = df["condition"].astype(str).str.strip().str.lower()
med_clean = df["medication"].astype(str).str.strip().str.lower()

# Measure 1: Controlling Blood Pressure (CBP)
htn_mask = cond_clean == "hypertension"
n_htn = htn_mask.sum()
cbp_rate = ((df.loc[htn_mask, "systolic_bp"] < 140) & (df.loc[htn_mask, "diastolic_bp"] < 90)).mean() * 100

# Measure 2: Statin Therapy for Cardiovascular Disease (SPC)
hd_mask = cond_clean == "heart disease"
n_hd = hd_mask.sum()
baseline_hd_statin = (med_clean[hd_mask] == "atorvastatin").sum()
unmet_hd = n_hd - baseline_hd_statin
remediated_hd = round(unmet_hd * (remediation_rate / 100.0))
sim_hd_statin = baseline_hd_statin + remediated_hd
spc_rate = (sim_hd_statin / n_hd * 100) if n_hd > 0 else 0.0

# Measure 3: Statin Therapy for Patients with Diabetes (SUPD)
diab_mask = cond_clean == "diabetes"
n_diab = diab_mask.sum()
baseline_diab_statin = (med_clean[diab_mask] == "atorvastatin").sum()
unmet_diab = n_diab - baseline_diab_statin
remediated_diab = round(unmet_diab * (remediation_rate / 100.0))
sim_diab_statin = baseline_diab_statin + remediated_diab
supd_rate = (sim_diab_statin / n_diab * 100) if n_diab > 0 else 0.0

# Assemble HEDIS Audit Data Table
hedis_rows = [
    {
        "measure_key": "CBP",
        "measure_name": f"<b>CBP: Blood Pressure</b><br><span style='font-size:10px; color:#64748B;'>HTN Cohort (N = {n_htn})</span>",
        "actual_rate": cbp_rate,
        "benchmark_rate": 72.0,
        "gap": cbp_rate - 72.0,
        "target_text": "Target: 72%"
    },
    {
        "measure_key": "SPC",
        "measure_name": f"<b>SPC: Statin (Cardiac)</b><br><span style='font-size:10px; color:#64748B;'>Heart Disease (N = {n_hd})</span>",
        "actual_rate": spc_rate,
        "benchmark_rate": 80.0,
        "gap": spc_rate - 80.0,
        "target_text": "Target: 80%"
    },
    {
        "measure_key": "SUPD",
        "measure_name": f"<b>SUPD: Statin (Diabetes)</b><br><span style='font-size:10px; color:#64748B;'>Diabetic Cohort (N = {n_diab})</span>",
        "actual_rate": supd_rate,
        "benchmark_rate": 78.0,
        "gap": supd_rate - 78.0,
        "target_text": "Target: 78%"
    }
]

hedis_df = pd.DataFrame(hedis_rows)

# Determine Status Badges & Colors
bar_colors = []
status_badges = []
for _, r in hedis_df.iterrows():
    if r["gap"] >= 0:
        bar_colors.append("#10B981") # Goal Met (Green)
        status_badges.append(f"Goal Met (+{r['gap']:.1f}%)")
    else:
        bar_colors.append("#DC2626") # Critical Deficit (Red)
        status_badges.append(f"Critical Deficit ({r['gap']:.1f}%)")

hedis_df["color"] = bar_colors
hedis_df["status"] = status_badges

# Build Executive Bullet Scorecard in Plotly
fig_v8 = go.Figure()

# 1. Background 100% Track (Light Slate)
fig_v8.add_trace(go.Bar(
    y=hedis_df["measure_name"],
    x=[100, 100, 100],
    orientation="h",
    width=0.38,
    marker=dict(color="#F1F5F9"),
    hoverinfo="skip",
    showlegend=False
))

# 2. Actual Performance Bars
fig_v8.add_trace(go.Bar(
    y=hedis_df["measure_name"],
    x=hedis_df["actual_rate"],
    orientation="h",
    width=0.38,
    marker=dict(color=hedis_df["color"]),
    text=[f"<b>{r:.1f}%</b>" for r in hedis_df["actual_rate"]],
    textposition="inside",
    insidetextanchor="start",
    insidetextfont=dict(color="#FFFFFF", size=12, family="Be Vietnam Pro"),
    hovertemplate="<b>%{y}</b><br>Compliance Rate: %{x:.1f}%<extra></extra>",
    showlegend=False
))

# 3. Target Benchmark Tick Markers (Scatter with native line-ns symbol)
fig_v8.add_trace(go.Scatter(
    x=hedis_df["benchmark_rate"],
    y=hedis_df["measure_name"],
    mode="markers+text",
    marker=dict(symbol="line-ns-open", size=36, line=dict(color="#0F172A", width=4)),
    text=[f"<b>Target: {b:.0f}%</b>" for b in hedis_df["benchmark_rate"]],
    textposition="top center",
    textfont=dict(size=10.5, color="#0F172A", family="Be Vietnam Pro"),
    hoverinfo="skip",
    showlegend=False
))

# 4. Status Badges Aligned to Categorical Rows
for _, row in hedis_df.iterrows():
    is_met = row["gap"] >= 0
    badge_color = "#047857" if is_met else "#991B1B"
    badge_bg = "#ECFDF5" if is_met else "#FEF2F2"
    badge_label = row["status"]
    fig_v8.add_annotation(
        x=105,
        y=row["measure_name"],
        text=f"<b>{badge_label}</b>",
        showarrow=False,
        xanchor="left",
        font=dict(size=10.5, color=badge_color, family="Be Vietnam Pro"),
        bgcolor=badge_bg,
        bordercolor=badge_color,
        borderwidth=1,
        borderpad=4
    )

fig_v8.update_layout(
    title=dict(
        text="<b>National HEDIS Quality Benchmark Audit & Compliance Performance Scorecard</b>",
        x=0.5, y=0.96, xanchor="center", yanchor="top"
    ),
    margin=dict(l=220, r=30, t=65, b=40),
    height=400,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Compliance / Performance Rate (%)", range=[0, 138]),
    yaxis=dict(title="", tickfont=dict(size=12, family="Be Vietnam Pro"), autorange="reversed"),
    font=dict(family="Be Vietnam Pro, sans-serif")
)

st.plotly_chart(fig_v8, width="stretch")

# Narrative Directly Under Visual 8
st.markdown(
    """
    **Quality Governance & CMS Star Rating Assessment**: Under federal CMS Medicare Advantage Star Ratings, health systems are scored on a 1-to-5 star scale. 
    Achieving a 4.0 or 5.0 Star Rating unlocks substantial annual Quality Bonus Payments (typically 5% bonus on Medicare benchmark payments), 
    while falling below 3.5 stars results in marketing restrictions, loss of auto-enrollment, and severe financial penalties.
    
    The audit above reveals a profound clinical paradox:
    * **Clinical Success in Hypertension (HEDIS CBP)**: Metropolitan Health achieves a **76.5% compliance rate** on Controlling High Blood Pressure 
      (`<140/90 mmHg`), outperforming the national 72.0% benchmark by **+4.5%**. This reflects sound primary care physician practices during clinic visits.
    * **Severe Regulatory Deficits in Statin Therapy (HEDIS SPC & SUPD)**: In stark contrast, only **26.6% of heart disease patients** (against an 80.0% benchmark) 
      and **19.6% of diabetic patients** (against a 78.0% benchmark) are actively prescribed guideline-directed statin therapy (`Atorvastatin`). 
      These double-digit deficits (**-53.4%** and **-58.4%**) drag Metropolitan Health's Star Rating directly into 1-star penalty territory on cardiovascular measures.
    * **The Interactive Simulation**: Dragging the remediation slider above illustrates the operational solution. Closing just **50% of statin gaps** 
      moves diabetic adherence to ~60% and cardiac adherence to ~63%, immediately lifting Metropolitan Health out of severe penalty bands and recovering 
      millions of dollars in at-risk Medicare Advantage quality incentives.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; line-height: 1.6;'>
        <em>To evaluate preventative care economic breakeven and nurse staffing requirements, proceed to 
        <strong>ROI & Staffing Model</strong> in the navigation rail.</em>
    </p>
    """,
    unsafe_allow_html=True
)

