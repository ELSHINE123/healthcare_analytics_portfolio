"""
Clinical Risk Stratification Engine
Applies American Heart Association (AHA/ACC) 2017 Blood Pressure guidelines,
NCEP ATP III Cholesterol classifications, and composite clinical risk scoring.
"""

from typing import Union
import pandas as pd
import numpy as np


def classify_bp_stage(systolic: Union[int, float], diastolic: Union[int, float]) -> str:
    """
    Classify blood pressure into clinical stages based on AHA/ACC 2017 Guidelines.
    
    Stages:
      - Normal: Systolic < 120 and Diastolic < 80
      - Elevated: Systolic 120-129 and Diastolic < 80
      - Stage 1 Hypertension: Systolic 130-139 or Diastolic 80-89
      - Stage 2 Hypertension: Systolic >= 140 or Diastolic >= 90
      - Hypertensive Crisis: Systolic > 180 or Diastolic > 120
    """
    if pd.isna(systolic) or pd.isna(diastolic):
        return "Unknown"
    
    sys_val = float(systolic)
    dia_val = float(diastolic)
    
    if sys_val > 180 or dia_val > 120:
        return "Hypertensive Crisis"
    if sys_val >= 140 or dia_val >= 90:
        return "Stage 2 Hypertension"
    if (130 <= sys_val <= 139) or (80 <= dia_val <= 89):
        return "Stage 1 Hypertension"
    if (120 <= sys_val <= 129) and dia_val < 80:
        return "Elevated"
    if sys_val < 120 and dia_val < 80:
        return "Normal"
    
    return "Stage 1 Hypertension"


def classify_cholesterol(cholesterol: Union[int, float]) -> str:
    """
    Classify serum cholesterol based on NCEP ATP III Clinical Guidelines:
      - Desirable: < 200 mg/dL
      - Borderline High: 200 - 239 mg/dL
      - High: >= 240 mg/dL
    """
    if pd.isna(cholesterol):
        return "Unknown"
    
    val = float(cholesterol)
    if val < 200:
        return "Desirable"
    if 200 <= val <= 239:
        return "Borderline High"
    return "High"


def calculate_clinical_risk_score(row: pd.Series) -> int:
    """
    Calculate an evidence-based composite clinical risk score (0 to 100).
    
    Scoring components:
      1. Age bracket (0 to 30 pts)
      2. Blood Pressure Staging (0 to 40 pts)
      3. Cholesterol Tier (0 to 15 pts)
      4. Diagnosed Pre-existing Conditions (0 to 30 pts)
      5. Unmedicated Chronic Status (+15 pts)
    """
    score = 0
    
    # 1. Age Factor
    age = row.get("age", 0)
    if pd.notna(age):
        age_val = float(age)
        if age_val >= 60:
            score += 30
        elif age_val >= 45:
            score += 20
        elif age_val >= 35:
            score += 10
        else:
            score += 5
            
    # 2. Blood Pressure Factor
    bp_stage = row.get("bp_stage", "")
    if bp_stage == "Hypertensive Crisis":
        score += 40
    elif bp_stage == "Stage 2 Hypertension":
        score += 35
    elif bp_stage == "Stage 1 Hypertension":
        score += 20
    elif bp_stage == "Elevated":
        score += 10
        
    # 3. Cholesterol Factor
    chol_tier = row.get("cholesterol_tier", "")
    if chol_tier == "High":
        score += 15
    elif chol_tier == "Borderline High":
        score += 10
        
    # 4. Chronic Illness Multiplier
    condition = str(row.get("condition", "")).strip().lower()
    if condition == "heart disease":
        score += 25
    elif condition == "diabetes":
        score += 20
    elif condition == "hypertension":
        score += 15
    elif condition == "asthma":
        score += 10
        
    # 5. Unmedicated Chronic Penalty
    med = str(row.get("medication", "")).strip().lower()
    if condition in ["heart disease", "diabetes", "hypertension"] and med == "none":
        score += 15
        
    return min(score, 100)


def map_risk_tier(score: int) -> str:
    """
    Map composite clinical risk score to executive triage tiers.
    """
    if score >= 75:
        return "Severe Acuity"
    if score >= 55:
        return "High Acuity"
    if score >= 35:
        return "Moderate Acuity"
    return "Low Acuity"


def apply_risk_stratification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich input DataFrame with clinical risk classification attributes.
    """
    df_out = df.copy()
    
    df_out["bp_stage"] = [
        classify_bp_stage(s, d) for s, d in zip(df_out["systolic_bp"], df_out["diastolic_bp"])
    ]
    df_out["cholesterol_tier"] = [classify_cholesterol(c) for c in df_out["cholesterol"]]
    
    df_out["clinical_risk_score"] = df_out.apply(calculate_clinical_risk_score, axis=1)
    df_out["clinical_risk_tier"] = df_out["clinical_risk_score"].apply(map_risk_tier)
    
    return df_out

