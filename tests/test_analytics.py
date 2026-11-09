"""
Comprehensive Unit Test Suite for Healthcare Analytics Engine
Tests AHA/ACC BP staging, clinical risk calculation, therapeutic discordance,
and AHRQ HCUP / CMS financial modeling formulas.
Supports both unittest (standard library) and pytest.
"""

import sys
from pathlib import Path
import unittest

# Ensure healthcare_analytics_portfolio root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from src.risk_engine import (
    classify_bp_stage,
    classify_cholesterol,
    calculate_clinical_risk_score,
    map_risk_tier,
    apply_risk_stratification
)
from src.therapeutic_engine import identify_therapeutic_gaps
from src.contact_engine import audit_contactability
from src.financial_engine import (
    calculate_cohort_financials,
    generate_sensitivity_matrix,
    BENCHMARKS
)


class TestHealthcareAnalytics(unittest.TestCase):

    # 1. Blood Pressure Staging Tests
    def test_bp_staging(self):
        cases = [
            (115, 75, "Normal"),
            (125, 75, "Elevated"),
            (130, 75, "Stage 1 Hypertension"),
            (125, 85, "Stage 1 Hypertension"),
            (140, 85, "Stage 2 Hypertension"),
            (130, 95, "Stage 2 Hypertension"),
            (190, 100, "Hypertensive Crisis"),
            (130, 125, "Hypertensive Crisis"),
        ]
        for systolic, diastolic, expected in cases:
            with self.subTest(systolic=systolic, diastolic=diastolic):
                self.assertEqual(classify_bp_stage(systolic, diastolic), expected)

    # 2. Cholesterol Tiering Tests
    def test_cholesterol_tiering(self):
        cases = [
            (180, "Desirable"),
            (200, "Borderline High"),
            (220, "Borderline High"),
            (245, "High"),
        ]
        for cholesterol, expected in cases:
            with self.subTest(cholesterol=cholesterol):
                self.assertEqual(classify_cholesterol(cholesterol), expected)

    # 3. Clinical Risk Score Calculation Tests
    def test_clinical_risk_score_calculation(self):
        # Low risk patient: young, normal BP, desirable cholesterol, no condition
        low_pt = pd.Series({
            "age": 28,
            "bp_stage": "Normal",
            "cholesterol_tier": "Desirable",
            "condition": "Unknown",
            "medication": "none"
        })
        score_low = calculate_clinical_risk_score(low_pt)
        self.assertLess(score_low, 35)
        self.assertEqual(map_risk_tier(score_low), "Low Acuity")

        # Severe risk patient: elderly, stage 2 HTN, borderline chol, heart disease, unmedicated
        severe_pt = pd.Series({
            "age": 68,
            "bp_stage": "Stage 2 Hypertension",
            "cholesterol_tier": "Borderline High",
            "condition": "heart disease",
            "medication": "none"
        })
        score_severe = calculate_clinical_risk_score(severe_pt)
        self.assertGreaterEqual(score_severe, 75)
        self.assertEqual(map_risk_tier(score_severe), "Severe Acuity")

    # 4. Therapeutic Gap Detection Tests
    def test_therapeutic_gap_detection(self):
        sample_df = pd.DataFrame([
            {"patient_name": "Alice", "condition": "diabetes", "medication": "none"},
            {"patient_name": "Bob", "condition": "diabetes", "medication": "albuterol"},
            {"patient_name": "Charlie", "condition": "hypertension", "medication": "albuterol"},
            {"patient_name": "Diana", "condition": "asthma", "medication": "lisinopril"},
            {"patient_name": "Evan", "condition": "hypertension", "medication": "lisinopril"},
        ])

        result = identify_therapeutic_gaps(sample_df)

        # Alice is unmedicated chronic
        self.assertTrue(bool(result.loc[result["patient_name"] == "Alice", "is_unmedicated_chronic"].values[0]))
        # Bob is diabetic with bronchodilator mismatch
        self.assertTrue(bool(result.loc[result["patient_name"] == "Bob", "is_therapeutic_discordance"].values[0]))
        # Charlie is hypertensive with bronchodilator mismatch
        self.assertTrue(bool(result.loc[result["patient_name"] == "Charlie", "is_therapeutic_discordance"].values[0]))
        # Diana is asthma on contraindicated ACE-inhibitor
        self.assertTrue(bool(result.loc[result["patient_name"] == "Diana", "is_therapeutic_discordance"].values[0]))
        # Evan is concordant
        self.assertFalse(bool(result.loc[result["patient_name"] == "Evan", "has_care_gap"].values[0]))

    # 5. Contactability Audit Tests
    def test_contactability_audit(self):
        sample_df = pd.DataFrame([
            {"patient_name": "P1", "email": "Unknown", "phone_number": "Unknown", "clinical_risk_tier": "Severe Acuity"},
            {"patient_name": "P2", "email": "p2@hospital.org", "phone_number": "Unknown", "clinical_risk_tier": "Low Acuity"},
            {"patient_name": "P3", "email": "p3@hospital.org", "phone_number": "555-1234", "clinical_risk_tier": "High Acuity"},
        ])

        result = audit_contactability(sample_df)
        self.assertTrue(bool(result.loc[result["patient_name"] == "P1", "is_uncontactable"].values[0]))
        self.assertTrue(bool(result.loc[result["patient_name"] == "P1", "critical_uncontactable_risk"].values[0]))
        self.assertEqual(result.loc[result["patient_name"] == "P2", "contact_status"].values[0], "Email Only")
        self.assertEqual(result.loc[result["patient_name"] == "P3", "contact_status"].values[0], "Omnichannel (Email & Phone)")

    # 6. Financial Simulation Model Tests
    def test_financial_simulation_model(self):
        dummy_enriched = pd.DataFrame({
            "clinical_risk_tier": ["Severe Acuity"] * 100 + ["High Acuity"] * 200 + ["Low Acuity"] * 300
        })

        res = calculate_cohort_financials(
            dummy_enriched,
            admission_cost=12500.0,
            program_cost_per_patient=500.0,
            admission_reduction_rate=0.25,
            enrollment_percentage=1.0
        )

        self.assertEqual(res["eligible_patients"], 300)
        self.assertEqual(res["enrolled_patients"], 300)
        self.assertEqual(res["total_program_investment"], 300 * 500.0)
        self.assertGreater(res["gross_savings"], res["total_program_investment"])
        self.assertGreater(res["net_savings"], 0)
        self.assertGreater(res["roi_percentage"], 0)
        self.assertGreater(res["benefit_cost_ratio"], 1.0)

    # 7. Sensitivity Matrix Structure Tests
    def test_sensitivity_matrix_structure(self):
        dummy_enriched = pd.DataFrame({
            "clinical_risk_tier": ["Severe Acuity"] * 50 + ["High Acuity"] * 100 + ["Moderate Acuity"] * 150
        })
        matrix = generate_sensitivity_matrix(dummy_enriched)
        self.assertEqual(len(matrix), 3)
        self.assertIn("Scenario", matrix.columns)
        self.assertIn("Net Savings", matrix.columns)
        self.assertIn("Benefit-Cost Ratio", matrix.columns)

    # 8. Glossary & Lexicon Data Integrity Tests
    def test_glossary_integrity(self):
        from src.glossary_data import GLOSSARY_TERMS, CATEGORIES
        self.assertGreaterEqual(len(GLOSSARY_TERMS), 20)
        self.assertIn("All Categories", CATEGORIES)
        required_keys = {"term", "full_name", "category", "definition", "project_context", "related_page"}
        for item in GLOSSARY_TERMS:
            self.assertTrue(required_keys.issubset(item.keys()), f"Missing keys in {item.get('term')}")
            self.assertIn(item["category"], CATEGORIES)
            self.assertGreater(len(item["definition"]), 10)
            self.assertGreater(len(item["project_context"]), 10)


if __name__ == "__main__":
    unittest.main()
