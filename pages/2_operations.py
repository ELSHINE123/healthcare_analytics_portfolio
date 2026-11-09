# pages/2_operations.py
"""
Act 2: Operations & Reach: Contactability, Surveillance & Data Integrity
Author: Daniel Ademola Dongo
Setting: Metropolitan Health Integrated Network (ACO)
Narrative Flow Style: Interactive Visuals with Integrated Narrative Storytelling
Answers Questions 2, 3, and 8
"""

import streamlit as st
import pandas as pd
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
# 2. PAGE HEADER & OPERATIONAL FRAMING
# ==============================================================================
st.title("Operational Reach, Surveillance & Data Quality")
st.caption("Patient Contactability Channels, Longitudinal Surveillance Cadence & Clinical Data Quality")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    Even the most sophisticated clinical risk stratification models fail if ambulatory operations cannot reach 
    the vulnerable patient. In population health management, healthcare systems face three silent operational barriers: 
    **contactability blind spots** that cause outreach campaigns to fail, **surveillance decay** where high-risk patients 
    go unmonitored for over a year, and **imputation bias** in EHR records that creates false clinical complacency.
    
    This analytical module audits Metropolitan Health System's ambulatory outreach infrastructure across all **983 chronic patients**, 
    uncovering critical digital blind spots and establishing the evidentiary foundation for targeted nurse recall workflows.
    """
)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. PATIENT CONTACTABILITY CHANNELS & LOSS-TO-FOLLOW-UP
# ==============================================================================
st.header("1. Patient Contactability Channels & Digital Blind Spots")

if not df.empty:
    with st.container(border=True):
        v4_col1, v4_col2 = st.columns(2, gap="large")

        with v4_col1:
            # Visual 4A: Contactability Reach Donut
            channel_order = ["Omnichannel (Email & Phone)", "Phone Only", "Email Only", "Uncontactable (Loss to Follow-up)"]
            channel_counts = df["contact_status"].value_counts().reindex(channel_order, fill_value=0).reset_index()
            channel_counts.columns = ["Channel", "Patients"]

            channel_palette = ["#10B981", "#3B82F6", "#64748B", "#DC2626"]

            fig_v4a = go.Figure(data=[go.Pie(
                labels=channel_counts["Channel"],
                values=channel_counts["Patients"],
                hole=0.55,
                domain=dict(y=[0.24, 1.0]),
                marker=dict(colors=channel_palette),
                textinfo="percent",
                textposition="inside",
                insidetextfont=dict(color="#FFFFFF", size=13, family="Be Vietnam Pro"),
                hovertemplate="<b>%{label}</b><br>Patients: %{value:,}<br>Share: %{percent}<extra></extra>"
            )])
            fig_v4a.update_layout(
                title="<b>Population Reach by Contact Channel</b>",
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="top", y=0.12, xanchor="center", x=0.5, font=dict(family="Be Vietnam Pro", size=11.5)),
                height=390,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v4a, width="stretch")

        with v4_col2:
            # Visual 4B: Acuity Breakdown of the 145 Uncontactable Patients (Slim Columns)
            uncontactable_df = df[df["uncontactable"] == True].copy()
            uncontactable_acuity = uncontactable_df["clinical_risk_tier"].value_counts().reindex(
                ["Severe Acuity", "High Acuity", "Moderate Acuity", "Low Acuity"], fill_value=0
            ).reset_index()
            uncontactable_acuity.columns = ["Tier", "Patients"]

            fig_v4b = go.Figure(data=[go.Bar(
                x=uncontactable_acuity["Tier"],
                y=uncontactable_acuity["Patients"],
                text=uncontactable_acuity["Patients"],
                textposition="outside",
                width=0.42,
                marker=dict(color=["#DC2626", "#F59E0B", "#3B82F6", "#10B981"]),
                hovertemplate="<b>%{x}</b><br>Uncontactable Patients: %{y:,}<extra></extra>"
            )])
            fig_v4b.update_layout(
                title="<b>Acuity Severity of Uncontactable Cohort (N = 145)</b>",
                margin=dict(l=20, r=20, t=50, b=40),
                height=370,
                bargap=0.45,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Number of Patients", range=[0, 65]),
                xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v4b, width="stretch")

# Narrative Directly Under Visual 4
st.markdown(
    """
    **Contactability Audit Findings & Digital Blind Spots**: Standard healthcare outreach strategies assume that patients can be contacted 
    through automated telephone dialers or patient portal messaging. The left chart audits the actual reachability of 
    Metropolitan Health's chronic cohort: while **375 patients (38.1%)** possess verified omnichannel contact data (both phone and email), 
    and another 463 patients have at least one channel, **145 patients (14.8%) are completely uncontactable**. 
    These individuals lack both a valid phone number and a working email in the EHR, representing an operational dead end.
    
    The right chart reveals the severe clinical stakes of this operational gap: **85 of the 145 uncontactable patients (58.6%)** 
    sit in the High Acuity (53 patients) or Severe Acuity (32 patients) tiers. These individuals suffer from uncontrolled Stage 2 
    hypertension and dyslipidemia without any operational pathway for automated clinical recall. When chronic patients become 
    unreachable 'clinical ghosts,' they do not receive preventative care; instead, they decompensate in the community and present 
    directly to the Emergency Department, triggering catastrophic &dollar;12,500 inpatient stays.
    
    **Operational Prescription**: Automated recall campaigns must never be deployed blindly to this cohort. Clinic reception 
    workflows must be configured with a mandatory EHR demographic stop-flag at clinic check-in, requiring front-desk staff 
    to capture and verify contact credentials whenever an uncontactable patient presents for any service.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. SURVEILLANCE DELAYS & THE OVERDUE COHORT (SIDE-BY-SIDE)
