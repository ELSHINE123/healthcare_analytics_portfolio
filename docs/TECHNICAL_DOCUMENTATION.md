# Technical Architecture & Data Science Documentation
## Metropolitan Health System — Value-Based Healthcare Analytics Suite

**Author**: Daniel Ademola Dongo  
**Role**: Principal Systems Architect & Lead Healthcare Data Analyst  
**Institutional Setting**: Metropolitan Health System (Integrated Healthcare Delivery Network & Accountable Care Organization)  
**Contractual Context**: CMS Two-Sided Shared-Savings Medicare Advantage / NextGen ACO Risk Contracts  
**Target Deployment**: Streamlit Community Cloud & Streamlit in Snowflake (Python 3.11+, Streamlit 1.36+)

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

### E. HIPAA Safe Harbor De-Identification Protocol (`45 CFR § 164.514(b)(2)`)
Before persisting processed data or surfacing row-level records in interactive triage and CSV exports, `apply_safe_harbor_deidentification()` (`src/pipeline.py`) enforces structural de-identification across all 983 patient rows:
1. **Opaque Record Key (`45 CFR § 164.514(c)`)**: Replaces `patient_name` with non-derived sequential identifiers (`PT-0001` through `PT-0983`) across `data/processed/healthcare_analytics_enriched.csv`, the Clinical Worklist & Snapshot Chart Inspector (`pages/1_clinical.py`), and `generate_care_gap_roster_csv()` (`src/export_engine.py`).
2. **Contact Credential Stripping**: Drops `email` and `phone_number` strings while preserving `missing_email`, `missing_phone`, `uncontactable`, and `contact_status` outreach indicators computed by `src/contact_engine.py` (with graceful boolean fallback when raw credential columns are absent).
3. **Date Generalization**: Converts exact `visit_date` values into year-only `visit_year` while retaining relative elapsed intervals (`days_since_visit`).
4. **Age 90+ Aggregation**: Enforces `age > 89 -> 90` capping (`max age = 70` in current cohort).

---

## 3. Codebase Directory Structure & Component Inventory

```text
healthcare_analytics_portfolio/
├── app.py                       # Master entrypoint, st.navigation routing, boardroom mode
├── home.py                      # Institutional overview, ACO background, Safe Harbor notice, persona guide
├── pages/
│   ├── 0_executive_summary.py   # High-level C-suite briefing, KPI strip, acuity donuts, export center
│   ├── 1_clinical.py            # Bivariate acuity scatter plot, diagnostic inspector (PT-XXXX), discordance heatmap
│   ├── 2_operations.py          # Omnichannel contactability reach, 180-day surveillance matrix, data provenance
│   ├── 3_financial.py           # AHRQ HCUP inpatient simulation, statin gap revenue, HEDIS penalty scorecard
│   ├── 4_roi.py                 # Preventative care sensitivity heatmap, 7.0 RN FTE staffing model, economic coverage
│   ├── 5_recommendations.py     # 4 Pillars of transformation, 180-day execution roadmap, boardroom directives
│   └── 6_glossary.py            # Searchable healthcare glossary with certified clinical/actuarial definitions
├── src/
│   ├── pipeline.py              # Production ETL orchestration & HIPAA Safe Harbor de-identification
│   ├── risk_engine.py           # Bivariate clinical risk scoring and acuity tier categorization
│   ├── therapeutic_engine.py    # HEDIS medication gap and safety contraindication detection
│   ├── contact_engine.py        # Contactability reachability audit (supports raw & Safe Harbor schemas)
│   ├── financial_engine.py      # Actuarial inpatient liability, RN caseload, and ROI matrix modeling
│   ├── styles.py                # Unified sticky topbar, collapsed-sidebar expansion, mobile breakpoints & card CSS
│   ├── export_engine.py         # ReportLab PDF board memorandum and de-identified CSV roster generator
│   └── glossary_data.py         # Structured dictionary of healthcare acronyms and formulas
├── data/
│   └── processed/
│       └── healthcare_analytics_enriched.csv # 983 Safe Harbor de-identified clinical records (PT-0001..PT-0983)
├── tests/
│   └── test_analytics.py        # Unit tests covering scoring, therapeutic gaps, contactability, ROI & Safe Harbor
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

### A. Unified Sticky Top Bar & Cross-Runtime Widescreen Expansion (`app.py` & `src/styles.py`)
* **Single Flush Top Bar (`y = 0`)**: The native Streamlit `<header data-testid="stHeader">` is dissolved into a transparent click-through overlay (`pointer-events: none` on the wrapper, `pointer-events: auto` on controls), while Google Fonts are loaded via `@import` inside `<style>` so invisible style containers do not introduce a top gap.
* **Cross-Runtime Sidebar Collapse Expansion**: Targets both modern Streamlit selectors (`[data-testid="stMain"]`, `[data-testid="stMainBlockContainer"]`, flex parent `StyledMainContent`) and legacy Streamlit/Snowflake selectors (`.main`, `[data-testid="stAppViewBlockContainer"]`), explicitly forcing `width: 0; min-width: 0; max-width: 0; flex: 0 0 0` on collapsed sidebar states (`[aria-expanded="false"]`, `:has([data-testid="collapsedControl"])`, `:has([data-testid="stExpandSidebarButton"])`).
* **Sticky Positioning Integrity**: Root horizontal overflow is constrained via `overflow-x: clip` rather than `overflow-x: hidden` so ancestor containers never trap or disable `position: sticky` snapping. When collapsed, `.sticky-page-header` adds `4.25rem` left padding on desktop (`54px`/`52px` on mobile) to clear the `>>` reopen toggle.

### B. Non-Clipping Visual Cards & Mobile Breakpoints (`src/styles.py`)
All interactive visual cards render with uniform elevation:
* **Background**: `#FFFFFF` with `1px solid #E2E8F0` border and `12px` border radius.
* **Overflow Handling**: Strict `overflow: visible !important;` prevents internal scrollbars on desktop and ensures SVG labels, axis titles, and colorbars are 100% visible; mobile breakpoints (`<= 768px`, `<= 480px`) enable `-webkit-overflow-scrolling: touch` on charts/tables and adjust container padding (`0.75rem` / `0.5rem`) and header font sizing (`15px` / `13.5px`).
* **Aspect Ratio**: Heatmaps (`px.imshow`) enforce `aspect="auto"` to stretch dynamically to 100% of the parent card width, eliminating squashed square cells and angled axis labels.

---

## 5. Verification & Testing Framework

The suite incorporates two tiers of validation:
1. **Algorithmic & Compliance Unit Tests** (`python -m unittest discover -s tests` — **9 tests** in `tests/test_analytics.py`):
   * Validates risk score bounds ($0 \le \text{Score} \le 100$) and acuity tier classification against ACC/AHA cutoffs.
   * Tests therapeutic discordance, asthma/Lisinopril contraindication flagging, contactability channel categorization, actuarial ROI payback, and `test_safe_harbor_deidentification` (`patient_id`, `visit_year`, age `<= 90`, and stripped identifier columns).
2. **Playwright Headless DOM & Viewport Verification**:
   * Verifies expanded/collapsed desktop (`1440×900`) and mobile (`375×812`) rendering, `stSidebar` collapse to `0px`, full `1440px` main canvas expansion, sticky header snapping at `y = 0` after scrolling, and multi-page navigation across modules with zero runtime exceptions.

