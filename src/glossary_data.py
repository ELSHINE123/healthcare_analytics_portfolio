# src/glossary_data.py
"""
Centralized Healthcare Analytics & Value-Based Care Terminology Repository
Author: Daniel Ademola Dongo
Provides definitions, categories, and project context for all domain acronyms
and healthcare economics concepts across the Metropolitan Health System suite.
"""

from typing import List, Dict, Any

GLOSSARY_TERMS: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. VALUE-BASED CARE & HEALTHCARE ECONOMICS
    # =========================================================================
    {
        "term": "ACO",
        "full_name": "Accountable Care Organization",
        "category": "Value-Based Care & Economics",
        "definition": "A legally formed network of doctors, hospitals, and healthcare providers who collaborate voluntarily to give coordinated, high-quality care to assigned Medicare patients, taking shared financial responsibility for the total cost and quality of care.",
        "project_context": "Metropolitan Health System operates as an Accountable Care Organization participating in CMS two-sided downside risk contracts, meaning hospital inpatient admissions directly reduce shared savings bonus pools.",
        "related_page": "0_executive_summary.py",
        "page_label": "Executive Summary"
    },
    {
        "term": "FFS",
        "full_name": "Fee-for-Service",
        "category": "Value-Based Care & Economics",
        "definition": "The legacy healthcare reimbursement model where providers are paid separately for each individual service rendered (office visits, tests, procedures, hospital stays), inherently rewarding volume of care over quality or prevention.",
        "project_context": "The portfolio analyzes Metropolitan Health's transition away from FFS (where inpatient bed occupancy generated hospital revenue) toward Value-Based Care (where avoidable bed days represent institutional losses).",
        "related_page": "home.py",
        "page_label": "Hospital Setting"
    },
    {
        "term": "VBC",
        "full_name": "Value-Based Care",
        "category": "Value-Based Care & Economics",
        "definition": "A healthcare delivery model in which providers (hospitals and physicians) are reimbursed based on patient health outcomes, clinical quality, and total cost efficiency rather than the number of services billed.",
        "project_context": "Forms the overarching financial framework of this study: proving that proactive clinical nurse outreach is financially accretive under value-based payment models.",
        "related_page": "home.py",
        "page_label": "Hospital Setting"
    },
    {
        "term": "Two-Sided Risk",
        "full_name": "Two-Sided Downside Financial Risk Contract",
        "category": "Value-Based Care & Economics",
        "definition": "A contractual agreement where an ACO can earn shared savings bonuses if medical expenditures fall below an actuarial benchmark, but must repay financial penalties to payers if patient expenditures exceed the benchmark.",
        "project_context": "Under two-sided risk contracts, Metropolitan Health is held directly liable for preventable admissions, turning acute hospitalization reduction into an urgent C-suite imperative.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "Capitation",
        "full_name": "Capitated Payment Model (PMPM)",
        "category": "Value-Based Care & Economics",
        "definition": "A fixed amount of money per patient per unit of time (typically Per Member Per Month - PMPM) paid in advance to the healthcare provider to deliver all necessary healthcare services for the enrolled population.",
        "project_context": "Under capitation, every avoidable emergency hospital admission is an unreimbursed operational cost that erodes the health system's operating margin.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "Shared Savings",
        "full_name": "CMS Medicare Shared Savings Program (MSSP)",
        "category": "Value-Based Care & Economics",
        "definition": "A federal incentive program that distributes a percentage of net medical cost reductions back to participating ACOs, provided the health system achieves predefined quality benchmark targets.",
        "project_context": "The ROI model demonstrates that a 20% admission reduction captures up to &dollar;420K in CMS quality shared savings bonuses for Metropolitan Health.",
        "related_page": "4_roi.py",
        "page_label": "Preventative ROI"
    },
    {
        "term": "HCUP",
        "full_name": "Healthcare Cost and Utilization Project",
        "category": "Value-Based Care & Economics",
        "definition": "A family of national healthcare databases and software tools developed through a Federal-State-Industry partnership sponsored by AHRQ, providing reliable cost-to-charge benchmarks for US hospital inpatient stays.",
        "project_context": "Supplies the standardized &dollar;12,500 national average cost benchmark used throughout the dashboard to quantify avoidable acute chronic disease inpatient admissions.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "AHRQ",
        "full_name": "Agency for Healthcare Research and Quality",
        "category": "Value-Based Care & Economics",
        "definition": "The lead Federal agency within the US Department of Health and Human Services (HHS) charged with improving the safety, quality, and economic efficiency of healthcare.",
        "project_context": "Provides the foundational Prevention Quality Indicators (PQIs) and cost benchmarks cited across the financial and executive reports.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "Self-Funding Model",
        "full_name": "Self-Funding Operational Architecture",
        "category": "Value-Based Care & Economics",
        "definition": "An operational program whose cost avoidance and revenue capture exceed its ongoing operating expenses, generating positive net operating margin without requiring external subsidy.",
        "project_context": "The 7.0 RN Care Management Unit costs &dollar;665K annually but generates &dollar;1.06M in economic value, operating at a 159% self-funding ratio (+&dollar;392K net margin).",
        "related_page": "4_roi.py",
        "page_label": "Preventative ROI"
    },

    # =========================================================================
    # 2. QUALITY, GOVERNANCE & REGULATORY MEASURES
    # =========================================================================
    {
        "term": "HEDIS",
        "full_name": "Healthcare Effectiveness Data and Information Set",
        "category": "Quality & Regulatory",
        "definition": "A widely used set of standardized performance measures maintained by NCQA, utilized by over 90% of US health plans to measure performance on critical dimensions of clinical care and service.",
        "project_context": "Metropolitan Health's quality performance is audited against three mandatory HEDIS measures: CBP (Blood Pressure), SPC (Cardiac Statin), and SUPD (Diabetes Statin).",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "NCQA",
        "full_name": "National Committee for Quality Assurance",
        "category": "Quality & Regulatory",
        "definition": "An independent 501(c)(3) non-profit organization in the United States that works to improve healthcare quality through evidence-based accreditation standards and HEDIS measure governance.",
        "project_context": "Governs the clinical specifications, benchmark percentiles, and annual reporting windows for the quality scorecards modeled in Act 3.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "CMS",
        "full_name": "Centers for Medicare & Medicaid Services",
        "category": "Quality & Regulatory",
        "definition": "The federal agency within the US Department of Health and Human Services that administers Medicare, Medicaid, the Children's Health Insurance Program (CHIP), and health insurance exchanges.",
        "project_context": "The primary regulatory body governing Metropolitan Health's ACO risk contracts, Star Ratings, and quality incentive disbursements.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "CMS Star Ratings",
        "full_name": "Medicare Advantage 5-Star Quality Rating System",
        "category": "Quality & Regulatory",
        "definition": "A quality rating system on a 1-to-5 star scale published annually by CMS to measure the quality of health and drug services received by consumers enrolled in Medicare Advantage plans.",
        "project_context": "Health systems achieving 4.0 or 5.0 Stars unlock a mandatory 5% Quality Bonus Payment on Medicare benchmark revenue; falling below 3.5 Stars triggers financial penalties and marketing freezes.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "QBP",
        "full_name": "Quality Bonus Payment",
        "category": "Quality & Regulatory",
        "definition": "Federal bonus payments awarded by CMS to Medicare Advantage plans that achieve 4.0 or more stars on the annual quality evaluation, typically equivalent to an extra 5% capitation revenue.",
        "project_context": "Modeled in Visual 9A and the Financial Bridge: recovering from 1-star statin deficits unlocks &dollar;68K to &dollar;136K in shared quality bonuses.",
        "related_page": "4_roi.py",
        "page_label": "Preventative ROI"
    },
    {
        "term": "HEDIS CBP",
        "full_name": "Controlling High Blood Pressure (Measure CBP)",
        "category": "Quality & Regulatory",
        "definition": "The percentage of members ages 18–85 with documented hypertension whose blood pressure was adequately controlled (<140/90 mmHg) during the measurement year.",
        "project_context": "Metropolitan Health outperforms the national benchmark on this measure (76.5% vs. 72.0% target), representing an operational success in primary clinic care.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "HEDIS SPC",
        "full_name": "Statin Therapy for Patients with Cardiovascular Disease (Measure SPC)",
        "category": "Quality & Regulatory",
        "definition": "The percentage of males 21–75 and females 40–75 with documented clinical atherosclerotic cardiovascular disease (ASCVD) who were actively dispensed at least one high- or moderate-intensity statin.",
        "project_context": "Identified as a critical regulatory deficit: Metropolitan Health achieves only 26.6% adherence against an 80.0% national benchmark (-53.4% deficit).",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "HEDIS SUPD",
        "full_name": "Statin Therapy for Patients with Diabetes (Measure SUPD)",
        "category": "Quality & Regulatory",
        "definition": "The percentage of patients ages 40–75 with diabetes who do not have clinical ASCVD and were dispensed at least one statin medication of moderate or high intensity during the measurement year.",
        "project_context": "Metropolitan Health sits in severe penalty territory with only 19.6% adherence against a 78.0% national benchmark (-58.4% deficit).",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },

    # =========================================================================
    # 3. CLINICAL GUIDELINES, BIOMETRICS & RISK STRATIFICATION
    # =========================================================================
    {
        "term": "ACC / AHA",
        "full_name": "American College of Cardiology / American Heart Association",
        "category": "Clinical & Biometrics",
        "definition": "The premier clinical cardiology organizations in the United States responsible for authoring the joint practice guidelines for hypertension, lipid management, and cardiovascular disease prevention.",
        "project_context": "The 2017 ACC/AHA High Blood Pressure Clinical Practice Guidelines form the clinical gold standard utilized in the suite to stratify biometric vitals.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "2017 ACC/AHA BP Guidelines",
        "full_name": "ACC/AHA Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure",
        "category": "Clinical & Biometrics",
        "definition": "The landmark clinical consensus that lowered hypertension thresholds: Normal (<120/<80), Elevated (120–129/<80), Stage 1 Hypertension (130–139/80–89), and Stage 2 Hypertension (≥140/≥90 mmHg).",
        "project_context": "Used to stratify Metropolitan Health's 983 patients, proving that 56.3% of chronic patients suffer from uncontrolled Stage 1 or Stage 2 hypertension.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "NCEP ATP III",
        "full_name": "National Cholesterol Education Program Adult Treatment Panel III",
        "category": "Clinical & Biometrics",
        "definition": "Evidence-based clinical guidelines establishing lipid thresholds: Desirable Total Cholesterol (<200 mg/dL), Borderline High (200–239 mg/dL), and High Risk (≥240 mg/dL).",
        "project_context": "Forms the horizontal axis threshold on Visual 1 (Bivariate Clinical Acuity Matrix) to identify compounded metabolic cardiovascular risk.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "SBP / DBP",
        "full_name": "Systolic Blood Pressure / Diastolic Blood Pressure",
        "category": "Clinical & Biometrics",
        "definition": "Systolic BP measures the pressure in blood vessels when the heart beats; Diastolic BP measures arterial pressure when the heart rests between beats, recorded in millimeters of mercury (mmHg).",
        "project_context": "Biometric measurements analyzed to flag cardiovascular instability, where SBP ≥140 mmHg designates Severe Acuity risk.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "Clinical Risk Tier",
        "full_name": "Four-Tier Population Health Risk Stratification",
        "category": "Clinical & Biometrics",
        "definition": "A predictive stratification framework categorizing patients into Low, Moderate, High, or Severe Acuity based on biometric vitals, multi-morbidity, and clinical guidelines.",
        "project_context": "Categorizes the panel into Low (164 pts, 16.7%), Moderate (266 pts, 27.1%), High (349 pts, 35.5%), and Severe (204 pts, 20.8%).",
        "related_page": "0_executive_summary.py",
        "page_label": "Executive Summary"
    },
    {
        "term": "Rising Risk",
        "full_name": "The 'Rising Risk' Patient Cohort",
        "category": "Clinical & Biometrics",
        "definition": "Patients currently in intermediate acuity (High Acuity) who, without proactive disease management, have a 40–50% probability of deteriorating into Severe Acuity within 12 to 18 months.",
        "project_context": "Metropolitan Health's 349 High Acuity patients represent this rising risk pool, prioritized for bi-weekly telephonic monitoring (1:100 caseload ratio).",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "HbA1c",
        "full_name": "Glycated Hemoglobin A1c",
        "category": "Clinical & Biometrics",
        "definition": "A standard laboratory blood test that measures average blood sugar levels over the past two to three months; values ≥6.5% indicate diabetes.",
        "project_context": "Referenced in clinical care coordination protocols for diabetic patients with uncontrolled glycemic trends.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },

    # =========================================================================
    # 4. PHARMACOLOGY & PATIENT SAFETY
    # =========================================================================
    {
        "term": "ACE Inhibitor (ACEI)",
        "full_name": "Angiotensin-Converting Enzyme Inhibitor (e.g., Lisinopril)",
        "category": "Pharmacology & Safety",
        "definition": "A class of medication that relaxes blood vessels by preventing an enzyme from producing angiotensin II, a substance that narrows blood vessels and raises blood pressure.",
        "project_context": "Used as guideline-directed first-line therapy for hypertension, but carries a dangerous contraindication when prescribed to asthmatic patients.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "SABA",
        "full_name": "Short-Acting Beta-2 Agonist (e.g., Albuterol)",
        "category": "Pharmacology & Safety",
        "definition": "A fast-acting bronchodilator inhaled medication used to quickly relieve sudden symptoms of asthma or chronic bronchitis by relaxing smooth muscles in the airways.",
        "project_context": "Audited in Visual 3: 40 diabetics and 30 hypertensives receive Albuterol alone with zero anti-glycemic or anti-hypertensive medication on record.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "Statin",
        "full_name": "HMG-CoA Reductase Inhibitor (e.g., Atorvastatin)",
        "category": "Pharmacology & Safety",
        "definition": "A class of lipid-lowering medications that reduce cardiovascular events and mortality by inhibiting the rate-limiting enzyme in hepatic cholesterol biosynthesis.",
        "project_context": "Mandated by ACC/AHA guidelines for all diabetics and cardiac patients; closing Metropolitan Health's 50% statin prescription deficit is the focus of Act 3.",
        "related_page": "3_financial.py",
        "page_label": "Financial Liability"
    },
    {
        "term": "Therapeutic Discordance",
        "full_name": "Pharmacotherapeutic Discordance",
        "category": "Pharmacology & Safety",
        "definition": "A clinical situation in which prescribed medications fail to address the patient's primary documented chronic condition or actively conflict with guideline-directed disease protocols.",
        "project_context": "Audited in the Medication Heatmap: isolates 111 patients on discordant medications across Metropolitan Health's network.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "Kinase II / Bradykinin",
        "full_name": "Bradykinin-Induced Bronchospasm (ACEI Contraindication)",
        "category": "Pharmacology & Safety",
        "definition": "Angiotensin-converting enzyme is identical to kinase II, which breaks down bradykinin. Inhibiting this enzyme leads to bradykinin accumulation in lung tissue, triggering acute bronchospasm and persistent cough.",
        "project_context": "Explains the severe pharmacologic risk for the 41 asthmatic patients prescribed Lisinopril, driving avoidable emergency department presentations.",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },

    # =========================================================================
    # 5. HEALTH INFORMATICS, OPERATIONS & WORKFORCE
    # =========================================================================
    {
        "term": "EHR",
        "full_name": "Electronic Health Record",
        "category": "Operations & Informatics",
        "definition": "A digital version of a patient's medical history maintained by healthcare providers over time, containing administrative and clinical data across diagnoses, vitals, labs, and medications.",
        "project_context": "The primary data foundation of this intelligence suite, linking 983 audited patient charts across inpatient and ambulatory sites.",
        "related_page": "0_executive_summary.py",
        "page_label": "Executive Summary"
    },
    {
        "term": "CDS",
        "full_name": "Clinical Decision Support Alerts",
        "category": "Operations & Informatics",
        "definition": "Health information technology systems designed to provide physicians and clinicians with person-specific, intelligently filtered clinical knowledge and alerts at the point of care.",
        "project_context": "The Phase 1 Roadmap recommendation: deploying EHR hard-stop CDS alerts to block contraindicated ACEI orders in asthmatics and prompt statin prescribing.",
        "related_page": "5_recommendations.py",
        "page_label": "Strategic Roadmap"
    },
    {
        "term": "FTE",
        "full_name": "Full-Time Equivalent Workforce Unit",
        "category": "Operations & Informatics",
        "definition": "A unit of measurement indicating the workload of an employed person in a way that makes workloads comparable across various contexts (typically 1.0 FTE = 40 hours per week).",
        "project_context": "The calibrated staffing model calculates that Metropolitan Health requires exactly 7.0 RN FTEs (&dollar;95K loaded cost) to manage the 553 high-acuity panel.",
        "related_page": "4_roi.py",
        "page_label": "Preventative ROI"
    },
    {
        "term": "CMSA",
        "full_name": "Case Management Society of America",
        "category": "Operations & Informatics",
        "definition": "The leading professional association providing practice standards, ethical guidelines, and evidence-based caseload staffing ratios for nurse case managers in the US.",
        "project_context": "Provides the industry staffing ratios utilized in Act 4: 1:60 nurse-to-patient ratio for Severe Acuity and 1:100 for High Acuity.",
        "related_page": "4_roi.py",
        "page_label": "Preventative ROI"
    },
    {
        "term": "ICD-10",
        "full_name": "International Classification of Diseases, 10th Revision",
        "category": "Operations & Informatics",
        "definition": "The global standard diagnostic classification code system adopted by the World Health Organization (WHO) and HIPAA for epidemiological tracking and clinical billing.",
        "project_context": "Used to formally identify patient cohort registries: Heart Disease (I25.1), Diabetes (E11.9), Hypertension (I10), and Asthma (J45.9).",
        "related_page": "1_clinical.py",
        "page_label": "Clinical Acuity"
    },
    {
        "term": "Surveillance Recency",
        "full_name": "Clinical Surveillance & Visit Recency Cadence",
        "category": "Operations & Informatics",
        "definition": "The interval elapsed since a patient's last recorded clinical encounter (in-person clinic visit or synchronous telehealth consultation).",
        "project_context": "Segmented into Active (<6m), Recall Due (6–12m), and Critically Overdue (>12m); audits show 206 patients (21.0%) have had no contact for >365 days.",
        "related_page": "2_operations.py",
        "page_label": "Operations & Reach"
    },
    {
        "term": "Data Provenance",
        "full_name": "Laboratory Measurement Provenance & Imputation",
        "category": "Operations & Informatics",
        "definition": "The documentation of the origins, history, and custody of data, distinguishing direct clinical biometric lab tests from imputed, synthetic, or estimated measurements.",
        "project_context": "Audits show 344 records (35.0%) contain imputed vitals, demonstrating hidden regulatory liability if clinical risk scores rely on unverified estimates.",
        "related_page": "2_operations.py",
        "page_label": "Operations & Reach"
    },
    {
        "term": "Clinical Ghost",
        "full_name": "Uncontactable Patient (Loss to Follow-up)",
        "category": "Operations & Informatics",
        "definition": "A high-risk patient carrying active chronic disease diagnoses who cannot be reached due to invalid or missing contact credentials in the EHR, typically resulting in emergency decompensation.",
        "project_context": "Isolates the 145 patients (14.8%) lacking working phone numbers and emails, requiring mandatory front-desk demographic stop-flags at clinic check-in.",
        "related_page": "2_operations.py",
        "page_label": "Operations & Reach"
    }
]

CATEGORIES: List[str] = [
    "All Categories",
    "Value-Based Care & Economics",
    "Quality & Regulatory",
    "Clinical & Biometrics",
    "Pharmacology & Safety",
    "Operations & Informatics"
]

