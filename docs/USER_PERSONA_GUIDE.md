# Executive Stakeholder User Guide
## Metropolitan Health System — Value-Based Healthcare Analytics Suite

**Author**: Daniel Ademola Dongo  
**System Target**: Enterprise Healthcare Decision Support & Actuarial Governance  
**Audience**: Healthcare Executives, Clinical Leaders, Operations Directors, and Population Health Analysts  

---

## 🧭 How to Use This Intelligence Suite

This application is engineered as a **5-Act narrative workflow** supporting data-driven clinical and financial decision-making under value-based risk contracts. To maximize efficiency, this user guide organizes navigation pathways tailored to specific leadership personas.

Select your executive role below to view your curated review pathway, key visual indicators, and actionable decisions:

---

### 🩺 Persona 1: Chief Medical Officer (CMO) & Clinical Quality Director

> **Core Mandate**: Protect patient safety, eliminate unmedicated disease cohorts, resolve prescribing contraindications, and achieve HEDIS 4.0+ Star Quality ratings.

#### Recommended 3-Step Navigation Pathway:
1. **Act 1: Clinical Risk & Safety (`pages/1_clinical.py`)**:
   * **Bivariate Acuity Distribution Visual**: Filter by **Chronic Disease Registry** (e.g., *Heart Disease*, *Diabetes*) and **Clinical Acuity Tier** (*Severe Acuity*). Observe the red/amber patient clusters exceeding AHA Stage 2 thresholds ($\ge 140\text{ mmHg}$) and NCEP lipid cutoffs ($\ge 240\text{ mg/dL}$).
   * **Dynamic Diagnostic Inspector**: Read the auto-generated clinical narrative on the right side panel. Review mean vitals, patient count, and care gaps for the live cohort.
   * **Medication Discordance & Safety Heatmap**: Scroll down to Section 3 to inspect the 5×5 prescribing matrix. Note the **41 asthmatic patients prescribed Lisinopril** (a life-threatening bronchospasm contraindication).
2. **Act 1: Individual Patient EHR Snapshot**:
   * Open the EHR Ambulatory Clinical Chart expander. Select high-acuity patients to inspect their real-time vitals, pharmacotherapy dispense status, and assigned care pod.
3. **Act 3: Quality Scorecard Audit (`pages/3_financial.py`)**:
   * Examine Section 2 (**HEDIS Quality Measures**). Review the Statin Therapy compliance gap in Diabetes ($45.4\%$ actual vs. $65.0\%$ benchmark) and Cardiovascular Disease ($53.4\%$ actual vs. $80.0\%$ benchmark).

#### Key Decisions to Make:
* [x] Authorize the pharmacy safety recall to switch all 41 asthmatics from Lisinopril to ARBs or CCBs within 48 hours.
* [x] Mandate standing nurse titration orders for the 109 unmedicated chronic patients.
* [x] Deploy protocolized statin therapy reconciliation to capture the $+\$420,000$ HEDIS quality shared-savings bonus.

---

### ⚙️ Persona 2: Chief Operating Officer (COO) & VP of Population Health

> **Core Mandate**: Calibrate clinical workforce capacity, eliminate outreach blind spots, and enforce longitudinal surveillance cadences.

#### Recommended 3-Step Navigation Pathway:
1. **Act 2: Operations & Reach (`pages/2_operations.py`)**:
   * **Patient Contactability Distribution**: Note that **145 high-risk patients (14.8%)** lack both a phone number and an email address in the EHR. Automated SMS recall workflows will fail for this group 100% of the time.
   * **Surveillance Recency Matrix**: Review the 180-day longitudinal decay heatmap. Identify the **206 patients who have had zero clinical encounters for over 12 months**, with **114 sitting in High or Severe Acuity tiers**.
2. **Act 4: Staffing Economics & ROI (`pages/4_roi.py`)**:
   * **Caseload Sizing Model**: Review the CMSA/NCQA-calibrated staffing model allocating **3.4 FTEs** for Severe Acuity ($1:60$ ratio) and **3.5 FTEs** for High Acuity ($1:100$ ratio).
   * Confirm the total required dedicated workforce: **7.0 Registered Nurse (RN) FTEs**.
3. **Act 5: Strategic Implementation Roadmap (`pages/5_recommendations.py`)**:
   * Review the **90-Day Phased Execution Plan**: Days 1–30 (Triage & Safety Callbacks), Days 31–60 (Care Pod Restructuring), Days 61–90 (Closed-Loop Quality Governance).

