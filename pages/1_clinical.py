# pages/1_clinical.py
"""
Act 1: Clinical Risk Acuity & Pharmacotherapy Care Gaps
Author: Daniel Ademola Dongo
Setting: Metropolitan Health Integrated Network (ACO)
Narrative Flow Style: Interactive Clinical Workbench with Integrated Real-Time Narrative
Answers Questions 1, 6, 4, and 5
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. DATA REPOSITORY & PIPELINE RECOVERY
# ==============================================================================
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "healthcare_analytics_enriched.csv"
if not DATA_PATH.exists():
    DATA_PATH = Path("data/processed/healthcare_analytics_enriched.csv")

@st.cache_data
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()

df = load_data()

# ==============================================================================
# 2. PAGE HEADER & CLINICAL FRAMING
# ==============================================================================
st.title("Clinical Risk Stratification & Patient Safety")
st.caption("Guideline-Concordant Acuity Profiling, Demographic Care Gaps & Pharmacotherapy Safety")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    In value-based healthcare contracts, managing population health requires objective, protocolized risk stratification. 
    Traditional episodic workflows rely on physician intuition during infrequent 15-minute consultations, allowing chronic disease 
    decompensations to evolve silently. 
    
    This analytical module audits the **983-patient chronic cohort** against gold-standard clinical guidelines: 
    the **2017 ACC/AHA High Blood Pressure Clinical Practice Guidelines** and the **National Cholesterol Education Program 
    (NCEP) Adult Treatment Panel III**. By cross-referencing biometric vitals, diagnostic registries, and active pharmacotherapy, 
    this audit identifies vascular deterioration, quantifies unmedicated chronic disease burden, and uncovers 
    life-threatening prescribing discordances.
    """
)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. DYNAMIC INTERPRETATION GENERATOR FUNCTION
# ==============================================================================
def get_clinical_narrative(cond, tier, n, pct, mean_sbp, mean_chol, unmed_count):
    # Case 1: Default Baseline (All Conditions x All Tiers)
    if cond == "All Conditions" and tier == "All Acuity Tiers":
        return (
            "The bivariate distribution maps patient vulnerability across vascular pressure and serum lipid concentration for all 983 patients. "
            "Under **2017 ACC/AHA guidelines**, normal systolic pressure is `<120 mmHg`, Stage 1 HTN is `130–139 mmHg`, and Stage 2 HTN is `≥140 mmHg`. "
            "Concurrently, **NCEP ATP III guidelines** establish total cholesterol `<200 mg/dL` as desirable and `≥240 mg/dL` as high risk.\n\n"
            "**553 patients (56.3% of the cohort)** sit in High or Severe Acuity tiers. These individuals experience concurrent uncontrolled "
            "hypertension and dyslipidemia, driving preventable emergency department visits and acute inpatient admissions (&dollar;12,500 benchmark). "
            "Select specific disease or acuity filters above to inspect subgroup clinical dynamics."
        )

    # Case 2: Severe Acuity Subgroups
    elif tier == "Severe Acuity":
        if cond == "Heart Disease":
            return (
                f"These {n} cardiac patients combine diagnosed coronary disease with severe Stage 2 hypertension (mean SBP {mean_sbp:.1f} mmHg) "
                f"and hypercholesterolemia (mean cholesterol {mean_chol:.1f} mg/dL). Uncontrolled systolic pressure dramatically elevates myocardial "
                f"oxygen demand while lipid plaque vulnerability accelerates coronary thrombosis. Notably, **{unmed_count} patients are completely unmedicated**. "
                f"This subgroup represents Metropolitan Health's single highest 30-day acute myocardial infarction and readmission liability. "
                f"**Action Mandate**: Immediate 48-hour telephonic triage by an RN care coordinator and expedited cardiology re-evaluation."
            )
        elif cond == "Diabetes":
            return (
                f"These {n} diabetic patients present with critical vascular strain (mean SBP {mean_sbp:.1f} mmHg) and lipid elevation "
                f"(mean cholesterol {mean_chol:.1f} mg/dL), with **{unmed_count} unmedicated individuals**. In chronic diabetes, systolic pressure "
                f"≥130 mmHg exponentially accelerates glomerular hyperfiltration, microalbuminuria, and diabetic retinopathy. "
                f"Combined with dyslipidemia, this cohort faces compounding peripheral vascular and renal failure liabilities. "
                f"**Action Mandate**: Prioritize nurse-led initiation of ACE-I/ARB renal protection protocols and multidisciplinary endocrinology recall."
            )
        elif cond == "Hypertension":
            return (
                f"These {n} patients suffer from severe, uncontrolled hypertensive vascular disease (mean SBP {mean_sbp:.1f} mmHg, "
                f"mean cholesterol {mean_chol:.1f} mg/dL), with **{unmed_count} patients receiving zero anti-hypertensive therapy**. "
                f"Vascular pressures in this range double the 5-year risk of hemorrhagic or ischemic stroke and degrade HEDIS Star Ratings. "
                f"**Action Mandate**: Immediate dual-agent pharmacotherapy titration (e.g. ACE-I/ARB plus CCB) via protocolized nurse outreach."
            )
        elif cond == "Asthma":
            return (
                f"These {n} asthmatic patients exhibit compounding Stage 2 hypertension (mean SBP {mean_sbp:.1f} mmHg, mean cholesterol {mean_chol:.1f} mg/dL). "
                f"In chronic pulmonary disease, severe hypertension increases pulmonary artery pressures and strains the right ventricle. "
                f"Treating hypertension in asthmatics requires vigilance: non-cardioselective beta-blockers and ACE-inhibitors are contraindicated. "
                f"**Action Mandate**: Medication review to verify zero asthmatics are on bronchoconstrictive anti-hypertensives."
            )
        else: # All Conditions x Severe Acuity
            return (
                f"Across all disease registries, {n} patients are classified in Severe Acuity (mean SBP {mean_sbp:.1f} mmHg, "
                f"mean cholesterol {mean_chol:.1f} mg/dL, **{unmed_count} unmedicated**). This high-risk cohort accounts for the vast majority "
                f"of avoidable acute hospitalizations under AHRQ HCUP benchmarks. **Action Mandate**: Primary caseload target for Metropolitan Health's "
                f"7.0 RN FTE care coordination unit, where intensive nurse management directly averts &dollar;12,500 inpatient stays."
            )

    # Case 3: High Acuity Subgroups
    elif tier == "High Acuity":
        if cond == "Heart Disease":
            return (
                f"These {n} cardiac patients exhibit Stage 1 hypertension (mean SBP {mean_sbp:.1f} mmHg) and borderline hypercholesterolemia "
                f"(mean cholesterol {mean_chol:.1f} mg/dL), with **{unmed_count} unmedicated individuals**. Uncontrolled Stage 1 pressures continuously "
                f"fatigue myocardial tissue. **Action Mandate**: Schedule outpatient nurse telehealth consults within 14 days to optimize statin therapy."
            )
        elif cond == "Diabetes":
            return (
                f"These {n} patients have documented diabetes with Stage 1 hypertension (mean SBP {mean_sbp:.1f} mmHg) and elevated lipids "
                f"(mean cholesterol {mean_chol:.1f} mg/dL, **{unmed_count} unmedicated**). The 2017 ACC/AHA guidelines mandate a strict target "
                f"of `<130/80 mmHg` for all diabetic patients. **Action Mandate**: Reconcile HbA1c and lipid panels, engaging pharmacists for titration."
            )
        elif cond == "Hypertension":
            return (
                f"Representing {pct:.1f}% of the health system's panel, these {n} patients exhibit Stage 1/Stage 2 hypertension "
                f"(mean SBP {mean_sbp:.1f} mmHg, **{unmed_count} unmedicated**). This group represents the primary opportunity for HEDIS "
                f"Controlling High Blood Pressure (CBP) quality metric remediation. **Action Mandate**: Deploy automated home BP monitoring recall."
            )
        elif cond == "Asthma":
            return (
                f"These {n} patients present with persistent Stage 1 hypertension (mean SBP {mean_sbp:.1f} mmHg, mean cholesterol {mean_chol:.1f} mg/dL). "
                f"Systemic vascular resistance complicates dyspnea evaluation. **Action Mandate**: Ensure BP control is managed with dihydropyridine "
                f"calcium channel blockers or ARBs, avoiding drugs that trigger bronchial hyper-reactivity."
            )
        else: # All Conditions x High Acuity
            return (
                f"With {n} patients exhibiting Stage 1 hypertension (mean SBP {mean_sbp:.1f} mmHg, mean cholesterol {mean_chol:.1f} mg/dL), "
                f"this tier represents the 'rising risk' population. Left unmanaged, 40–50% of this cohort will progress into Severe Acuity "
                f"within 12 to 18 months. **Action Mandate**: Proactive care management recall to arrest vascular deterioration."
            )

    # Case 4: Moderate Acuity Subgroups
    elif tier == "Moderate Acuity":
        return (
            f"Patients in this tier ({cond}, N = {n}) present with elevated or early Stage 1 vitals (mean SBP {mean_sbp:.1f} mmHg, "
            f"mean cholesterol {mean_chol:.1f} mg/dL, **{unmed_count} unmedicated**). Acute hospitalization risk is low in the short term, "
            f"but unaddressed lifestyle factors cause progressive arterial stiffening. **Action Mandate**: Enroll in automated digital SMS health reminders, "
            f"dietary counseling, and bi-monthly blood pressure tracking."
        )

    # Case 5: Low Acuity Subgroups
    elif tier == "Low Acuity":
        return (
            f"Patients in this tier ({cond}, N = {n}) exhibit normal, well-controlled biometric vitals (mean SBP {mean_sbp:.1f} mmHg, "
            f"mean cholesterol {mean_chol:.1f} mg/dL). These individuals represent clinical success stories within Metropolitan Health. "
            f"**Action Mandate**: Standard annual primary care wellness examinations. Zero intensive 1:1 nurse caseload allocation is required, "
            f"preserving operational capacity for the 553 high-acuity patients."
        )

    # Case 6: Condition Overviews (Condition x All Tiers)
    else:
        return (
            f"Across all acuity levels, the {cond} registry ({n} patients, {pct:.1f}% of cohort) exhibits an average systolic blood pressure of "
            f"{mean_sbp:.1f} mmHg and cholesterol of {mean_chol:.1f} mg/dL, with **{unmed_count} patients receiving zero pharmacotherapy**. "
            f"The scatter plot on the left highlights significant internal polarization: while a minority are well-controlled in Low/Moderate tiers, "
            f"the majority cluster in high-risk quadrants requiring protocolized care coordination."
        )

