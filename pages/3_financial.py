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

# KPI Metric Strip (Clean responsive scorecard architecture)
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Audited Cohort</div>
            <div class="kpi-card-value" style="color: #0F172A;">{total_patients:,}</div>
            <div class="kpi-card-subtitle">
                <span>{selected_service}</span>
                <span class="kpi-badge kpi-badge-blue">Audited</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Projected Admissions</div>
            <div class="kpi-card-value" style="color: #2563EB;">{total_projected_admissions:.1f}</div>
            <div class="kpi-card-subtitle">
                <span>Annual Inpatient</span>
                <span class="kpi-badge kpi-badge-amber">At Risk</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Financial Liability</div>
            <div class="kpi-card-value" style="color: #DC2626;">&dollar;{total_financial_exposure / 1e6:.2f}M</div>
            <div class="kpi-card-subtitle">
                <span>@ &dollar;{admission_cost:,}/Stay</span>
                <span class="kpi-badge kpi-badge-red">AHRQ HCUP</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-metric-card">
            <div class="kpi-card-title">Pareto Concentration</div>
            <div class="kpi-card-value" style="color: #7C3AED;">{pareto_share:.1f}%</div>
            <div class="kpi-card-subtitle">
                <span>High & Severe</span>
                <span class="kpi-badge kpi-badge-red">Top 20% Panel</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. INPATIENT COST EXPOSURE & PARETO CONCENTRATION (STANDALONE VISUALS)
# ==============================================================================
st.header("2. Annual Inpatient Financial Liability & 80/20 Risk Concentration")

# Visual 7A: Cost Exposure by Acuity Tier (Horizontal Bar - Standalone Full Width)
fig_v7a = go.Figure()

fig_v7a.add_trace(go.Bar(
    y=cost_df["clinical_risk_tier"],
    x=cost_df["cost_millions"],
    orientation="h",
    width=0.42,
    marker=dict(color=[acuity_colors[t] for t in cost_df["clinical_risk_tier"]]),
    text=[f"<b>${c:.2f}M</b> ({adm:.0f} adm)" for c, adm in zip(cost_df["cost_millions"], cost_df["expected_admissions"])],
    textposition="outside",
    textfont=dict(color="#0F172A", size=11.5, family="Be Vietnam Pro"),
    hovertemplate="<b>%{y}</b><br>Projected Cost: $%{x:.3f}M<br>Expected Admissions: %{customdata[0]:.1f}<br>Patient Count: %{customdata[1]:,}<extra></extra>",
    customdata=cost_df[["expected_admissions", "patient_count"]].values
))

max_x = max(cost_df["cost_millions"]) * 1.35 if max(cost_df["cost_millions"]) > 0 else 1.0

