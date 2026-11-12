"""
Operational Outreach and Contactability Audit Engine
Identifies data completeness gaps in patient contact channels and calculates
loss-to-follow-up risks for high-acuity cohorts.
"""

import pandas as pd


def audit_contactability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich DataFrame with patient contactability and loss-to-follow-up risk flags.
    """
    df_out = df.copy()
    
    if "email" in df_out.columns and "phone_number" in df_out.columns:
        email_clean = df_out["email"].astype(str).str.strip().str.lower()
        phone_clean = df_out["phone_number"].astype(str).str.strip().str.lower()

        # Missing / Unknown flags
        df_out["missing_email"] = email_clean.isin(["unknown", "none", "", "nan"])
        df_out["missing_phone"] = phone_clean.isin(["unknown", "none", "", "nan"])
    else:
        # Support Safe Harbor de-identified datasets where raw credentials are stripped
        df_out["missing_email"] = df_out.get("missing_email", pd.Series(True, index=df_out.index)).astype(bool)
        df_out["missing_phone"] = df_out.get("missing_phone", pd.Series(True, index=df_out.index)).astype(bool)
    
    # Uncontactable completely (neither email nor phone valid)
    df_out["is_uncontactable"] = df_out["missing_email"] & df_out["missing_phone"]
    
    # Contact channel status category
    contact_status = []
    for e_miss, p_miss in zip(df_out["missing_email"], df_out["missing_phone"]):
        if not e_miss and not p_miss:
            contact_status.append("Omnichannel (Email & Phone)")
        elif not e_miss:
            contact_status.append("Email Only")
        elif not p_miss:
            contact_status.append("Phone Only")
        else:
            contact_status.append("Uncontactable (Loss to Follow-up)")
            
    df_out["contact_status"] = contact_status
    
    # Flag severe/high acuity patients who cannot be contacted
    if "clinical_risk_tier" in df_out.columns:
        high_risk_mask = df_out["clinical_risk_tier"].isin(["High Acuity", "Severe Acuity"])
        df_out["critical_uncontactable_risk"] = high_risk_mask & df_out["is_uncontactable"]
    else:
        df_out["critical_uncontactable_risk"] = False
        
    return df_out

