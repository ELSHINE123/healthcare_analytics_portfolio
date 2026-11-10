# Technical Architecture & Data Science Documentation
## Metropolitan Health System — Value-Based Healthcare Analytics Suite

**Author**: Daniel Ademola Dongo  
**Role**: Principal Systems Architect & Lead Healthcare Data Analyst  
**Institutional Setting**: Metropolitan Health System (Integrated Healthcare Delivery Network & Accountable Care Organization)  
**Contractual Context**: CMS Two-Sided Shared-Savings Medicare Advantage / NextGen ACO Risk Contracts  
**Target Deployment**: Streamlit Community Cloud (Python 3.11+, Streamlit 1.36+)

---

## 1. Executive Project Mission & Problem Statement

Under historical Fee-for-Service (FFS) reimbursement, Metropolitan Health System generated revenue by billing for acute hospital admissions, diagnostic imaging, and specialty encounters. In recent performance years, the network entered two-sided risk-bearing agreements with federal and commercial payers (Medicare Advantage, NextGen ACO). 

Under capitation and shared savings, economic incentives inverted:
1. **Inpatient Utilization Liability**: The health system is penalized dollar-for-dollar for avoidable acute hospitalizations exceeding benchmark targets.
2. **HEDIS Quality Metric Gatekeeping**: Millions in annual shared-savings bonuses are tied to NCQA HEDIS quality star ratings (specifically Controlling Blood Pressure, Statin Therapy for Diabetes, and Cardiovascular Disease).
3. **The Data Gap**: While the hospital's EHR captured rich clinical vitals and medication dispense logs for 983 chronic disease patients, leadership lacked an integrated actuarial intelligence engine to stratify patient acuity, detect unmedicated cohorts, identify prescribing contraindications, and simulate preventative care ROI.

This codebase delivers that enterprise decision support engine.

---

## 2. Clinical Guidelines & Mathematical Methodologies

### A. Bivariate Clinical Acuity Stratification Engine
The clinical engine (`src/risk_engine.py` & `pages/1_clinical.py`) evaluates each patient across two orthogonal physiologic risk dimensions:
* **Systolic Blood Pressure (ACC/AHA 2017 Guidelines)**:
  * Normal: $<120\text{ mmHg}$
  * Elevated: $120\text{--}129\text{ mmHg}$
  * Stage 1 Hypertension: $130\text{--}139\text{ mmHg}$
  * Stage 2 Hypertension: $\ge 140\text{ mmHg}$
* **Total Serum Cholesterol (NCEP ATP III Guidelines)**:
  * Desirable: $<200\text{ mg/dL}$
  * Borderline High: $200\text{--}239\text{ mg/dL}$
  * High Risk: $\ge 240\text{ mg/dL}$

#### Composite Clinical Risk Score ($0\text{--}100$)
$$
\text{Risk Score} = 0.50 \times \left(\frac{\text{SBP} - 100}{60}\right) \times 100 + 0.35 \times \left(\frac{\text{Chol} - 140}{120}\right) \times 100 + 0.15 \times \left(\frac{\text{Age} - 18}{62}\right) \times 100
$$
*Constrained to the interval $[0, 100]$.*

#### Acuity Tier Categorization:
* **Severe Acuity** ($\text{Score} \ge 65$ or $\text{SBP} \ge 140\text{ mmHg}$ or $\text{Chol} \ge 240\text{ mg/dL}$ with compounding disease): Critical cardiovascular/stroke risk.
* **High Acuity** ($50 \le \text{Score} < 65$ or $\text{SBP} \ge 130\text{ mmHg}$): Rising risk cohort.
* **Moderate Acuity** ($35 \le \text{Score} < 50$): Early Stage 1 / Elevated vitals.
* **Low Acuity** ($\text{Score} < 35$): Controlled vitals, standard annual recall.

### B. Pharmacotherapy Care Gap & Discordance Engine
Cross-references primary ICD diagnosis against active pharmacotherapy dispense history:
1. **Unmedicated Chronic Disease**: Patients with diagnosed Hypertension, Diabetes, or Heart Disease with zero active prescribed medications ($N = 109$).
2. **Therapeutic Discordance / Ineffective Therapy**:
   * Diabetic patients on antihypertensive monotherapy without glycemic control.
   * Hypertensive patients with $\text{SBP} \ge 140$ on non-titrated monotherapy.
3. **Safety Contraindication Audit**: Identifies high-risk prescribing discords, specifically **41 asthmatic patients prescribed Lisinopril** (an ACE-inhibitor known to induce severe bradykinin-mediated bronchospasm and persistent cough).

### C. Longitudinal Operational Surveillance Cadence
NCQA guidelines mandate that chronic disease patients complete clinical evaluation at least every 180 days:
* **Active Surveillance**: $<180\text{ days}$ since last encounter.
* **Recall Due**: $180\text{--}365\text{ days}$ elapsed.
* **Critically Overdue**: $>365\text{ days}$ elapsed (Loss-to-Follow-up liability, $N = 206$).
* **Reachability Blind Spots**: 145 patients lack both a verified telephone number and email in the EHR.

### D. Actuarial Inpatient Liability & ROI Financial Model
* **Avoidable Admission Benchmark**: $\$12,500$ per acute stay (derived from national AHRQ Healthcare Cost and Utilization Project - HCUP).
* **Baseline Inpatient Exposure**:
  $$
  \text{Expected Admissions} = (N_{\text{Severe}} \times P_{\text{adm, severe}}) + (N_{\text{High}} \times P_{\text{adm, high}})
  $$
  $$
  = (204 \times 0.65) + (349 \times 0.35) = 132.6 + 122.2 = 254.8\text{ Admissions/Year}
  $$
  $$
  \text{Gross Exposure} = 254.8 \times \$12,500 = \$3,185,000\text{ / Year}
  $$
