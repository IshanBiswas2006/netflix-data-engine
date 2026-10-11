# Product Requirements Document (PRD)

## Project Name: Netflix Movies and TV Shows Analysis
**Project Type**: End-to-end Data Analytics Project with an Interactive Flask Web Application

---

## 4.1 Product Overview
The **Netflix Movies and TV Shows Analysis** platform is an end-to-end data analytics system and interactive web portal. It ingests the raw Netflix catalog dataset (covering titles from the mid-20th century through recent releases), applies rigorous data cleaning and normalization, runs exploratory data analysis (EDA), generates reproducible analytical summaries and production-grade Matplotlib charts, stores structured data in MySQL, and presents all insights via a responsive Flask website adhering to the supplied dark aesthetic design template.

---

## 4.2 Problem Statement
Streaming media catalogs are constantly evolving with thousands of movies and TV show seasons added, removed, and curated across international territories. However, raw catalog data often suffers from:
- Inconsistent and missing fields (missing directors, cast, and country affiliations).
- Heterogeneous duration representations (mixing movie runtimes in minutes with TV show season counts).
- Comma-delimited multi-value fields (multiple genres, multiple production countries).
- Misconceptions conflating theatrical `release_year` with the digital `date_added` onto Netflix.

There is a clear need for a clean, reproducible, and mathematically sound analytics pipeline that processes this catalog, models it in relational SQL databases, answers critical media questions, and visualizes trends cleanly.

---

## 4.3 Project Goals
1. **Dataset Understanding**: Systematically inspect schemas, record counts, null rates, and distribution boundaries.
2. **Data Cleaning**: Implement reproducible transformations separating duration units, parsing datetime formats, and eliminating inconsistencies.
3. **Exploratory Data Analysis**: Calculate exact metrics for content type splits (Movies vs TV Shows), release year trends, international content production, genre dominance, rating distributions, and addition velocity.
4. **Relational Database Modeling**: Define robust MySQL schemas (`netflix_titles`, `title_countries`, `title_genres`) and execute analytical SQL queries with performance indices.
5. **Data Visualization**: Generate 8 high-resolution Matplotlib visualizations styled harmoniously with the dark UI theme.
6. **Web Presentation**: Build a Flask web app with 5 dedicated routes (`/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about`).
7. **Design Replication**: Faithfully replicate the supplied UI template's dark visual identity, typography (`Tanker`, `Space Grotesk`, `Inter`), glowing orbs, blurred sticky navigation, and card aesthetics.
8. **Automated Testing & Documentation**: Maintain 100% test coverage of cleaning logic, analytical computations, and web routes via `pytest`.

---

## 4.4 Intended Users
- **Data Analysts & Recruiters**: Evaluating end-to-end data engineering, SQL, visualization, and Python engineering competencies.
- **Academic Reviewers & Portfolio Visitors**: Assessing analytical methodology and software engineering best practices.
- **Streaming Industry Enthusiasts**: Exploring actual statistical insights into the Netflix catalog composition.

---

## 4.5 Functional Requirements
- **FR-01**: Load the original raw dataset from `data/raw/netflix_titles.csv`.
- **FR-02**: Validate dataset schema against expected columns (`show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`).
- **FR-03**: Clean the dataset reproducibly without altering the raw source file.
- **FR-04**: Preserve raw records and document affected row counts in `reports/data_cleaning_notes.md`.
- **FR-05**: Generate structured analytical summaries for catalog splits, ratings, countries, genres, and addition trends.
- **FR-06**: Model and store the cleaned catalog in MySQL (`netflix_analysis` database).
- **FR-07**: Execute analytical SQL queries with clear business interpretations.
- **FR-08**: Generate 8 standardized Matplotlib charts saved into `static/images/charts/`.
- **FR-09**: Serve analytical findings through Flask views.
- **FR-10**: Embed and display generated charts with responsive styling.
- **FR-11**: Provide an interactive SQL query inspector displaying questions, SQL code, and real result tables.
- **FR-12**: Gracefully handle missing datasets or database offline states with user-friendly alerts without crashing.
- **FR-13**: Maintain complete project documentation in `README.md` and reports.
- **FR-14**: Provide unit and integration test suites using `pytest`.
- **FR-15**: Maintain visual fidelity with the supplied template design tokens, typography, and layout.

---

## 4.6 Non-Functional Requirements
- **Code Readability & Modularity**: Separation of concerns (`src/data_cleaning.py`, `src/data_analysis.py`, `src/visualization.py`, `src/database.py`).
- **Reproducibility**: Parameterized scripts and deterministic execution.
- **Security**: No hardcoded credentials; environment variables loaded from `.env` via `python-dotenv`.
- **Performance**: Precomputed analytics and cached visualizations preventing heavy DataFrame computations on every request.
- **Accessibility & Responsiveness**: Clean semantic HTML5, high-contrast dark palette, responsive breakpoints (Desktop, Laptop, Tablet, Mobile).

---

## 4.7 Out of Scope
- User authentication, login, or user registration.
- Video streaming player or copyright-protected media playback.
- Machine learning recommendation algorithms.
- Payment systems or e-commerce features.
- External cloud API dependencies.

---

## 4.8 Acceptance Criteria
- [x] Raw dataset validated and preserved at `data/raw/netflix_titles.csv`.
- [x] Processed dataset generated at `data/processed/netflix_cleaned.csv`.
- [x] 8 Matplotlib charts created in `static/images/charts/`.
- [x] SQL scripts created in `sql/` and query executor in `src/database.py`.
- [x] All 5 Flask routes (`/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about`) functional.
- [x] UI matches the dark theme, typography, and card components of the supplied template.
- [x] Automated pytest test suite passes completely.
- [x] Complete documentation in `README.md`, findings, and audit reports.
