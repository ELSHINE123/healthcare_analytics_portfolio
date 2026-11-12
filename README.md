# Metropolitan Health System — Value-Based Healthcare Intelligence Suite

**Author**: Daniel Ademola Dongo  
**Institutional Setting**: Metropolitan Health System (Midwestern Integrated Healthcare Delivery Network & Accountable Care Organization)  
**Contractual Context**: CMS Two-Sided Shared-Savings Medicare Advantage / NextGen ACO Risk Contracts  
**Audited Cohort**: 983 Chronic Disease Patients across Heart Disease, Diabetes, Hypertension, and Asthma Registries  

---

## 🏛️ Executive Summary & Context

Metropolitan Health System operates under two-sided downside risk contracts where avoidable inpatient hospitalizations directly erode institutional operating margins. This clinical intelligence application translates clinical Electronic Health Record (EHR) data, biometric vital signs, and pharmacotherapy records into actionable C-suite strategy.

### Core Actuarial & Clinical Findings
* **High-Acuity Risk Concentration**: **56.3% of the panel (553 patients)** sit in the High or Severe Acuity tiers. Under the 80/20 Pareto rule, the top 20% highest-risk patients drive 82% of all avoidable inpatient expenses.
* **Inpatient Cost Exposure**: Under baseline utilization rates (65% in Severe, 35% in High Acuity), this high-risk cohort generates **254.8 acute hospitalizations annually**, representing **$3.18M in gross annual financial liability** (at the $12,500 AHRQ HCUP benchmark).
* **Clinical Care Gaps**:
  * **109 patients** with formal ICD diagnoses receive zero prescribed medication.
  * **111 patients** receive discordant or contraindicated medications (including 41 asthmatics prescribed Lisinopril).
  * Severe HEDIS statin therapy compliance gaps in diabetes (45.4% vs. 65.0% benchmark) and cardiovascular disease (53.4% vs. 80.0% benchmark).
* **Operational Blind Spots**: **145 patients (14.8%)** lack valid contact details, and **462 patients (47.0%)** exceed 180 days since their last clinical visit.
* **The Self-Funding Solution**: Deploying a dedicated **7.0 RN FTE Ambulatory Care Management Unit** ($665K annual staffing investment) achieves a 20% admission reduction, averting 51 acute hospitalizations and generating **$1.06M in total economic value** ($637K cost avoidance + $420K CMS quality shared-savings bonus), returning **+$392K in net operating margin (159% self-funding ratio)**.

---

## 🛠️ Tech Stack Audit & Bill of Materials

| Component Category | Selected Technology | Reasoning & Architectural Fit |
| :--- | :--- | :--- |
| **Language & Runtime** | Python 3.11+ / 3.13 | High-performance numeric and data manipulation runtime. |
| **Frontend Framework** | Streamlit 1.30+ | Rapid, interactive data applications with native session state management. |
| **Data Visualization** | Plotly 5.18+ | Responsive, publication-grade interactive charts (SVG/WebGL) with hover tooltips. |
| **Data Processing** | Pandas 2.0+ & NumPy 1.24+ | Vectorized tabular operations and data enrichment pipelines. |
| **Testing Suite** | Pytest & Streamlit AppTest | End-to-end integration and programmatic UI execution verification. |
| **Typography & Theme** | Google Fonts (*Be Vietnam Pro*) | Editorial executive styling with high-contrast steel-slate navigation rails. |

---

## 📂 Application Architecture & Navigation

The suite is organized into 8 sequential modules adhering to executive governance principles:

```text
healthcare_analytics_portfolio/
├── app.py                     # Master entrypoint, steel-slate navigation rail, presentation mode
├── home.py                    # Module 1: Institutional setting, ACO transition & decision framework
├── pages/
│   ├── 0_executive_summary.py # Module 2: High-level KPI strip, acuity donuts & export center
│   ├── 1_clinical.py          # Module 3: Blood pressure vs. lipid matrix & discordance heatmap
│   ├── 2_operations.py        # Module 4: Contactability reach, surveillance recency & lab provenance
│   ├── 3_financial.py         # Module 5: AHRQ HCUP cost simulation & HEDIS quality penalty scorecard
│   ├── 4_roi.py               # Module 6: Preventative care ROI sensitivity & 7.0 RN staffing model
│   ├── 5_recommendations.py   # Module 7: 4 Pillars of transformation & 180-day executive roadmap
│   └── 6_glossary.py          # Module 8: Searchable healthcare acronym & value-based care lexicon
├── src/
│   ├── pipeline.py            # Production ETL, risk scoring & HIPAA Safe Harbor de-identification
│   ├── export_engine.py       # ReportLab PDF board memorandum and de-identified CSV roster export
│   ├── risk_engine.py         # Bivariate acuity scoring and risk tier categorization
│   ├── therapeutic_engine.py  # HEDIS care gaps and contraindication identification
│   ├── contact_engine.py      # Contactability reach and surveillance audit engine
│   ├── financial_engine.py    # Actuarial cost modeling and staffing ROI equations
│   ├── glossary_data.py       # Centralized domain terminology repository
│   └── styles.py              # Unified flush top bar, mobile breakpoints & card container CSS
├── data/
│   ├── raw/                   # Baseline clinical and demographic datasets
│   └── processed/             # healthcare_analytics_enriched.csv (983 Safe Harbor de-identified records)
├── tests/                     # Unit and integration test suites
├── requirements.txt           # Verified project dependencies
└── .env.example               # Environment variable templates
```

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.10+ installed
* Git installed

