"""
Financial Exposure and Preventative Care ROI Simulation Engine
Anchored to AHRQ HCUP Statistical Briefs (#278 / #286) and CMS Chronic Care Management schedules.
"""

from typing import Dict, Any
import pandas as pd


# Documented Federal Benchmarks
BENCHMARKS = {
    "AHRQ_HCUP_INPATIENT_AVG_COST": 12500.0,      # AHRQ HCUP Statistical Brief #278 / #286 blended chronic inpatient stay
    "CMS_ANNUAL_CCM_PROGRAM_COST": 750.0,         # CMS CPT 99490 Chronic Care Management (~$62.50/month)
    "BASE_SEVERE_ACUTE_EVENT_RATE": 0.28,         # Annual probability of avoidable acute ED/inpatient visit (Severe)
    "BASE_HIGH_ACUTE_EVENT_RATE": 0.18,           # Annual probability of avoidable acute ED/inpatient visit (High)
    "BASE_MODERATE_ACUTE_EVENT_RATE": 0.08,       # Annual probability of avoidable acute ED/inpatient visit (Moderate)
    "BASE_ADMISSION_REDUCTION_RATE": 0.25,        # 25% relative risk reduction through proactive care management
}


def calculate_cohort_financials(
    df: pd.DataFrame,
    admission_cost: float = BENCHMARKS["AHRQ_HCUP_INPATIENT_AVG_COST"],
    program_cost_per_patient: float = BENCHMARKS["CMS_ANNUAL_CCM_PROGRAM_COST"],
    admission_reduction_rate: float = BENCHMARKS["BASE_ADMISSION_REDUCTION_RATE"],
    enrollment_percentage: float = 1.0,
    target_tiers: list = None
) -> Dict[str, Any]:
    """
    Simulate financial exposure, program operational cost, gross savings, and net ROI.
    
    Parameters:
      - df: Enriched DataFrame with 'clinical_risk_tier'
      - admission_cost: Cost per acute avoidable inpatient stay (default $12,500)
      - program_cost_per_patient: Annual cost to enroll patient in care management (default $750)
      - admission_reduction_rate: Expected percentage reduction in acute admissions (default 25%)
      - enrollment_percentage: Portion of eligible cohort successfully engaged (0.0 to 1.0)
      - target_tiers: Risk tiers targeted for intervention (default: High & Severe Acuity)
    """
    if target_tiers is None:
        target_tiers = ["Severe Acuity", "High Acuity"]
        
    tier_counts = df["clinical_risk_tier"].value_counts().to_dict()
    severe_count = tier_counts.get("Severe Acuity", 0)
    high_count = tier_counts.get("High Acuity", 0)
    moderate_count = tier_counts.get("Moderate Acuity", 0)
    low_count = tier_counts.get("Low Acuity", 0)
    
    # 1. Total baseline acute event volume (without intervention)
    expected_severe_events = severe_count * BENCHMARKS["BASE_SEVERE_ACUTE_EVENT_RATE"]
    expected_high_events = high_count * BENCHMARKS["BASE_HIGH_ACUTE_EVENT_RATE"]
    expected_moderate_events = moderate_count * BENCHMARKS["BASE_MODERATE_ACUTE_EVENT_RATE"]
    total_expected_events = expected_severe_events + expected_high_events + expected_moderate_events
    
    # Total baseline hospital cost exposure
    total_cost_exposure = total_expected_events * admission_cost
    
    # 2. Targeted Intervention Cohort
    target_df = df[df["clinical_risk_tier"].isin(target_tiers)]
    eligible_patients = len(target_df)
    enrolled_patients = int(eligible_patients * enrollment_percentage)
    
    # Events within targeted cohort
    targeted_expected_events = (
        (severe_count if "Severe Acuity" in target_tiers else 0) * BENCHMARKS["BASE_SEVERE_ACUTE_EVENT_RATE"] +
        (high_count if "High Acuity" in target_tiers else 0) * BENCHMARKS["BASE_HIGH_ACUTE_EVENT_RATE"]
    )
    enrolled_events = targeted_expected_events * enrollment_percentage
    
    # 3. Prevented Events & Financial Savings
    prevented_admissions = enrolled_events * admission_reduction_rate
    gross_savings = prevented_admissions * admission_cost
    total_program_cost = enrolled_patients * program_cost_per_patient
    net_savings = gross_savings - total_program_cost
    roi_percentage = (net_savings / total_program_cost * 100.0) if total_program_cost > 0 else 0.0
    benefit_cost_ratio = (gross_savings / total_program_cost) if total_program_cost > 0 else 0.0
    
    return {
        "eligible_patients": eligible_patients,
        "enrolled_patients": enrolled_patients,
        "total_baseline_cost_exposure": round(total_cost_exposure, 2),
        "total_program_investment": round(total_program_cost, 2),
        "prevented_admissions": round(prevented_admissions, 1),
        "gross_savings": round(gross_savings, 2),
        "net_savings": round(net_savings, 2),
        "roi_percentage": round(roi_percentage, 1),
        "benefit_cost_ratio": round(benefit_cost_ratio, 2),
        "severe_patients": severe_count,
        "high_patients": high_count,
        "moderate_patients": moderate_count,
        "low_patients": low_count,
    }


def generate_sensitivity_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a 3-tier sensitivity model: Conservative vs. Base vs. Optimistic.
    """
    scenarios = [
        {
            "Scenario": "Conservative (Pessimistic)",
            "Admission Cost ($)": 9500.0,
            "Reduction Rate (%)": "15%",
            "Program Cost / Pt ($)": 900.0,
            "params": (9500.0, 900.0, 0.15, 0.80),
        },
        {
            "Scenario": "Base Case (HCUP / CMS)",
            "Admission Cost ($)": 12500.0,
            "Reduction Rate (%)": "25%",
            "Program Cost / Pt ($)": 750.0,
            "params": (12500.0, 750.0, 0.25, 1.00),
        },
        {
            "Scenario": "Optimistic (High Engagement)",
            "Admission Cost ($)": 15000.0,
            "Reduction Rate (%)": "35%",
            "Program Cost / Pt ($)": 600.0,
            "params": (15000.0, 600.0, 0.35, 1.00),
        },
    ]
    
    results = []
    for sc in scenarios:
        adm, prog, red, enr = sc["params"]
        res = calculate_cohort_financials(
            df,
            admission_cost=adm,
            program_cost_per_patient=prog,
            admission_reduction_rate=red,
            enrollment_percentage=enr
        )
        results.append({
            "Scenario": sc["Scenario"],
            "Admission Benchmark": f"${adm:,.0f}",
            "Intervention Efficacy": sc["Reduction Rate (%)"],
            "Program Investment": f"${res['total_program_investment']:,.0f}",
            "Prevented Admissions": f"{res['prevented_admissions']:.1f}",
            "Gross Savings": f"${res['gross_savings']:,.0f}",
            "Net Savings": f"${res['net_savings']:,.0f}",
            "Benefit-Cost Ratio": f"{res['benefit_cost_ratio']:.2f}x",
            "ROI": f"{res['roi_percentage']:.1f}%",
        })
        
    return pd.DataFrame(results)