# ==============================================================================
st.header("2. Longitudinal Surveillance Cadence & Overdue Patient Recall")

if not df.empty:
    with st.container(border=True):
        v5_col1, v5_col2 = st.columns(2, gap="large")

        with v5_col1:
            # Visual 5A: Surveillance Recency x Clinical Acuity Heatmap
            recall_ct = pd.crosstab(
                df["clinical_risk_tier"],
                df["surveillance_status"]
            )
            # Reorder rows Severe -> Low, columns Active -> Overdue
            row_order = [r for r in ["Severe Acuity", "High Acuity", "Moderate Acuity", "Low Acuity"] if r in recall_ct.index]
            col_order = [c for c in ["Active Surveillance (<6m)", "Recall Due (6-12m)", "Critically Overdue (>12m)"] if c in recall_ct.columns]
            recall_ct_clean = recall_ct.reindex(index=row_order, columns=col_order, fill_value=0)

            fig_v5a = px.imshow(
                recall_ct_clean,
                text_auto=True,
                labels=dict(x="Surveillance Recency", y="Acuity Tier", color="Patients"),
                x=["Active (<6m)", "Recall Due (6-12m)", "Overdue (>12m)"],
                y=recall_ct_clean.index,
                color_continuous_scale="Blues",
                title="<b>Surveillance Recency by Clinical Acuity Matrix</b>"
            )
            fig_v5a.update_traces(
                hovertemplate="<b>Acuity:</b> %{y}<br><b>Surveillance:</b> %{x}<br><b>Patients:</b> %{z:,}<extra></extra>",
                textfont=dict(size=14, family="Be Vietnam Pro")
            )
            fig_v5a.update_layout(
                margin=dict(l=20, r=20, t=50, b=30),
                height=370,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
                yaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
                coloraxis_showscale=False,
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v5a, width="stretch")

        with v5_col2:
            # Visual 5B: Chronic Disease Breakdown of Overdue Patients (Slim Horizontal Columns)
            overdue_df = df[df["surveillance_status"] == "Critically Overdue (>12m)"].copy()
            cond_overdue = overdue_df[overdue_df["condition"] != "Unknown"]["condition"].str.title().value_counts().reset_index()
            cond_overdue.columns = ["Condition", "Patients"]
            cond_overdue = cond_overdue.sort_values("Patients", ascending=True)

            fig_v5b = px.bar(
                cond_overdue,
                x="Patients",
                y="Condition",
                orientation="h",
                text="Patients",
                title="<b>Critically Overdue Patients (>12m) by Registry</b>",
                color="Patients",
                color_continuous_scale="Blues"
            )
            fig_v5b.update_traces(
                textposition="outside",
                width=0.45,
                hovertemplate="<b>%{y}</b><br>Overdue Patients: %{x:,}<extra></extra>"
            )
            fig_v5b.update_layout(
                margin=dict(l=10, r=40, t=50, b=10),
                showlegend=False,
                coloraxis_showscale=False,
                height=370,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Number of Patients", range=[0, 60]),
                yaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title=""),
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v5b, width="stretch")

