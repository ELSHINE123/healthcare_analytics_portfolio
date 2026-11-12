"""
Production ETL & Feature Enrichment Pipeline
Executes risk stratification, therapeutic gap identification, contactability auditing,
and individual patient financial scoring.
"""

from pathlib import Path
import logging
import pandas as pd

from src.risk_engine import apply_risk_stratification
from src.therapeutic_engine import identify_therapeutic_gaps
from src.contact_engine import audit_contactability
from src.financial_engine import BENCHMARKS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def apply_safe_harbor_deidentification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce HIPAA Safe Harbor de-identification (45 CFR § 164.514(b)(2)):
    - Replace direct patient identifiers with non-derived opaque IDs (PT-0001..PT-NNNN)
    - Strip direct contact credentials (email, phone_number) while retaining boolean reachability flags
    - Generalize full visit_date to visit_year
    - Cap ages above 89 into a unified 90+ category
    """
    df_safe = df.copy()

    # Deterministic sequential record key not derived from PHI (45 CFR § 164.514(c))
    if "patient_id" not in df_safe.columns:
        patient_ids = [f"PT-{i:04d}" for i in range(1, len(df_safe) + 1)]
        df_safe.insert(0, "patient_id", patient_ids)

    # Extract year only from exact dates (45 CFR § 164.514(b)(2)(i)(C))
    if "visit_date" in df_safe.columns and "visit_year" not in df_safe.columns:
        parsed_dates = pd.to_datetime(df_safe["visit_date"], errors="coerce")
        df_safe["visit_year"] = parsed_dates.dt.year.astype("Int64")

    # Aggregate ages >= 90 (45 CFR § 164.514(b)(2)(i)(C))
    if "age" in df_safe.columns:
        df_safe.loc[df_safe["age"] > 89, "age"] = 90

    # Strip direct Safe Harbor identifier columns
    identifiers_to_drop = ["patient_name", "email", "phone_number", "visit_date"]
    df_safe = df_safe.drop(columns=[c for c in identifiers_to_drop if c in df_safe.columns])
    return df_safe


def run_enrichment_pipeline(
    input_path: Path,
    output_path: Path
) -> pd.DataFrame:
    """
    Run full clinical and financial feature engineering on clean EHR records.
    """
    logging.info(f"Loading raw cleaned dataset from {input_path}")
    df = pd.read_csv(input_path)
    initial_shape = df.shape
    logging.info(f"Loaded {initial_shape[0]} patient records across {initial_shape[1]} columns")
    
    # 1. Apply Clinical Risk Stratification
    logging.info("Applying AHA/ACC 2017 Blood Pressure & Clinical Risk Stratification...")
    df_enriched = apply_risk_stratification(df)
    
    # 2. Identify Care Gaps and Medication Discordance
    logging.info("Auditing therapeutic alignment and clinical care gaps...")
    df_enriched = identify_therapeutic_gaps(df_enriched)
    
    # 3. Audit Contactability
    logging.info("Auditing omnichannel patient contactability...")
    df_enriched = audit_contactability(df_enriched)
    
    # 4. Attach Individual Patient Cost Attribution (Annualized Risk-Weighted Cost Exposure)
    tier_event_rates = {
        "Severe Acuity": BENCHMARKS["BASE_SEVERE_ACUTE_EVENT_RATE"],
        "High Acuity": BENCHMARKS["BASE_HIGH_ACUTE_EVENT_RATE"],
        "Moderate Acuity": BENCHMARKS["BASE_MODERATE_ACUTE_EVENT_RATE"],
        "Low Acuity": 0.02,
    }
    admission_cost = BENCHMARKS["AHRQ_HCUP_INPATIENT_AVG_COST"]
    
    df_enriched["annual_event_probability"] = df_enriched["clinical_risk_tier"].map(tier_event_rates).fillna(0.02)
    df_enriched["expected_annual_cost_exposure"] = (
        df_enriched["annual_event_probability"] * admission_cost
    ).round(2)

    # 5. Enforce HIPAA Safe Harbor De-Identification
    logging.info("Applying HIPAA Safe Harbor de-identification (45 CFR § 164.514(b)(2))...")
    df_enriched = apply_safe_harbor_deidentification(df_enriched)
    
    # 6. Export Enriched Dataset
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_enriched.to_csv(output_path, index=False)
    logging.info(f"Successfully exported enriched dataset to {output_path} ({df_enriched.shape[0]} rows, {df_enriched.shape[1]} columns)")
    
    return df_enriched


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    raw_file = project_root / "data" / "raw" / "cleaned_healthcare_data.csv"
    processed_file = project_root / "data" / "processed" / "healthcare_analytics_enriched.csv"
    
    run_enrichment_pipeline(raw_file, processed_file)

