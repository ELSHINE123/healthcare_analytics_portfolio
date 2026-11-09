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
│   ├── export_engine.py       # Board memorandum and care gap CSV export generator
│   ├── risk_engine.py         # Bivariate acuity scoring and risk tier categorization
│   ├── therapeutic_engine.py  # HEDIS care gaps and contraindication identification
│   ├── contact_engine.py      # Contactability reach and surveillance audit engine
│   ├── financial_engine.py    # Actuarial cost modeling and staffing ROI equations
│   ├── glossary_data.py       # Centralized domain terminology repository
│   └── styles.py              # Unified scrollable card architecture & typography
├── data/
│   ├── raw/                   # Baseline clinical and demographic datasets
│   └── processed/             # healthcare_analytics_enriched.csv (983 enriched patient records)
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
git clone <repository-url>
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

Run the full programmatic test suite across all 8 pages:
```bash
python -c "
from streamlit.testing.v1 import AppTest
pages = ['app.py', 'home.py', 'pages/0_executive_summary.py', 'pages/1_clinical.py', 'pages/2_operations.py', 'pages/3_financial.py', 'pages/4_roi.py', 'pages/5_recommendations.py']
for p in pages:
    at = AppTest.from_file(p, default_timeout=30)
    at.run()
    assert not at.exception, f'Error in {p}: {at.exception}'
    print(f'PASS {p}')
print('ALL 8 PAGES PASSED!')
"
```

---

## 💼 Executive Features

* **Boardroom Presentation Mode**: Toggle in the sidebar expands the canvas to 95% width, scales up typography, elevates contrast, and locks the ROI model into recommended executive baselines for conference room projectors.
* **One-Click Certified Board Memorandum**: Download a complete, publication-ready executive briefing document (`.md`) directly from the sidebar, Executive Summary, or Strategic Roadmap.
* **Care Gap Audit Registry**: Export an actionable, audit-ready CSV roster of all 553 high-risk patients with assigned clinical pathways for frontline care management teams.

---
*Developed by Daniel Ademola Dongo | Healthcare Systems Architecture & Actuarial Intelligence.*