#### Key Decisions to Make:
* [x] Reallocate ambulatory clinic front-desk staff to execute mandatory phone/email capture for the 145 uncontactable patients during in-person check-in.
* [x] Authorize the recruitment/reassignment of **7.0 RN Care Managers** into dedicated chronic disease disease-management pods.
* [x] Establish a 60-day callback queue for all patients reaching day 120 of surveillance inactivity.

---

### 💰 Persona 3: Chief Financial Officer (CFO) & Managed Care Director

> **Core Mandate**: Quantify avoidable acute inpatient liability, validate care management business cases, and insulate operating margins against downside risk.

#### Recommended 3-Step Navigation Pathway:
1. **Act 0: Executive Summary (`pages/0_executive_summary.py`)**:
   * **Financial Exposure Strip**: Review the baseline gross inpatient liability: **$\$3,185,000\text{ / Year}$** driven by $254.8$ expected acute hospitalizations across the 553 high-risk patients.
2. **Act 3: Financial Exposure Simulation (`pages/3_financial.py`)**:
   * **AHRQ HCUP Inpatient Cost Simulator**: Adjust the cost-per-stay slider between $\$10,000$ and $\$16,000$ (baseline: $\$12,500$). Observe how hospital exposure scales across service lines.
   * Review Section 3 to see the net financial gain from closing the statin gap.
3. **Act 4: ROI Workbench & Sensitivity Matrix (`pages/4_roi.py`)**:
   * **Interactive ROI Workbench**: Use the sliders to test assumptions:
     * Nurse Fully-Loaded Compensation: $\$85\text{K}$ to $\$125\text{K}$ (default: $\$95\text{K}$).
     * Avoidable Admission Reduction Target: $10\%$ to $35\%$ (default: $20\%$).
   * **Preventative Care Breakeven Frontier**: Inspect the 2D green/amber/red sensitivity heatmap. Notice that positive net margins are maintained even under conservative $15\%$ admission reductions and elevated nurse salaries.
   * **Economic Coverage Model**: Confirm the **+$392,000 net annual operating margin** and **159% self-funding ratio** ($4.8\text{-month}$ payback).

#### Key Decisions to Make:
* [x] Approve the **$\$665,000$ annual operational budget** for the 7.0 RN Care Coordination Unit, supported by positive margin breakeven certainty.
* [x] Factor $+\$637,000$ in inpatient medical cost avoidance and $+\$420,000$ in CMS quality bonuses into next fiscal year's ACO shared-savings budget.

---

### 📋 Persona 4: Nurse Care Coordinator & Healthcare Data Analyst

> **Core Mandate**: Screen daily priority patient lists, execute targeted clinical triage callbacks, export audit rosters, and verify metric calculations.

#### Recommended Navigation Pathway:
1. **Act 1: Interactive Triage Worklist (`pages/1_clinical.py`)**:
   * Use the **Worklist Filters**: Set Acuity Tier to *Severe Acuity* and select *Unmedicated* or *Therapeutic Discordance*.
   * Use the **Patient Search Bar** to look up specific individuals by name.
   * View live summary badges: filtered patient count, severe cases, unmedicated status, and assigned care pathways.
2. **Sidebar: Export Center**:
   * Click **"📥 Download Care Gap Patient Roster (CSV)"** to generate an audit-ready patient file formatted for direct import into Epic / Cerner EHR workqueues.
   * Click **"📄 Download Certified Board Memorandum (Markdown)"** to generate an offline executive briefing summary.
3. **Act 6: Terminology & Compendium Lexicon (`pages/6_glossary.py`)**:
   * Search over 40 clinical, actuarial, and regulatory terms (e.g., *AHRQ HCUP*, *ACC/AHA 2017*, *HEDIS CBP*, *Pareto 80/20 Rule*).
   * Review exact formulas, certified clinical reference values, and project-specific findings.

---

## 🖥️ Screen & Projector Features

* **💼 Boardroom Presentation Mode**: Toggle in the sidebar expands the canvas to 95% widescreen width, elevates contrast, and locks the ROI sensitivity model to certified executive baselines for high-visibility display on conference room screens.
* **↺ One-Click Reset Buttons**: Every interactive visual (Acuity Matrix, Worklist Triage, HCUP Simulator, ROI Workbench, Glossary Search) includes a dedicated reset button to restore default baseline views instantly.
* **📱 Responsive Layout**: Visuals dynamically stretch to 100% of their container width without internal scrollbars across laptop, tablet, and desktop displays.