fig_v7a.update_layout(
    title=dict(text="<b>Annual Inpatient Cost Exposure by Acuity Tier</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
    margin=dict(l=125, r=80, t=50, b=40),
    height=390,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Projected Acute Inpatient Exposure ($ Millions)", range=[0, max_x]),
    yaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v7a, width="stretch")

# Analysis Directly Under Visual 7A
severe_cost = cost_df.loc[cost_df['clinical_risk_tier'] == 'Severe Acuity', 'cost_exposure'].values[0] if not cost_df.empty else 0
st.markdown(
    f"""
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Actuarial Inpatient Risk Assessment by Acuity Tier</strong>: In value-based ACO contracts, acute inpatient admissions represent the single largest 
        source of avoidable medical expense. Applying national <strong>AHRQ HCUP benchmarks</strong> (&dollar;{admission_cost:,} average cost per acute chronic stay) 
        against actuarial admission probabilities (5% for Low Acuity, 15% for Moderate, 35% for High, and 65% for Severe), 
        Metropolitan Health System faces a baseline inpatient exposure of <strong>&dollar;{total_financial_exposure / 1e6:.2f}M across {total_projected_admissions:.1f} projected admissions</strong> 
        in this cohort alone.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Visual 7B: Pareto Risk Concentration Donut (Standalone Full Width)
pareto_df = pd.DataFrame({
    "Tier Group": ["High & Severe Acuity", "Low & Moderate Acuity"],
    "Cost": [high_severe_cost, low_mod_cost],
    "Share": [pareto_share, 100.0 - pareto_share]
})

fig_v7b = go.Figure(data=[go.Pie(
    labels=pareto_df["Tier Group"],
    values=pareto_df["Cost"],
    hole=0.55,
    domain=dict(y=[0.18, 1.0]),
    marker=dict(colors=["#DC2626", "#3B82F6"]),
    textinfo="percent",
    textposition="inside",
    insidetextfont=dict(color="#FFFFFF", size=13, family="Be Vietnam Pro"),
    hovertemplate="<b>%{label}</b><br>Cost Exposure: $%{value:,.0f}<br>Proportion: %{percent}<extra></extra>"
)])

# Center Text in Donut Hole
fig_v7b.add_annotation(
    text=f"<b>${total_financial_exposure / 1e6:.2f}M</b><br><span style='font-size:10px; color:#64748B;'>Total Annual<br>Cost Exposure</span>",
    x=0.5, y=0.59,
    showarrow=False,
    font=dict(size=14, color="#0F172A", family="Be Vietnam Pro")
)

fig_v7b.update_layout(
    title=dict(text="<b>80/20 Pareto Financial Risk Concentration</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="h", yanchor="top", y=0.08, xanchor="center", x=0.5, font=dict(family="Be Vietnam Pro", size=11.5)),
    height=400,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Be Vietnam Pro, sans-serif")
)
st.plotly_chart(fig_v7b, width="stretch")

# Analysis Directly Under Visual 7B
st.markdown(
    f"""
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>80/20 Pareto Financial Risk Concentration</strong>: The Pareto decomposition illustrates the classic risk asymmetry of population health:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>The Critical Driver</strong>: The High and Severe Acuity tiers account for <strong>&dollar;{high_severe_cost / 1e6:.2f}M ({pareto_share:.1f}%)</strong> of the entire health system's financial liability. Specifically, the 204 Severe Acuity patients (mean SBP ≥140 mmHg or total cholesterol ≥240 mg/dL) generate <strong>&dollar;{severe_cost / 1e6:.2f}M</strong> in exposure alone, with a significant 65% annual admission probability.</li>
        <li style='margin-bottom: 8px;'><strong>Strategic ROI Focus</strong>: Traditional disease management programs dilute resources by broadcasting educational materials across the entire panel. These actuarial figures prove that care management resources must be intensely concentrated: deploying nurse navigators to stabilize the top two acuity tiers controls over four-fifths of the system's total balance sheet exposure.</li>
    </ul>
    """,
    unsafe_allow_html=True
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
    xaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Compliance / Performance Rate (%)", range=[0, 138]),
    yaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro"), autorange="reversed"),
    font=dict(family="Be Vietnam Pro, sans-serif")
)

st.plotly_chart(fig_v8, width="stretch")

# Narrative Directly Under Visual 8
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Quality Governance & CMS Star Rating Assessment</strong>: Under federal CMS Medicare Advantage Star Ratings, health systems are scored on a 1-to-5 star scale. 
        Achieving a 4.0 or 5.0 Star Rating unlocks substantial annual Quality Bonus Payments (typically 5% bonus on Medicare benchmark payments), 
        while falling below 3.5 stars results in marketing restrictions, loss of auto-enrollment, and severe financial penalties.
    </p>
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; margin-top: 6px;'>
        The audit above reveals a profound clinical paradox:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Clinical Success in Hypertension (HEDIS CBP)</strong>: Metropolitan Health achieves a <strong>76.5% compliance rate</strong> on Controlling High Blood Pressure (&lt;140/90 mmHg), outperforming the national 72.0% benchmark by <strong>+4.5%</strong>. This reflects sound primary care physician practices during clinic visits.</li>
        <li style='margin-bottom: 8px;'><strong>Severe Regulatory Deficits in Statin Therapy (HEDIS SPC & SUPD)</strong>: In stark contrast, only <strong>26.6% of heart disease patients</strong> (against an 80.0% benchmark) and <strong>19.6% of diabetic patients</strong> (against a 78.0% benchmark) are actively prescribed guideline-directed statin therapy (Atorvastatin). These double-digit deficits (<strong>-53.4%</strong> and <strong>-58.4%</strong>) drag Metropolitan Health's Star Rating directly into 1-star penalty territory on cardiovascular measures.</li>
        <li style='margin-bottom: 8px;'><strong>The Interactive Simulation</strong>: Dragging the remediation slider above illustrates the operational solution. Closing just <strong>50% of statin gaps</strong> moves diabetic adherence to ~60% and cardiac adherence to ~63%, immediately lifting Metropolitan Health out of severe penalty bands and recovering millions of dollars in at-risk Medicare Advantage quality incentives.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 6. INTERACTIVE CMS STAR RATING & QUALITY BONUS CALCULATOR
# ==============================================================================
st.subheader("Interactive CMS Star Rating & Quality Revenue Simulation")

st.markdown(
    """
    Under Medicare Advantage two-sided risk contracts, achieving a 4.0+ Star Rating unlocks annual 
    Quality Bonus Payments (QBP). Test different Star Rating tiers below to evaluate the gross revenue capture 
    associated with closing Metropolitan Health's blood pressure and statin care gaps:
    """
)

star_col1, star_col2 = st.columns([1.1, 1.4], gap="medium")

with star_col1:
    star_target = st.select_slider(
        "Simulated CMS Star Rating Performance Target:",
        options=[3.0, 3.5, 4.0, 4.5, 5.0],
        value=4.0,
        format_func=lambda x: f"★ {x:.1f} Stars" + (" (Current Baseline)" if x == 3.0 else (" (Target)" if x == 4.0 else "")),
        help="Simulate the top-line quality revenue unlocked by remediating HEDIS statin and hypertension gaps."
    )

star_bonus_map = {
    3.0: 0,
    3.5: 150000,
    4.0: 420000,
    4.5: 630000,
    5.0: 900000
}
unlocked_bonus = star_bonus_map[star_target]
status_tag = "Baseline / Penalty Band" if star_target == 3.0 else ("Quality Shared Savings Unlocked" if star_target < 4.5 else "5% Full CMS Quality Bonus Unlocked")
badge_class = "kpi-badge-red" if star_target == 3.0 else ("kpi-badge-amber" if star_target == 3.5 else "kpi-badge-green")

with star_col2:
    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px 18px; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.06em;">CMS Quality Revenue Unlocked</span>
                <span class="kpi-badge {badge_class}">{status_tag}</span>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: #059669; line-height: 1.1; margin-bottom: 4px;">
                +&dollar;{unlocked_bonus:,.0f} / yr
            </div>
            <div style="font-size: 12.5px; color: #475569; line-height: 1.4;">
                Simulated for <strong>★ {star_target:.1f} Stars</strong> across the 983-patient chronic disease panel.
            </div>
        </div>
        """,
        unsafe_allow_html=True
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

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.markdown("---")

# Executive Tour Progression Card
tour_col1, tour_col2 = st.columns([2.4, 1.2], gap="medium")
with tour_col1:
    st.markdown(
        """
        <div style="padding: 2px 0;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #2563EB; margin-bottom: 2px;">
                EXECUTIVE TOUR &bull; ACT 4 OF 4
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">
                ROI & Preventative Care Staffing Model
            </div>
            <div style="font-size: 12.5px; color: #64748B;">
                Simulate 7.0 RN FTE caseload calibration, admission reduction sensitivities, and the 159% self-funding model.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with tour_col2:
    try:
        st.page_link(
            "pages/4_roi.py",
            label="Proceed to ROI Model →",
            icon="📈",
            use_container_width=True
        )
    except Exception:
        if st.button("Proceed to ROI Model →", key="tour_fin_btn", use_container_width=True):
            st.switch_page("pages/4_roi.py")

