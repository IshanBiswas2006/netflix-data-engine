# Netflix Movies and TV Shows Analysis

> An end-to-end data analytics engineering project and interactive Flask web application uncovering catalog composition, international diversification, runtime trends, and temporal ingestion velocity across the Netflix catalog.

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-3.0-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11-green.svg)
![Tests](https://img.shields.io/badge/Pytest-21%20Passed-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

---

## 1. Project Title
**Netflix Movies and TV Shows Analysis**: In-Depth Empirical Data Pipeline, MySQL Relational Modeling & Interactive Analytics Portal.

---

## 2. Overview
This project delivers a complete data analytics lifecycle: from ingesting raw streaming metadata to automated cleaning, statistical exploratory analysis, relational MySQL schema design, production Matplotlib visualization generation, and presentation through an interactive Flask web application. Designed to replicate modern dark-mode aesthetic standards, the application incorporates custom typography, sticky frosted glass headers, and responsive layouts.

---

## 3. Objectives
- Ingest and validate the complete Netflix catalog (6,234 titles).
- Resolve data quality defects, decomposing composite duration strings and parsing timestamps.
- Perform exploratory data analysis to evaluate film versus episodic television dominance.
- Analyze international co-production hubs, genre popularity, and maturity rating profiles.
- Model catalog entities into normalized MySQL tables and execute 10 core analytical queries.
- Generate 8 high-resolution Matplotlib visualizations styled harmoniously with the UI design system.
- Deploy an interactive Flask web application with 5 dedicated routes.
- Maintain 100% automated test coverage with Pytest.

---

## 4. Key Features
- **Reproducible Data Pipeline**: Deterministic scripts for data validation, cleaning, and preprocessing.
- **Relational SQL Database Engine**: MySQL 8.0 schema scripts with 1:N normalized tables (`title_countries`, `title_genres`) and automated offline query execution fallback.
- **Production Visualizations**: 8 Matplotlib figures utilizing dark-mode tokens, custom labels, and clean aesthetic callouts.
- **Interactive Web Interface**: 5 Flask routes (`/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about`) featuring real-time client-side search and query accordions.
- **Exact UI Template Parity**: Dark obsidian canvas (`#0b0d0e`), card surfaces (`#161616`), ambient gradient glows, and custom typography (`Tanker`, `Space Grotesk`, `Inter`).
- **Comprehensive Automated Testing**: 21 unit and integration tests covering cleaning edge cases, aggregate computations, and web routes.

---

## 5. Technologies
- **Core Languages**: Python 3.14, SQL, JavaScript (ES6+), HTML5, CSS3
- **Data Engineering & Analytics**: Pandas 3.0, NumPy 2.5
- **Data Visualization**: Matplotlib 3.11
- **Database Engine**: MySQL Server 8.0, SQLite (in-memory mirror)
- **Web Backend**: Flask 3.1, Jinja2, Werkzeug
- **Testing & Quality Assurance**: Pytest 9.1
- **Configuration & Secrets**: Python-Dotenv

---

## 6. Dataset Source
- **Origin**: Kaggle / Shivam Bansal Netflix Shows Catalog (`netflix_titles.csv`)
- **Reference**: [Kaggle Dataset Reference](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- **Raw File Location**: `data/raw/netflix_titles.csv`
- **Volume**: 6,234 unique catalog rows, 12 attributes, 2.41 MB

---

## 7. Dataset Schema
| Column | Raw Type | Cleaned Type | Description |
| :--- | :--- | :--- | :--- |
| `show_id` | `int64` | `BIGINT` | Unique primary key identifier |
| `type` | `object` | `VARCHAR(20)` | `Movie` or `TV Show` |
| `title` | `object` | `VARCHAR(255)` | Official title string |
| `director` | `object` | `TEXT` | Credited directors (comma-separated) |
| `cast` | `object` | `TEXT` | Key cast members (comma-separated) |
| `country` | `object` | `VARCHAR(255)` | Production / co-producing countries |
| `date_added` | `object` | `VARCHAR(50)` | Raw date string (e.g. "September 9, 2019") |
| `date_added_clean` | *New* | `DATE` | Standardized ISO-8601 date (`YYYY-MM-DD`) |
| `year_added` | *New* | `INT` | Extracted digital addition year (2008–2020) |
| `month_added` | *New* | `INT` | Extracted digital addition month (1–12) |
| `release_year` | `int64` | `INT` | Theatrical / broadcast release year (1925–2020) |
| `rating` | `object` | `VARCHAR(20)` | Content maturity rating (TV-MA, TV-14, R, etc.) |
| `duration` | `object` | `VARCHAR(50)` | Raw composite duration string |
| `duration_minutes` | *New* | `INT` | Runtime in minutes (for Movies only) |
| `seasons_count` | *New* | `INT` | Total seasons (for TV Shows only) |
| `listed_in` | `object` | `TEXT` | Genre categories (comma-separated) |
| `description` | `object` | `TEXT` | Textual synopsis narrative |

---

## 8. Project Structure
```
netflix-movies-tv-shows-analysis/
├── app.py                      # Flask web application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git untracked paths
├── README.md                   # Complete project documentation
│
├── config/
│   └── settings.py             # Paths, database, and app settings
│
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv  # Original raw dataset (preserved)
│   └── processed/
│       └── netflix_cleaned.csv # Cleaned reproducible dataset
│
├── notebooks/
│   └── netflix_analysis.ipynb  # Executable Jupyter notebook
│
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py        # Data validation and cleaning pipeline
│   ├── data_analysis.py        # Exploratory analysis & aggregate stats
│   ├── visualization.py        # Matplotlib visualization generator
│   └── database.py             # MySQL connector & SQL engine
│
├── sql/
│   ├── create_database.sql     # Database creation script
│   ├── create_tables.sql       # Table schema with indexes
│   └── analysis_queries.sql    # 10 Analytical SQL queries
│
├── templates/
│   ├── base.html               # Shared layout with sticky frosted nav
│   ├── index.html              # Home page with hero and core stats
│   ├── analysis.html           # In-depth exploratory data tables
│   ├── visualizations.html     # Visualizations gallery
│   ├── sql_queries.html        # Interactive SQL queries & live results
│   └── about.html              # Methodology, tech stack & limitations
│
├── static/
│   ├── css/
│   │   └── style.css           # Core stylesheet matching template tokens
│   ├── js/
│   │   └── main.js             # Accordion, mobile nav & table search
│   ├── fonts/                  # Space Grotesk, Tanker, Inter WOFF2 files
│   ├── icons/                  # Favicons and touch icons
│   └── images/
│       └── charts/             # 8 Generated Matplotlib PNG charts
│
├── reports/
│   ├── project_plan.md         # Workspace structure & execution roadmap
│   ├── PRD.md                  # Product Requirements Document
│   ├── ui_template_analysis.md # Visual inspection of supplied template
│   ├── ui_replication_analysis.md # Component & interaction breakdown
│   ├── animation_inventory.md  # Animation states and timing
│   ├── interaction_inventory.md# User interaction behaviors
│   ├── asset_mapping.md        # Asset locations and mapping
│   ├── data_quality_report.md  # Raw data quality & null audit
│   ├── data_cleaning_notes.md  # Cleaning rationale & affected rows
│   ├── findings.md             # Key empirical analytical results
│   ├── test_results.md         # Pytest execution audit (21 passed)
│   ├── ui_comparison_report.md # Visual parity comparison
│   ├── ui_test_results.md      # Route and asset load test logs
│   ├── resume_description.md   # Resume bullet points
│   ├── linkedin_project.md     # LinkedIn showcase description
│   └── final_audit.md          # Comprehensive completion audit
│
└── tests/
    ├── test_cleaning.py        # Data cleaning unit tests
    ├── test_analysis.py        # Analytical calculation tests
    └── test_routes.py          # Flask route integration tests
```

---

## 9. Data Cleaning Methodology
1. **Schema Validation**: Validates all 12 required columns exist before processing.
2. **String Standardization**: Strips leading/trailing whitespace across all text columns.
3. **Composite Duration Decomposition**:
   - Parses regex `r'(\d+)'` to separate minutes from season counts.
   - Creates `duration_minutes` (Int64) for Movies (mean 99.1 min, median 98 min).
   - Creates `seasons_count` (Int64) for TV Shows (mean 1.8 seasons, 67.1% single-season).
4. **Datetime Extraction**: Converts `"September 9, 2019"` into `date_added_clean` (`YYYY-MM-DD`), `year_added`, and `month_added`.
5. **Deduplication Audit**: Validates uniqueness of all 6,234 `show_id` values.
6. **Data Preservation**: Retains the original raw CSV untouched; writes outputs to `data/processed/netflix_cleaned.csv`.

---

## 10. Analytical Questions
1. What is the total volume of distinct catalog titles ingested?
2. What is the proportional breakdown between Movies and TV Shows?
3. How is content vintage distributed across theatrical release years?
4. Which countries produce the highest volume of catalog titles?
5. Which genres represent the largest segments of the Netflix library?
6. How is the catalog distributed across content maturity ratings?
7. What are the longest runtime feature films on Netflix?
8. Which television series have achieved the highest season counts?
9. How has Netflix's rate of catalog additions grown across digital ingestion years?
10. Which directors have the highest volume of films and series hosted?

---

## 11. SQL Functionality
All queries are implemented in `sql/analysis_queries.sql` and managed programmatically through `src/database.py`:
- Direct execution via `mysql-connector-python` when MySQL connection credentials are provided.
- Automated fallback to an in-memory SQLite relational mirror loaded with the exact processed dataset, ensuring continuous verification and zero crashes when offline.

---

## 12. Visualizations
Generated via `src/visualization.py` using Matplotlib with high-contrast dark theme styling:
1. `01_movies_vs_tv_shows.png`: Donut chart of catalog split (68.4% Movies vs 31.6% TV Shows).
2. `02_titles_by_release_year.png`: Release year trends from 1990 to 2020.
3. `03_top_10_countries.png`: Horizontal bar chart of top producing nations (US, India, UK, Canada, France, Japan).
4. `04_top_10_genres.png`: Horizontal bar chart of top genres (International Movies, Dramas, Comedies).
5. `05_content_rating_distribution.png`: Bar chart of maturity classifications (TV-MA, TV-14, TV-PG, R, PG-13).
6. `06_movie_duration_distribution.png`: Histogram & KDE of movie running times (median 98 min, mean 99.1 min).
7. `07_tv_show_seasons_distribution.png`: Breakdown of TV series seasons (67.1% single-season).
8. `08_titles_added_over_time.png`: Historical velocity of digital catalog additions (peaking at 2,349 in 2019).

---

## 13. Website Pages
- **`GET /` (Overview)**: Hero banner, 4 high-level stat cards, core analytical dimension showcase cards, and recent catalog records table.
- **`GET /analysis` (Analysis)**: Detailed statistical breakdowns, content split tables, duration benchmarks, top countries, top genres, and extreme runtime rankings.
- **`GET /visualizations` (Visualizations)**: High-resolution gallery of all 8 Matplotlib charts with detailed methodology callouts.
- **`GET /sql-queries` (SQL Engine)**: Interactive query viewer with SQL code blocks, execution engine status, real-time client-side search, and verified result tables.
- **`GET /about` (About)**: Project documentation, 6-phase engineering lifecycle, technical stack, limitations, and future enhancements.

---

## 14. Installation Instructions

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Git
- MySQL Server 8.0 (Optional; local SQL fallback included)

---

## 15. Python Environment Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/netflix-movies-tv-shows-analysis.git
cd netflix-movies-tv-shows-analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
```

---

## 16. Dependency Installation
```bash
pip install -r requirements.txt
```

---

## 17. Dataset Placement
Ensure `netflix_titles.csv` is located at:
```
data/raw/netflix_titles.csv
```
If not present, run the automated pipeline to download and validate it.

---

## 18. Environment Variable Configuration
Copy the example environment configuration:
```bash
cp .env.example .env
```
Edit `.env` to configure your database settings if MySQL is available:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=netflix_analysis
PORT=5000
DEBUG=True
```

---

## 19. MySQL Setup
If MySQL is running on your machine:
```bash
mysql -u root -p < sql/create_database.sql
mysql -u root -p < sql/create_tables.sql
```

---

## 20. Database Import
To import the cleaned dataset directly into MySQL:
```bash
python -c "from src.database import import_csv_to_mysql; import_csv_to_mysql()"
```

---

## 21. Data Processing Commands
To run data cleaning and generate the processed dataset:
```bash
python src/data_cleaning.py
```
Outputs: `data/processed/netflix_cleaned.csv`

To execute exploratory analysis in terminal:
```bash
python src/data_analysis.py
```

---

## 22. Chart Generation Commands
To generate or refresh all 8 Matplotlib visualizations:
```bash
python src/visualization.py
```
Outputs: `static/images/charts/*.png`

---

## 23. Website Startup
Start the Flask web application dev server:
```bash
python app.py
```
Open your browser at:
- **Home**: [http://localhost:5000/](http://localhost:5000/)
- **Analysis**: [http://localhost:5000/analysis](http://localhost:5000/analysis)
- **Visualizations**: [http://localhost:5000/visualizations](http://localhost:5000/visualizations)
- **SQL Queries**: [http://localhost:5000/sql-queries](http://localhost:5000/sql-queries)
- **About**: [http://localhost:5000/about](http://localhost:5000/about)

---

## 24. Testing Commands
Run the complete automated test suite:
```bash
pytest tests/ -v
```
All 21 tests execute in under 1 second.

---

## 25. Example Analytical Findings
- **Film Dominance**: Movies represent 68.42% of the library (4,265 titles) while TV Shows account for 31.58% (1,969 titles).
- **International Content**: India ranks as the second-largest content contributor (838 titles) behind the United States (2,610 titles).
- **Genre Leadership**: "International Movies" (1,927) and "Dramas" (1,623) form the dominant categories.
- **Adult Demographics**: 59.8% of the catalog is classified as TV-MA or TV-14.
- **TV Longevity**: 67.09% of all television series conclude after only 1 season.
- **Peak Addition Velocity**: Digital catalog additions surged exponentially from 25 titles in 2014 to 2,349 additions in 2019.

---

## 26. Limitations
- Cast and director metadata are absent in certain episodic series and documentary productions.
- Does not incorporate proprietary viewership hours or financial licensing fees.
- Date added records reflect Netflix digital availability, not original theatrical debuts.

---

## 27. Future Improvements
- Automated ingestion via live metadata APIs (TMDB, OMDb).
- Dynamic multi-variable faceted filtering by genre, decade, and country.
- Natural language processing (NLP) sentiment scoring of plot synopses.

---

## 28. Credits and Licensing Considerations
- **Dataset Author**: Shivam Bansal (Kaggle)
- **Design Inspiration**: Supplied dark-mode portfolio template (`nehayadav.framer.website`)
- **License**: MIT License
