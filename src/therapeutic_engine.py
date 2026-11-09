"""
Therapeutic Gap and Clinical Discordance Engine
Audits condition-to-medication alignment, identifies unmedicated chronic patients,
and flags high-risk therapeutic discordance.
"""

import pandas as pd


def identify_therapeutic_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich DataFrame with medication adherence and clinical discordance flags.
    
    Clinical Rules:
      1. Unmedicated Chronic: Diagnosed with Hypertension, Heart Disease, or Diabetes,
         but medication is 'none'.
      2. Inappropriate / Discordant Therapy:
         - Diabetes on Albuterol without glycemic/metformin therapy.
         - Hypertension on Albuterol without anti-hypertensive (lisinopril/atorvastatin).
         - Asthma on Lisinopril (known ACE-inhibitor contraindication causing bronchospasm).
    """
    df_out = df.copy()
    
    cond_clean = df_out["condition"].astype(str).str.strip().str.lower()
    med_clean = df_out["medication"].astype(str).str.strip().str.lower()
    
    # 1. Unmedicated chronic illness
    chronic_conditions = ["heart disease", "diabetes", "hypertension"]
    df_out["is_unmedicated_chronic"] = (cond_clean.isin(chronic_conditions)) & (med_clean == "none")
    
    # 2. Therapeutic discordance flag
    is_diabetic_mismatch = (cond_clean == "diabetes") & (med_clean == "albuterol")
    is_htn_mismatch = (cond_clean == "hypertension") & (med_clean == "albuterol")
    is_asthma_contraindication = (cond_clean == "asthma") & (med_clean == "lisinopril")
    
    df_out["is_therapeutic_discordance"] = (
        is_diabetic_mismatch | is_htn_mismatch | is_asthma_contraindication
    )
    
    # Discordance classification detail
    discordance_types = []
    for c, m in zip(cond_clean, med_clean):
        if c in chronic_conditions and m == "none":
            discordance_types.append("Zero Medication Prescribed")
        elif c == "diabetes" and m == "albuterol":
            discordance_types.append("Diabetic on Bronchodilator Alone")
        elif c == "hypertension" and m == "albuterol":
            discordance_types.append("Hypertensive on Bronchodilator Alone")
        elif c == "asthma" and m == "lisinopril":
            discordance_types.append("Asthma on ACE-Inhibitor (Contraindicated)")
        elif m == "none":
            discordance_types.append("No Active Medication")
        else:
            discordance_types.append("Guideline Concordant / Under Observation")
            
    df_out["care_gap_category"] = discordance_types
    df_out["has_care_gap"] = df_out["is_unmedicated_chronic"] | df_out["is_therapeutic_discordance"]
    
    return df_out

