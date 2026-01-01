# Smart India Hackathon (SIH) 2025 — Problem Statements & Team Outcomes

## Overview
This dataset provides a cleaned, structured, and analysis-ready view of the **Smart India Hackathon (SIH)**,
covering problem statements, team submissions, institutional participation, and final competition outcomes.

The data has been independently collected, cleaned, and transformed to support **data analysis, visualization,
and exploratory research**.

---

## 📊 Interactive Dashboard
A live analytical dashboard built using Streamlit is available here:

👉 **Dashboard Link:** <PASTE_YOUR_STREAMLIT_URL_HERE>

The dashboard enables:
- Interactive filtering by year, theme, institute, status, and geography
- Problem statement–level and team-level analysis
- Institutional and geographic participation insights
- Dataset exploration and CSV export

---

## 📂 Dataset Contents

The dataset includes:

- **Problem Statements**
  - PS ID, title, category, theme, organization, and department
- **Team Submissions**
  - Team identifiers, team names, leaders, and submission status
- **Institutional Information**
  - Institute name, city, state, and AISHE code
- **Competition Outcomes**
  - Shortlisted teams, winners, and awarded prize amounts

---

## 🧾 Column Overview

### Core Identifiers
- `edition_year` – SIH edition year
- `ps_id` – Unique problem statement ID
- `team_id` – Unique team identifier
- `idea_id` – Unique idea identifier

### Problem Statement Details
- `problem_statement_title` – Official problem statement title
- `category` – Software / Hardware classification
- `theme` – Thematic domain
- `organization` – Issuing organization
- `department` – Responsible department

### Submission & Outcome
- `status` – Final submission status (Winner, Joint Winner, Shortlisted, Awards, etc.)
- `prize_money` – Prize amount awarded (if applicable)
- `total_submission` – Total submissions received
- `max_submission` – Maximum allowed submissions

### Institute Information
- `aishe_code` – AISHE institute code
- `institute_name` – Name of the institute
- `institute_city` – City
- `institute_state` – State

---

## 🔄 Data Processing

The following steps were applied during dataset preparation:

1. Standardized column naming and categorical values
2. Converted numeric fields for aggregation and analysis
3. Preserved missing values where data was not applicable
4. Normalized submission status values for consistency

---

## 🔗 Data Sources

The dataset was compiled using publicly available information published on the
official Smart India Hackathon (SIH) website.

Primary source pages include:

- SIH 2025 Problem Statements  
  https://sih.gov.in/sih2025PS

- SIH 2025 Screening Results — Batch 1  
  https://sih.gov.in/sih2025/screeningresult-batch1

- SIH 2025 Screening Results — Batch 2  
  https://sih.gov.in/sih2025/screeningresult-batch2

- SIH 2025 Screening Results — Batch 3  
  https://sih.gov.in/sih2025/screeningresult-batch3

- SIH 2025 Screening Results — Batch 4  
  https://sih.gov.in/sih2025/screeningresult-batch4

- SIH 2025 Grand Finale Results  
  https://sih.gov.in/sih2025/sih2025-grand-finale-result

These sources are publicly accessible and were used strictly for
educational and analytical purposes.

---

## 🎯 Intended Use

This dataset is suitable for:
- Data analysis and visualization projects
- Educational and academic research
- Hackathon participation analysis
- Institutional and geographic trend analysis

---

## ⚠️ Disclaimer
This dataset is an **independent analytical project** and is **not an official publication**
of the Smart India Hackathon program.

---

## 👤 Attribution
Prepared and curated by **Aryan Prajapati** (2025)

- GitHub: https://github.com/<your-username>
- Dashboard: <PASTE_YOUR_STREAMLIT_URL_HERE>

---

## 📜 License
This dataset is released under the **CC BY 4.0 License**.
Users are free to use, modify, and share the data with proper attribution.
