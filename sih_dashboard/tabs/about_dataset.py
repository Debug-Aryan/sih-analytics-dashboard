from __future__ import annotations

import streamlit as st


def render() -> None:
    """Render the About Dataset tab with documentation."""

    st.header("📖 About This Dataset")

    st.markdown(
        """
        ## Smart India Hackathon — Problem Statements & Team Submissions

        This dashboard provides an analytical view of Smart India Hackathon (SIH) data, covering
        problem statements, team submissions, institutional participation, and final outcomes
        across multiple SIH editions.

        The dataset has been independently collected, cleaned, structured, and transformed to
        enable reliable exploration, comparison, and insight generation.

        ---

        ## 📂 Dataset Overview

        The dataset includes:
        - **Problem Statements** issued by government ministries, departments, and organizations
        - **Team Submissions** from participating institutes across India
        - **Institutional Information** with city- and state-level geographic coverage
        - **Competition Outcomes**, including shortlisted teams and awarded winners

        ---

        ## 🧾 Column Descriptions

        ### Edition & Problem Statement Details
        - `edition_year` – Smart India Hackathon edition year
        - `ps_id` – Unique problem statement identifier
        - `problem_statement_title` – Official title of the problem statement
        - `category` – Problem category (Software / Hardware)
        - `theme` – Thematic domain of the problem statement
        - `organization` – Issuing organization or ministry
        - `department` – Responsible department under the organization

        ### Submission Metrics
        - `total_submission` – Total number of submissions received for the problem statement
        - `max_submission` – Maximum allowed submissions for the problem statement
        - `serial_no` – Serial reference number of the submission entry

        ### Team Details
        - `idea_id` – Unique identifier for the submitted idea
        - `team_id` – Unique team identifier
        - `team_name` – Registered team name
        - `team_leader_name` – Name of the team leader
        - `status` – Final evaluation status of the submission  
          *(Winner, Joint Winner, Shortlisted, Waitlist, Award Categories)*
        - `prize_money` – Prize amount awarded (if applicable)

        ### Institute Information
        - `aishe_code` – AISHE institute identification code
        - `institute_name` – Name of the participating institute
        - `institute_city` – City of the institute
        - `institute_state` – State of the institute

        ---

        ## 🔄 Data Processing & Transformations

        The following data preparation steps were applied:

        1. **Standardization** – Column names normalized and categorical values standardized
        2. **Type Casting** – Numeric fields converted to support aggregation and analysis
        3. **Missing Values Handling** – Non-applicable values retained as null to preserve data integrity
        4. **Outcome Normalization** – Submission status values mapped to consistent outcome categories

        ---

        ## 🧭 How to Use This Dashboard

        - Sidebar filters allow data selection by edition year, theme, status, institute, and geography
        - All analytical tabs update dynamically based on active filters
        - The **Data Explorer** tab supports custom column selection and CSV export for offline analysis

        ---

        ## 👤 Dataset Preparation & Attribution

        This dataset was independently collected, cleaned, structured, and analyzed by:

        **Aryan Prajapati**  
        Dataset Curation, Data Engineering & Analytical Dashboard Development (2025)

        - GitHub: https://github.com/Debug-Aryan/sih-analytics-dashboard
        - Kaggle: https://www.kaggle.com/aryanprajapati33/
        
        The dataset is intended strictly for educational, analytical, and exploratory purposes.

        ---

        ## 🛠️ Technology Stack

        - Python
        - Pandas
        - Streamlit
        - Plotly
        - NumPy

        ---

        *This dashboard is an independent analytical project and is not an official publication of the Smart India Hackathon program.*
        """
    )