### 1. Clone & Set Up Virtual Environment
```bash
# Clone the repository
git clone https://github.com/ELSHINE123/healthcare_analytics_portfolio.git
cd healthcare_analytics_portfolio

# Create and activate a virtual environment
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the unit test suite (including clinical scoring, ROI math, and HIPAA Safe Harbor de-identification checks):
```bash
python -m unittest discover -s tests
```

Or validate syntax compilation across all Python modules:
```bash
python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('**/*.py', recursive=True)]; print('ALL COMPILED')"
```

---

## 📚 Complete Project Documentation & Guides

For deep technical methodologies and persona-specific review workflows, consult the project documentation dossier in `docs/`:

1. **[Technical Architecture & Data Science Documentation](docs/TECHNICAL_DOCUMENTATION.md)**:
   * Comprehensive data pipeline, mathematical formulas, and actuarial modeling equations.
   * Clinical guideline cutoffs (ACC/AHA 2017 Blood Pressure, NCEP ATP III Lipids).
   * Pharmacotherapy care gap classification and Lisinopril-Asthma safety contraindication rules.
   * Front-end visual card CSS architecture, Plotly container scaling, and test suites.

2. **[Executive Stakeholder User Guide (by Persona)](docs/USER_PERSONA_GUIDE.md)**:
   * Curated review pathways and key decisions for **Chief Medical Officers (CMO)**, **Chief Operating Officers (COO)**, **Chief Financial Officers (CFO)**, and **Nurse Care Managers / Data Analysts**.

---

## ☁️ Deployment Guide (Streamlit Community Cloud & Snowflake)

This portfolio is structured for **Streamlit Community Cloud** and **Streamlit in Snowflake (SiS)** with cross-runtime collapsed-sidebar widescreen expansion and mobile breakpoints (`<= 768px`, `<= 480px`):

### 1. Push to GitHub
Ensure all code and processed data files are committed to your GitHub repository:
```bash
git add .
git commit -m "feat: complete value-based healthcare analytics suite"
git push origin main
```

### 2. Connect to Streamlit Community Cloud
1. Navigate to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"** (or **"Create app"**).
3. Select your repository: `<your-username>/healthcare_analytics_portfolio`.
4. Set the **Branch** to `main` (or `master`).
5. Set the **Main file path** to `app.py`.
6. Click **"Deploy!"**.

*(For **Streamlit in Snowflake**, upload the repository contents including `app.py`, `home.py`, `pages/`, `src/`, and `data/processed/healthcare_analytics_enriched.csv`, and configure `app.py` as the entrypoint.)*

### 3. Verify Deployment
* Streamlit Cloud will install dependencies automatically from `requirements.txt`.
* The multi-page navigation rail (`app.py`), presentation mode, interactive workbenches, and CSV/PDF export centers will be immediately live on your custom public URL.

---

## 🔒 Data Governance & HIPAA Safe Harbor Compliance

To ensure regulatory integrity under **45 CFR § 164.514(b)(2)**, all processed clinical tables, interactive triage views, and CSV exports enforce structural Safe Harbor de-identification (`apply_safe_harbor_deidentification` in `src/pipeline.py`):
* Direct identifiers (`patient_name`, `email`, `phone_number`, and exact `visit_date`) are stripped from the processed dataset and UI exports.
* Records are keyed by non-derived opaque IDs (`PT-0001`–`PT-0983`), binary outreach reachability flags (`missing_email`, `missing_phone`, `uncontactable`, `contact_status`), year-level timestamps (`visit_year`, `days_since_visit`), and a `90+` age cap.

---

## 💼 Executive Features

* **Boardroom Presentation Mode**: Toggle in the sidebar expands the canvas to 100% widescreen width, scales up typography, and elevates contrast for conference room projectors.
* **One-Click Certified Board Memorandum (PDF)**: Download a complete, publication-ready vector PDF executive briefing directly from the sidebar (`app.py`).
* **De-Identified Care Gap Audit Registry (CSV)**: Export an actionable, audit-ready CSV roster of high-risk/care-gap records keyed by `patient_id` (`PT-0001`–`PT-0983`) for frontline care management workflows.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by Daniel Ademola Dongo | Healthcare Systems Architecture & Actuarial Intelligence.*

