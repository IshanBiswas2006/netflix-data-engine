# Project Plan: Netflix Movies and TV Shows Analysis

## 1. Current Workspace Structure

- **Project Root**: `d:\Work\netflix`
- **Existing Template Files**:
  - `index.html`: Reference homepage (SSR HTML with embedded styling, custom typography, Framer layout)
  - `about.html`, `about/index.html`: Reference about page
  - `server.js`: Node.js dev server with byte-range MP4 video support and MIME handler
  - `package.json`: NPM scripts for dev server
  - `assets/`:
    - `assets/css/`: `styles.css` (142 KB), `fonts.css` (5.4 KB), `breakpoints.css` (316 B)
    - `assets/fonts/`: 32 WOFF2 font files (Space Grotesk, Tanker, Inter)
    - `assets/images/`: 58 full-resolution photos, polaroids, mockups, badges, vector SVGs
    - `assets/videos/`: 2 MP4 showcase videos
    - `assets/icons/`: Favicons and touch icons
    - `assets/js/`: Framer runtime, React, Motion, script bundles
    - `assets/data/`: Framer search index JSON files
- **Dataset**: `data/raw/netflix_titles.csv` acquired and validated (6,234 rows, 12 columns).
- **Environment**:
  - Python: `C:\Users\ISHAN\AppData\Local\Python\bin\python.exe` (Python 3.14)
  - Installed packages: Pandas (3.0.5), NumPy (2.5.1), Matplotlib (3.11.1), Flask (3.1.3), Pytest (9.1.1), MySQL Connector (26.7.0), python-dotenv (1.2.3), Jupyter / ipykernel.
  - MySQL Service: `MYSQL80` is running on `localhost:3306`.
  - Node.js dev server available.

## 2. Required Files to Create

```
d:\Work\netflix\
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── config/
│   └── settings.py
├── data/
│   ├── raw/netflix_titles.csv
│   └── processed/netflix_cleaned.csv
├── notebooks/
│   └── netflix_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── data_analysis.py
│   ├── visualization.py
│   └── database.py
├── sql/
│   ├── create_database.sql
│   ├── create_tables.sql
│   └── analysis_queries.sql
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── analysis.html
│   ├── visualizations.html
│   ├── sql_queries.html
│   └── about.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── fonts.css
│   │   └── breakpoints.css
│   ├── js/
│   │   └── main.js
│   ├── images/
│   │   └── charts/
│   │       ├── 01_movies_vs_tv_shows.png
│   │       ├── 02_titles_by_release_year.png
│   │       ├── 03_top_10_countries.png
│   │       ├── 04_top_10_genres.png
│   │       ├── 05_content_rating_distribution.png
│   │       ├── 06_movie_duration_distribution.png
│   │       ├── 07_tv_show_seasons_distribution.png
│   │       └── 08_titles_added_over_time.png
│   └── (integrated assets from template: fonts, images, etc.)
├── reports/
│   ├── project_plan.md
│   ├── PRD.md
│   ├── ui_template_analysis.md
│   ├── ui_replication_analysis.md
│   ├── animation_inventory.md
│   ├── interaction_inventory.md
│   ├── asset_mapping.md
│   ├── data_quality_report.md
│   ├── data_cleaning_notes.md
│   ├── findings.md
│   ├── test_results.md
│   ├── ui_comparison_report.md
│   ├── ui_test_results.md
│   ├── resume_description.md
│   ├── linkedin_project.md
│   └── final_audit.md
└── tests/
    ├── test_cleaning.py
    ├── test_analysis.py
    └── test_routes.py
```

## 3. Implementation Order (Phases 0 to 16)

1. **Phase 0**: Template and Workspace Inspection, Project Plan
2. **Phase 1**: Environment Configuration (`requirements.txt`, `.env.example`, `.gitignore`, `config/settings.py`)
3. **Phase 2**: Dataset Inspection & Quality Report (`reports/data_quality_report.md`)
4. **Phase 3**: Data Cleaning Pipeline (`src/data_cleaning.py`, `data/processed/netflix_cleaned.csv`, `reports/data_cleaning_notes.md`)
5. **Phase 4**: Exploratory Data Analysis & Jupyter Notebook (`src/data_analysis.py`, `notebooks/netflix_analysis.ipynb`, `reports/findings.md`)
6. **Phase 5**: MySQL Database Scripts & Query Engine (`sql/*.sql`, `src/database.py`)
7. **Phase 6**: Matplotlib Visualizations (`src/visualization.py`, 8 high-res charts with template color harmony)
8. **Phase 7**: Flask Backend Routes & Caching (`app.py`)
9. **Phase 8**: Frontend Implementation replicating supplied template styling (`templates/*.html`, `static/css/style.css`, `static/js/main.js`)
10. **Phase 9**: End-to-End Pipeline Integration
11. **Phase 10**: Automated Pytest Suite (`tests/test_cleaning.py`, `tests/test_analysis.py`, `tests/test_routes.py`)
12. **Phase 11**: Systematic Debugging & Verification
13. **Phase 12**: Visual UI Template Comparison (`reports/ui_comparison_report.md`)
14. **Phase 13**: Performance & Code Quality Review
15. **Phase 14**: Comprehensive Documentation (`README.md`)
16. **Phase 15**: GitHub & Portfolio Preparation (`reports/resume_description.md`, `reports/linkedin_project.md`)
17. **Phase 16**: Final Audit (`reports/final_audit.md`)

## 4. Potential Blockers & Mitigations

- **MySQL Authentication**: MySQL service `MYSQL80` is running on port 3306, but requires user credentials.
  - *Mitigation*: Configure `.env.example` with clear instructions, and in `src/database.py` support real MySQL connections when configured, plus a built-in analytical query engine executing the exact same SQL logic and returning structured query tables from the verified processed data so the site never crashes.
- **Frontend Fidelity**: Framer export uses specific proprietary module bundles for some dynamic React interactions.
  - *Mitigation*: Re-use the exact CSS tokens, typography (`Tanker`, `Space Grotesk`, `Inter`), blurred sticky header, glowing background orbs, pill badges, and dark modern palette in clean Flask Jinja templates with native JavaScript, ensuring 100% visual parity, zero broken dependencies, and instant load times.