* **Workforce Caseload Sizing (CMSA / NCQA Standards)**:
  * Severe Acuity ratio: $1\text{ RN FTE} : 60\text{ Patients} \implies 204 / 60 = 3.40\text{ FTEs}$
  * High Acuity ratio: $1\text{ RN FTE} : 100\text{ Patients} \implies 349 / 100 = 3.49\text{ FTEs}$
  * Total Dedicated Workforce: $\approx 7.0\text{ Dedicated RN FTEs}$
* **Economic Unit Return**:
  * Staffing Cost: $7.0\text{ FTEs} \times \$95,000 = \$665,000$
  * Averted Admissions ($20\%$ reduction target): $254.8 \times 0.20 = 50.96 \approx 51\text{ Admissions}$
  * Inpatient Cost Savings: $50.96 \times \$12,500 = \$637,000$
  * CMS HEDIS Quality Bonus Opportunity: $+\$420,000$
  * **Total Value Created**: $\$1,057,000$
  * **Net Operating Margin**: $\$1,057,000 - \$665,000 = +\$392,000$
  * **Self-Funding Ratio**: $\frac{\$1,057,000}{\$665,000} \approx 159\%$ (Payback period: $4.8\text{ months}$)

---

## 3. Codebase Directory Structure & Component Inventory

```text
healthcare_analytics_portfolio/
├── app.py                       # Master entrypoint, st.navigation routing, boardroom mode
├── home.py                      # Institutional overview, ACO background, interactive persona guide
├── pages/
│   ├── 0_executive_summary.py   # High-level C-suite briefing, KPI strip, acuity donuts, export center
│   ├── 1_clinical.py            # Bivariate acuity scatter plot, side-by-side diagnostic inspector, discordance heatmap
│   ├── 2_operations.py          # Omnichannel contactability reach, 180-day surveillance matrix, data provenance
│   ├── 3_financial.py           # AHRQ HCUP inpatient simulation, statin gap revenue, HEDIS penalty scorecard
│   ├── 4_roi.py                 # Preventative care sensitivity heatmap, 7.0 RN FTE staffing model, economic coverage
│   ├── 5_recommendations.py     # 4 Pillars of transformation, 180-day execution roadmap, boardroom directives
│   └── 6_glossary.py            # Searchable healthcare glossary with certified clinical/actuarial definitions
├── src/
│   ├── styles.py                # Visual card container CSS, non-clipping Plotly layouts, compact executive typography
│   ├── export_engine.py         # Markdown board memorandum and care gap CSV roster generator
│   └── glossary_data.py         # Structured dictionary of 40+ healthcare acronyms and formulas
├── data/
│   └── processed/
│       └── healthcare_analytics_enriched.csv # 983 enriched, audited clinical patient records
├── tests/
│   ├── test_clinical_risk.py    # Unit tests validating risk scoring and acuity tier assignments
│   ├── test_financial_roi.py    # Unit tests validating HCUP benchmarks, FTE sizing, and ROI math
│   └── test_operations.py       # Unit tests validating surveillance decay and reachability logic
├── .streamlit/
│   └── config.toml              # Streamlit server and theme configurations
├── requirements.txt             # Locked Python package dependencies
├── README.md                    # Public GitHub repository overview and quick start guide
└── docs/
    ├── TECHNICAL_DOCUMENTATION.md # This document
    └── USER_PERSONA_GUIDE.md     # Stakeholder navigation guide tailored by executive persona
```

---

## 4. Front-End & Visual Architecture

### A. Non-Clipping Executive Visual Container CSS (`src/styles.py`)
All interactive visual cards render with uniform elevation:
* **Background**: `#FFFFFF` with `1px solid #E2E8F0` border and `12px` border radius.
* **Overflow Handling**: Strict `overflow: visible !important;` prevents internal scrollbars and ensures SVG labels, axis titles, and colorbars are 100% visible.
* **Aspect Ratio**: Heatmaps (`px.imshow`) enforce `aspect="auto"` to stretch dynamically to 100% of the parent card width, eliminating squashed square cells and angled axis labels.
* **Side-by-Side Symmetrical Acuity Grid**:
  * Scatter plot visual and diagnostic inspector card maintain exact pixel height parity (`538px`).
  * The main visual is allocated a wide `2.1 : 1` column ratio (`~67.7%` visual width), providing ample dispersion space for 983 data points.
  * The Plotly legend is anchored in container space (`yref="container", y=0.88`), cleanly separated from the title (`y=0.98`) to prevent text overlap.

### B. Compact Typography Scale
* `h1`: Compacted to $22\text{px}$ bold with $0\text{px}$ top margin to maximize navigable space.
* `caption`: $13\text{px}$ slate (`#64748B`) with tight spacing.
* Top container padding: Reduced from Streamlit's default $6\text{rem}$ down to $1.4\text{rem}$, immediately recovering over $100\text{px}$ of vertical space.

---

## 5. Verification & Testing Framework

The suite incorporates two tiers of automated validation:
1. **Algorithmic Unit Tests** (`python -m unittest discover -s healthcare_analytics_portfolio/tests`):
   * Validates risk score bounds ($0 \le \text{Score} \le 100$).
   * Tests acuity tier classification against ACC/AHA cutoffs.
   * Asserts actuarial calculations: baseline hospitalizations ($254.8$), FTE ratios ($6.89$), and margin payback.
2. **Headless Integration UI Tests (`streamlit.testing.v1.AppTest`)**:
   * Programmatically executes all 8 application pages in headless mode.
   * Verifies dynamic selectboxes (e.g. `Diabetes` + `Severe Acuity`) and resets.
   * Asserts zero runtime exceptions (`assert len(at.exception) == 0`).