# Narrative Directly Under Visual 5
st.markdown(
    """
    **Surveillance Cadence & Overdue Recall Priorities**: Chronic disease management requires continuous clinical surveillance. 
    Under standard NCQA guidelines, patients with hypertension, coronary disease, or diabetes should complete a clinical 
    evaluation at least every 6 months to titrate pharmacotherapy and assess organ function. 
    
    The surveillance heatmap on the left reveals a dangerous operational decay: **206 patients (21.0% of the entire panel)** 
    have had no recorded in-person or telehealth contact with Metropolitan Health for over 365 days. 
    Critically, **114 of these overdue patients sit in the High Acuity (74 patients) or Severe Acuity (40 patients)** tiers. 
    These patients are living with unmonitored cardiovascular and metabolic deterioration, representing immediate actuarial liability.
    
    The right chart identifies the disease registries most heavily impacted by surveillance loss: diabetic patients (48 patients) 
    and heart disease patients (45 patients) form the bulk of the critically overdue cohort. 
    In diabetic patients, unmonitored glycemic levels lead to silent microvascular neuropathy; in heart disease patients, unmonitored 
    ischemia leads to sudden acute myocardial infarction. 
    
    **Care Management Priority**: Metropolitan Health's 7.0 RN FTE care coordination unit must immediately triage the **40 Severe Acuity 
    overdue patients** for rapid telephonic recall, reserving scheduled in-clinic appointment slots to re-establish clinical surveillance.
    """
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. CLINICAL LABORATORY DATA QUALITY & AUDIT PROVENANCE (SIDE-BY-SIDE)
# ==============================================================================
st.header("3. Clinical Laboratory Data Quality & Verification Auditing")

if not df.empty:
    with st.container(border=True):
        v6_col1, v6_col2 = st.columns(2, gap="large")

        with v6_col1:
            # Visual 6A: Data Provenance Donut
            prov_counts = df["data_provenance"].value_counts().reindex([
                "Pure Clinical Measurement",
                "Cholesterol Only Imputed",
                "Blood Pressure Only Imputed",
                "Both BP & Chol Imputed"
            ], fill_value=0).reset_index()
            prov_counts.columns = ["Provenance", "Patients"]

            prov_palette = ["#10B981", "#3B82F6", "#F59E0B", "#DC2626"]

            fig_v6a = go.Figure(data=[go.Pie(
                labels=prov_counts["Provenance"],
                values=prov_counts["Patients"],
                hole=0.55,
                domain=dict(y=[0.24, 1.0]),
                marker=dict(colors=prov_palette),
                textinfo="percent",
                textposition="inside",
                insidetextfont=dict(color="#FFFFFF", size=13, family="Be Vietnam Pro"),
                hovertemplate="<b>%{label}</b><br>Patients: %{value:,}<br>Share: %{percent}<extra></extra>"
            )])
            fig_v6a.update_layout(
                title=dict(text="<b>Clinical Laboratory Measurement Provenance</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
                margin=dict(l=10, r=10, t=85, b=10),
                legend=dict(orientation="h", yanchor="top", y=0.12, xanchor="center", x=0.5, font=dict(family="Be Vietnam Pro", size=11.5)),
                height=390,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v6a, width="stretch")

        with v6_col2:
            # Visual 6B: Acuity Distribution by Data Provenance (Pure vs. Imputed Grouped Bar)
            df_prov_plot = df.copy()
            df_prov_plot["imputed_label"] = df_prov_plot["has_imputed_vitals"].map({False: "Verified Direct Lab (N=639)", True: "Unverified / Imputed (N=344)"})
            
            prov_tier_ct = df_prov_plot.groupby(["clinical_risk_tier", "imputed_label"]).size().reset_index(name="Patients")
            prov_tier_ct["clinical_risk_tier"] = pd.Categorical(
                prov_tier_ct["clinical_risk_tier"], 
                categories=["Low Acuity", "Moderate Acuity", "High Acuity", "Severe Acuity"], 
                ordered=True
            )
            prov_tier_ct = prov_tier_ct.sort_values(["clinical_risk_tier", "imputed_label"])

            fig_v6b = px.bar(
                prov_tier_ct,
                x="clinical_risk_tier",
                y="Patients",
                color="imputed_label",
                barmode="group",
                text="Patients",
                color_discrete_map={
                    "Verified Direct Lab (N=639)": "#2563EB",
                    "Unverified / Imputed (N=344)": "#F59E0B"
                },
                labels={"clinical_risk_tier": "Clinical Acuity Tier", "Patients": "Patient Count", "imputed_label": "Record Status"}
            )
            fig_v6b.update_traces(
                textposition="outside",
                width=0.35,
                hovertemplate="<b>%{x}</b><br><b>Status:</b> %{fullData.name}<br><b>Patients:</b> %{y}<extra></extra>"
            )
            fig_v6b.update_layout(
                title=dict(text="<b>Clinical Acuity: Verified Direct Labs vs. Unverified Records</b>", x=0.5, y=0.96, xanchor="center", yanchor="top"),
                margin=dict(l=20, r=20, t=55, b=85),
                height=410,
                bargap=0.35,
                bargroupgap=0.15,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True, gridcolor="#E2E8F0", showline=True, linecolor="#CBD5E1", linewidth=1.2, title="Number of Patients", range=[0, 290]),
                xaxis=dict(showline=True, linecolor="#CBD5E1", linewidth=1.2, title="", tickfont=dict(size=12, family="Be Vietnam Pro")),
                legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, title="", font=dict(family="Be Vietnam Pro", size=11.5)),
                font=dict(family="Be Vietnam Pro, sans-serif")
            )
            st.plotly_chart(fig_v6b, width="stretch")