# ==============================================================================
# 4. CLINICAL ACUITY WORKBENCH (SIDE-BY-SIDE INTERACTIVE LAYOUT)
# ==============================================================================
st.header("1. Clinical Acuity Matrix: Blood Pressure vs. Lipid Stratification")

if not df.empty:
    chart_col, inspector_col = st.columns([1.45, 1.0], gap="medium")

    with inspector_col:
        st.markdown("#### 🔍 Cohort Inspector & Controls")
        st.caption("Adjust filters below to update the clinical plot and diagnostic interpretation in real time.")
        
        conditions_available = ["All Conditions"] + sorted([c.title() for c in df["condition"].dropna().unique() if c != "Unknown"])
        selected_condition = st.selectbox("Chronic Disease Registry:", conditions_available)

        tiers_available = ["All Acuity Tiers", "Severe Acuity", "High Acuity", "Moderate Acuity", "Low Acuity"]
        selected_tier = st.selectbox("Clinical Acuity Tier:", tiers_available)

        # Apply filtering
        filtered_df = df.copy()
        if selected_condition != "All Conditions":
            filtered_df = filtered_df[filtered_df["condition"].str.title() == selected_condition]
        if selected_tier != "All Acuity Tiers":
            filtered_df = filtered_df[filtered_df["clinical_risk_tier"] == selected_tier]

        # Calculate live metrics
        sub_n = len(filtered_df)
        sub_pct = (sub_n / len(df)) * 100
        sub_sbp = filtered_df["systolic_bp"].mean() if sub_n > 0 else 0
        sub_chol = filtered_df["cholesterol"].mean() if sub_n > 0 else 0
        sub_unmed = filtered_df["unmedicated_chronic"].sum() if "unmedicated_chronic" in filtered_df.columns else 0

        # Compact Live Metric Pill Row
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px; margin-top: 10px; margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #1D4ED8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                    Cohort Vital Signs Summary
                </div>
                <div style="font-size: 12.5px; color: #334155; line-height: 1.5;">
                    • <strong>{sub_n:,} Patients</strong> ({sub_pct:.1f}% of Cohort)<br>
                    • Mean SBP: <strong>{sub_sbp:.1f} mmHg</strong><br>
                    • Mean Total Cholesterol: <strong>{sub_chol:.1f} mg/dL</strong><br>
                    • Unmedicated Chronic Care Gaps: <strong>{sub_unmed}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="font-size: 13px; font-weight: 700; color: #0F172A; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 10px; margin-bottom: 6px;">
                🩺 Clinical Diagnostic Interpretation
            </div>
            """,
            unsafe_allow_html=True
        )
        dynamic_text = get_clinical_narrative(selected_condition, selected_tier, sub_n, sub_pct, sub_sbp, sub_chol, sub_unmed)
        st.markdown(f'<div class="inspector-text">{dynamic_text}</div>', unsafe_allow_html=True)

    with chart_col:
        # Apply Natural Biological Dispersion around Measurement Clusters (matching Notebook Visual 1)
        plot_df = filtered_df.copy()
        np.random.seed(42)
        plot_df["cholesterol_plot"] = plot_df["cholesterol"] + np.random.normal(0, 2.5, size=len(plot_df))
        plot_df["systolic_bp_plot"] = plot_df["systolic_bp"] + np.random.normal(0, 1.4, size=len(plot_df))

        # Color palette matching clinical severity
        acuity_palette = {
            "Low Acuity": "#10B981",       # Emerald Green
            "Moderate Acuity": "#3B82F6",  # Blue
            "High Acuity": "#F59E0B",      # Amber
            "Severe Acuity": "#DC2626"     # Crimson Red
        }

        fig_v1 = px.scatter(
            plot_df,
            x="cholesterol_plot",
            y="systolic_bp_plot",
            color="clinical_risk_tier",
            color_discrete_map=acuity_palette,
            category_orders={"clinical_risk_tier": ["Low Acuity", "Moderate Acuity", "High Acuity", "Severe Acuity"]},
            hover_data={
                "cholesterol_plot": False,
                "systolic_bp_plot": False,
                "patient_name": True,
                "age": True,
                "condition": True,
                "systolic_bp": True,
                "diastolic_bp": True,
                "cholesterol": True,
                "clinical_risk_tier": True
            }
        )

        # Reference Threshold Lines: AHA/ACC BP Guidelines & NCEP ATP III
        fig_v1.add_hline(
            y=130, 
            line_dash="dot", 
            line_color="#F59E0B", 
            annotation_text="AHA Stage 1 (130 mmHg)", 
            annotation_position="bottom left",
            annotation_font=dict(color="#B45309", size=10.5, family="Be Vietnam Pro")
        )
        fig_v1.add_hline(
            y=140, 
            line_dash="dash", 
            line_color="#DC2626", 
            annotation_text="AHA Stage 2 (140 mmHg)", 
            annotation_position="top left",
            annotation_font=dict(color="#991B1B", size=10.5, family="Be Vietnam Pro")
        )
        fig_v1.add_vline(
            x=200, 
            line_dash="dot", 
            line_color="#2563EB", 
            annotation_text="NCEP Border (200 mg/dL)", 
            annotation_position="top right",
            annotation_font=dict(color="#1D4ED8", size=10.5, family="Be Vietnam Pro")
        )

        fig_v1.update_traces(
            marker=dict(size=7.5, opacity=0.82, line=dict(width=0.5, color="#FFFFFF")),
            hovertemplate="<b>Patient:</b> %{customdata[2]}<br>" +
                          "<b>Age:</b> %{customdata[3]} | <b>Condition:</b> %{customdata[4]}<br>" +
                          "<b>Recorded Systolic BP:</b> %{customdata[5]} mmHg<br>" +
                          "<b>Recorded Diastolic BP:</b> %{customdata[6]} mmHg<br>" +
                          "<b>Recorded Cholesterol:</b> %{customdata[7]} mg/dL<br>" +
                          "<b>Acuity Tier:</b> %{customdata[8]}<extra></extra>"
        )

        fig_v1.update_layout(
            margin=dict(l=40, r=20, t=15, b=85),
            height=480,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Total Cholesterol (mg/dL) — NCEP ATP III", range=[150, 235]),
            yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Systolic BP (mmHg) — 2017 ACC/AHA", range=[102, 148]),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.16,
                xanchor="center",
                x=0.5,
                title="",
                font=dict(family="Be Vietnam Pro", size=12)
            ),
            font=dict(family="Be Vietnam Pro, sans-serif")
        )

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 6px; padding: 4px 0;">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A; letter-spacing: -0.01em;">
                    Bivariate Clinical Acuity Distribution
                </div>
                <div style="font-size: 12.5px; color: #64748B; font-weight: 500;">
                    {len(plot_df):,} Patients Displayed across SBP & Cholesterol
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(fig_v1, width="stretch")

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. UNMEDICATED CHRONIC CARE GAPS (GROUPED BARS)
# ==============================================================================
st.header("2. Unmedicated Chronic Disease Cohort by Demographic Segments")

if not df.empty:
    unmed_df = df[df["unmedicated_chronic"] == True].copy()
    unmed_df["condition_clean"] = unmed_df["condition"].replace({
        "heart disease": "Heart Disease",
        "diabetes": "Diabetes",
        "hypertension": "Hypertension"
    })
    
    unmed_grouped = unmed_df.groupby(["condition_clean", "age_group"]).size().reset_index(name="Patients")
    
    # Ordering conditions and age groups
    cond_order = ["Heart Disease", "Diabetes", "Hypertension"]
    unmed_grouped["condition_clean"] = pd.Categorical(unmed_grouped["condition_clean"], categories=cond_order, ordered=True)
    unmed_grouped = unmed_grouped.sort_values(["condition_clean", "age_group"])

    age_colors = {
        "<30": "#93C5FD",     # Light Blue (Younger adult cohort)
        "30-44": "#3B82F6",   # Primary Blue (Middle age cohort)
        "45-59": "#2563EB",   # Royal Blue
        "60-74": "#1E3A8A"    # Deep Navy (Senior vulnerable cohort)
    }

    fig_v2 = px.bar(
        unmed_grouped,
        x="condition_clean",
        y="Patients",
        color="age_group",
        barmode="group",
        text="Patients",
        color_discrete_map=age_colors,
        labels={"condition_clean": "Chronic Diagnosis", "Patients": "Unmedicated Patient Count", "age_group": "Age Group"}
    )

    fig_v2.update_traces(
        textposition="outside",
        width=0.22,
        hovertemplate="<b>Condition:</b> %{x}<br><b>Age Bracket:</b> %{fullData.name}<br><b>Unmedicated Patients:</b> %{y}<extra></extra>"
    )

    fig_v2.update_layout(
        title=dict(
            text="<b>Unmedicated Chronic Disease Cohort by Diagnosis & Age Bracket</b><br><span style='font-size:11.5px; color:#64748B; font-weight:500;'>109 Patients with Formal ICD Diagnosis Receiving Zero Pharmacotherapy</span>",
            x=0.5, y=0.97, xanchor="center", yanchor="top"
        ),
        margin=dict(l=20, r=20, t=65, b=85),
        height=440,
        bargap=0.35,
        bargroupgap=0.15,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Number of Patients", range=[0, 32]),
        xaxis=dict(title="", tickfont=dict(size=13, family="Be Vietnam Pro")),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            title="",
            font=dict(family="Be Vietnam Pro", size=11.5)
        ),
        font=dict(family="Be Vietnam Pro, sans-serif")
    )

    st.plotly_chart(fig_v2, width="stretch")

# Narrative Directly Under Visual 2
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Clinical Acuity Findings & Senior Cohort Vulnerabilities</strong>: In a well-managed healthcare network, patients carrying formal ICD-coded diagnoses 
        for chronic vascular or endocrine disease must receive guideline-directed medical therapy. The grouped analysis above isolates the 
        <strong>109 patients who have documented chronic disease but zero prescribed medication</strong> (patients with no active prescription on record).
    </p>
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; margin-top: 6px;'>
        The demographic stratification reveals an alarming clinical vulnerability:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>The Senior Liability (Ages 60–74)</strong>: The deep navy bars demonstrate that senior patients constitute the largest single demographic segment among unmedicated heart disease and diabetes cohorts. In elderly patients, unmedicated coronary artery disease or uncontrolled hyperglycemia accelerates atherosclerosis, precipitating acute myocardial infarction and hyperosmolar hyperglycemic state.</li>
        <li style='margin-bottom: 8px;'><strong>The Working-Age Blind Spot (Ages 30–44)</strong>: A substantial volume of unmedicated hypertensive and diabetic patients sit in the 30–44 age bracket. These individuals frequently underutilize primary care due to employment conflicts, experiencing silent organ damage that surfaces years later as premature renal failure or early heart failure.</li>
        <li style='margin-bottom: 8px;'><strong>Care Management Priority</strong>: Closing these 109 unmedicated care gaps represents the single most actionable clinical objective for the ambulatory nurse outreach unit, offering immediate risk mitigation with standardized first-line pharmacotherapy.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 6. PHARMACOTHERAPY DISCORDANCE HEATMAP
# ==============================================================================
st.header("3. Medication Discordance & Safety Contraindication Heatmap")

if not df.empty:
    # Build Cross-Tabulation Matrix
    ct = pd.crosstab(
        df["condition"].astype(str).str.strip().str.title(),
        df["medication"].astype(str).str.strip().str.title()
    )

    # Order rows and columns explicitly
    row_order = [r for r in ["Heart Disease", "Hypertension", "Diabetes", "Asthma", "Unknown"] if r in ct.index]
    col_order = [c for c in ["Lisinopril", "Metformin", "Atorvastatin", "Albuterol", "None"] if c in ct.columns]
    matrix_clean = ct.reindex(index=row_order, columns=col_order, fill_value=0)

    fig_v3 = px.imshow(
        matrix_clean,
        text_auto=True,
        labels=dict(x="Prescribed Medication", y="Documented Diagnosis", color="Patients"),
        x=matrix_clean.columns,
        y=matrix_clean.index,
        color_continuous_scale="Blues",
        title="<b>Clinical Prescribing Alignment: Documented Condition vs. Active Pharmacotherapy</b>"
    )

    fig_v3.update_traces(
        hovertemplate="<b>Diagnosis:</b> %{y}<br><b>Prescribed Drug:</b> %{x}<br><b>Patient Count:</b> %{z}<extra></extra>",
        textfont=dict(size=14, family="Be Vietnam Pro")
    )

    fig_v3.update_layout(
        margin=dict(l=20, r=20, t=50, b=30),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Active Pharmacotherapy Prescribed", tickfont=dict(size=12, family="Be Vietnam Pro")),
        yaxis=dict(title="Primary Documented Diagnosis", tickfont=dict(size=12, family="Be Vietnam Pro")),
        coloraxis_showscale=False,
        font=dict(family="Be Vietnam Pro, sans-serif")
    )

    st.plotly_chart(fig_v3, width="stretch")

# Narrative Directly Under Visual 3
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Pharmacotherapy Discordance & Contraindication Analysis</strong>: The cross-tabulation matrix above reveals profound pharmacotherapeutic discordance 
        and contraindication risk across the health system's ambulatory network. While diagonal alignment indicates guideline-concordant 
        care (e.g., diabetics on metformin, hypertensives on lisinopril, hyperlipidemic patients on atorvastatin), the off-diagonal cells 
        surface critical prescribing errors:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Severe Contraindication — Asthmatics on Lisinopril (41 Patients)</strong>: ACE inhibitors like Lisinopril inhibit kinase II, causing bradykinin accumulation in respiratory tissue. In asthmatic patients, this triggers severe persistent bronchospasm, intractable cough, and acute airway reactivity that mimics treatment-resistant asthma, driving avoidable Emergency Department visits.</li>
        <li style='margin-bottom: 8px;'><strong>Therapeutic Discordance — Diabetics on Albuterol Alone (40 Patients)</strong>: 40 patients carrying an isolated diagnosis of diabetes are prescribed Albuterol (a short-acting beta-2 agonist) without any documented glycemic control agent. Beta-agonists stimulate glycogenolysis and lipolysis, worsening insulin resistance and exacerbating chronic hyperglycemia.</li>
        <li style='margin-bottom: 8px;'><strong>Unmanaged Vascular Risk — Hypertensives on Albuterol Alone (30 Patients)</strong>: 30 hypertensive patients receive bronchodilator therapy with zero anti-hypertensive medication. Beta-2 stimulation can induce tachycardia and mild inotropic spikes, further elevating vascular strain in unmedicated hypertensive patients.</li>
        <li style='margin-bottom: 8px;'><strong>Actionable Clinical Governance</strong>: Standardizing electronic health record clinical decision support (CDS) alerts and deploying nurse care managers to reconcile these <strong>111 discordant prescriptions</strong> eliminates iatrogenic harm and closes critical HEDIS quality gaps.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; line-height: 1.6;'>
        <em>To evaluate how these clinical risks intersect with patient contactability and recall bottlenecks, proceed to 
        <strong>Operations & Reach</strong> in the navigation rail.</em>
    </p>
    """,
    unsafe_allow_html=True
)