# Narrative Directly Under Visual 6
st.markdown(
    """
    <p style='color: #334155; font-size: 14.5px; line-height: 1.65; text-align: justify;'>
        <strong>Laboratory Data Quality & Regulatory Audit Risks</strong>: In healthcare analytics, handling missing biometric data with statistical 
        estimation is a common data convention. However, when applied to clinical decision support and regulatory 
        auditing, <strong>unverified or modeled lab records introduce significant clinical distortion</strong>:
    </p>
    <ul style='margin-top: 6px; margin-bottom: 12px; padding-left: 22px; line-height: 1.65; color: #334155;'>
        <li style='margin-bottom: 8px;'><strong>Cohort Exposure</strong>: Across Metropolitan Health's 983 audited patients, <strong>344 records (35.0%) contain at least one unverified vital sign</strong>: 191 patients have estimated cholesterol, 125 have estimated blood pressure, and 28 have both vitals estimated. Only 639 patients (65.0%) possess complete, verified direct laboratory measurements.</li>
        <li style='margin-bottom: 8px;'><strong>The Estimation Fallacy</strong>: Approximating missing blood pressure or cholesterol with group averages artificially compresses biological variance. Patients with unrecorded, dangerously elevated systolic pressure (e.g. 160+ mmHg) or severe familial hypercholesterolemia are pulled down to cohort averages (125 mmHg and 190 mg/dL), causing them to be falsely classified as Moderate or Low Acuity.</li>
        <li style='margin-bottom: 8px;'><strong>Regulatory Audit Risk</strong>: Under federal CMS Medicare Advantage Risk Adjustment Data Validation (RADV) audits, estimated vitals cannot be submitted for clinical risk adjustment or HEDIS quality bonus claims. If an ACO relies on unverified vitals to calculate shared-savings benchmarks, it faces severe financial clawbacks during retrospective audits.</li>
        <li style='margin-bottom: 8px;'><strong>Clinical Governance Mandate</strong>: Metropolitan Health System must enforce strict <strong>data provenance tracking</strong> in its clinical workflows. Care management systems must tag unverified records with a confirmatory draw order, directing nursing staff to collect physical lab panels and in-person biometric vitals before finalizing clinical risk tiers.</li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='color: #64748B; font-size: 13px; line-height: 1.6;'>
        <em>To evaluate the balance sheet impact of these clinical and operational gaps, proceed to 
        <strong>Financial Stakes</strong> in the navigation rail.</em>
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
                EXECUTIVE TOUR &bull; ACT 3 OF 4
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">
                Financial Stakes: Inpatient Liability & Quality Bonuses
            </div>
            <div style="font-size: 12.5px; color: #64748B;">
                Simulate avoidable inpatient expenses, 80/20 Pareto exposure, and CMS HEDIS Star Rating bonuses.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
with tour_col2:
    try:
        st.page_link(
            "pages/3_financial.py",
            label="Proceed to Financial Stakes →",
            icon="💰",
            use_container_width=True
        )
    except Exception:
        if st.button("Proceed to Financial Stakes →", key="tour_ops_btn", use_container_width=True):
            st.switch_page("pages/3_financial.py")

