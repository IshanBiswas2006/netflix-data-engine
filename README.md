<div align="center">

# 🎬 Netflix Movies & TV Shows Analysis

### Catalog Intelligence Portal — From Raw Data to Production Dashboard

*An end-to-end data analytics engineering pipeline and production-ready Flask portal examining catalog composition, international co-productions, runtime dynamics, content maturity, and ingestion velocity across **6,234 Netflix titles**.*

<br>

[![Live Demo](https://img.shields.io/badge/🚀_LIVE_DEMO-Open_App-E50914?style=for-the-badge&logo=netflix&logoColor=white)](https://netflix-analytics-2uzs.onrender.com/)

<br>

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Pytest-21%20Passed-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://netflix-analytics-2uzs.onrender.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-E50914?style=flat-square)](LICENSE)

</div>

---

## 🌐 Live Demo & Preview

| | |
| :--- | :--- |
| 🔴 **Live Application** | **[netflix-analytics-2uzs.onrender.com](https://netflix-analytics-2uzs.onrender.com/)** |
| 💻 **Local URL** | `http://localhost:5000/` |

> ⏳ *Hosted on Render's free tier — the first request may take ~30–60 seconds while the service wakes up.*

<div align="center">

![Netflix Catalog Intelligence Portal](reports/preview.png)

</div>

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-analytical-features)
3. [Key Insights](#-key-insights-at-a-glance)
4. [Technology Stack](#-technology-stack)
5. [Dataset Schema](#-dataset-schema--architecture)
6. [Repository Structure](#-repository-structure)
7. [Prerequisites](#-prerequisites)
8. [Local Setup](#-local-setup--installation)
9. [Running Locally](#-running-locally)
10. [Automated Testing](#-automated-testing)
11. [Environment Variables](#-environment-variables)
12. [Deployment: Render](#-deployment-method-a-render--paas)
13. [Deployment: Docker](#-deployment-method-b-docker--docker-compose)
14. [Asset & Path Validation](#-asset--path-validation)
15. [Performance Report](#-performance--size-optimization-report)
16. [Limitations & Future Scope](#-known-limitations--future-scope)
17. [License & Attributions](#-license--attributions)

---

## 🎯 Project Overview

The **Netflix Movies and TV Shows Analysis** platform bridges exploratory data science, relational database engineering, and interactive web visualization into one cohesive, production-grade application.

| # | Objective | Description |
| :-: | :--- | :--- |
| 1️⃣ | **Automated ETL Pipeline** | Ingest raw metadata, clean missing attributes, standardize dates to ISO-8601, and decompose duration (`min` vs `Seasons`). |
| 2️⃣ | **Exploratory Analysis** | Uncover content shifts, top production hubs, maturity ratings, and ingestion spikes. |
| 3️⃣ | **Relational SQL Engine** | 3NF normalized tables with bridge tables (`title_countries`, `title_genres`) and 10 analytical queries with SQLite/MySQL fallback. |
| 4️⃣ | **Interactive Web Portal** | 5 responsive Flask routes, dark obsidian design, SQL accordions, live table search, and a custom cursor effect. |

---

## ✨ Key Analytical Features

| Route | Feature | Highlights |
| :--- | :--- | :--- |
| `/` | 📊 **Overview Dashboard** | KPI cards (Total Titles, Movie/TV split, vintage range), recent ingest samples, floating 3D accents |
| `/analysis` | 🔎 **Exploratory Analytics** | Production volume, genre frequencies, maturity classes, runtime quartiles, TV longevity |
| `/visualizations` | 🖼️ **Visualizations Gallery** | 8 publication-grade Matplotlib figures with curated dark-mode palettes |
| `/sql-queries` | 🗄️ **SQL Analytics Engine** | 10 business questions, expandable SQL accordions, verified output tables |
| `/about` | 📘 **Methodology** | Pipeline architecture, normalization choices, assumptions, technical limits |

🖱️ **Fluid Custom Cursor** — `requestAnimationFrame` lerp tracking (60/120fps), `mix-blend-mode: difference`, hover expansion, automatic touch-device suppression.

---

## 💡 Key Insights at a Glance

| Metric | Finding |
| :--- | :--- |
| 🎥 **Content Split** | Movies **68.4%** · TV Shows **31.6%** |
| 🌍 **Top Production Hubs** | United States, India, United Kingdom |
| 🔞 **Dominant Rating** | TV-MA |
| 📅 **Catalog Span** | 1925 – 2020 |
| 📈 **Platform Additions** | 2008 – 2020 (with notable ingestion spikes) |

---

## 🛠️ Technology Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Backend** | Python 3.11 / 3.14, Flask 3.1, Werkzeug, Jinja2 |
| **Data Engineering** | Pandas 2.2+, NumPy 1.26+ |
| **Visualization** | Matplotlib 3.8+ (custom dark-mode design system) |
| **Database** | MySQL Server 8.0, In-Memory SQLite fallback |
| **Frontend** | HTML5, CSS3 (Variables, Flexbox, Grid), JavaScript ES6+ |
| **Typography** | Tanker, Space Grotesk, Inter (self-hosted `.woff2`) |
| **Production WSGI** | Gunicorn 21.2+ (multi-worker) |
| **Containerization** | Docker, Docker Compose (`python:3.11-slim`) |
| **Testing** | Pytest 9.1 (21 automated tests) |

---

## 🧬 Dataset Schema & Architecture

- **Source**: [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) (`netflix_titles.csv`)
- **Volume**: 6,234 unique titles (1925 – 2020)

| Attribute | Source Type | Cleaned Type | Description |
| :--- | :--- | :--- | :--- |
| `show_id` | `int64` | `BIGINT` | Unique primary key |
| `type` | `object` | `VARCHAR(20)` | `Movie` or `TV Show` |
| `title` | `object` | `VARCHAR(255)` | Official catalog title |
| `director` | `object` | `TEXT` | Credited directors |
| `cast` | `object` | `TEXT` | Credited cast |
| `country` | `object` | `VARCHAR(255)` | Co-producing territories |
| `date_added` | `object` | `VARCHAR(50)` | Raw ingest date string |
| `date_added_clean` | *Engineered* | `DATE` | ISO-8601 date (`YYYY-MM-DD`) |
| `year_added` | *Engineered* | `INT` | Platform release year (2008–2020) |
| `month_added` | *Engineered* | `INT` | Platform release month (1–12) |
| `release_year` | `int64` | `INT` | Original broadcast/theatrical year |
| `rating` | `object` | `VARCHAR(20)` | Maturity class (TV-MA, TV-14, PG-13, R) |
| `duration` | `object` | `VARCHAR(50)` | Raw string (`90 min`, `2 Seasons`) |
| `duration_minutes` | *Engineered* | `INT` | Parsed runtime (Movies) |
| `seasons_count` | *Engineered* | `INT` | Parsed seasons (TV Shows) |
| `listed_in` | `object` | `TEXT` | Genres / categories |
| `description` | `object` | `TEXT` | Editorial synopsis |

---

## 📁 Repository Structure

```
netflix/
├── app.py                      # Flask entry point & routes
├── requirements.txt            # Python dependencies
├── Procfile                    # PaaS process config (Render / Railway)
├── runtime.txt                 # Python runtime (python-3.11.9)
├── render.yaml                 # Render Infrastructure-as-Code blueprint
├── Dockerfile                  # Production container (python:3.11-slim)
├── docker-compose.yml          # Orchestration with health checks
├── .dockerignore               # Container build exclusions
├── .env.example                # Environment variable template
├── .gitignore                  # Git exclusions
├── README.md                   # Documentation
│
├── config/
│   └── settings.py             # App, database & filesystem config
│
├── data/
│   ├── raw/netflix_titles.csv          # Original dataset (2.41 MB)
│   └── processed/netflix_cleaned.csv   # Cleaned dataset (2.55 MB)
│
├── src/
│   ├── data_cleaning.py        # Validation, imputation, timestamp extraction
│   ├── data_analysis.py        # Statistics, distributions, rankings
│   ├── database.py             # MySQL connector & SQLite fallback
│   └── visualization.py        # Matplotlib chart generator
│
├── sql/
│   ├── create_database.sql     # Schema initialization
│   ├── create_tables.sql       # 3NF modeling & normalization
│   └── analysis_queries.sql    # 10 analytical queries
│
├── static/
│   ├── css/style.css           # Design system, layout, cursor, animations
│   ├── js/main.js              # Accordion, search filter, cursor physics
│   ├── fonts/                  # Self-hosted WOFF2 fonts
│   ├── icons/                  # Favicons & touch icons
│   └── images/
│       ├── charts/             # 8 generated visualizations
│       └── *.png               # 4 floating 3D stickers
│
├── templates/
│   ├── base.html               # Master layout & cursor canvas
│   ├── index.html              # Overview (/)
│   ├── analysis.html           # Findings (/analysis)
│   ├── visualizations.html     # Charts (/visualizations)
│   ├── sql_queries.html        # SQL engine (/sql-queries)
│   └── about.html              # Architecture (/about)
│
├── tests/
│   ├── test_cleaning.py        # 8 cleaning & feature tests
│   ├── test_analysis.py        # 7 metrics & ranking tests
│   └── test_routes.py          # 6 route & HTML tests
│
├── notebooks/
│   └── netflix_analysis.ipynb  # Exploratory notebook
│
└── reports/
    └── preview.png             # Preview screenshot
```

---

## ✅ Prerequisites

- 🐍 **Python** 3.10, 3.11, or 3.12+ (tested up to 3.14)
- 📦 **Pip** — latest version (`pip install --upgrade pip`)
- 🐳 **Docker** *(optional)* — Docker Desktop 24+ / Docker Engine

---

## ⚙️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/IshanBiswas2006/netflix-data-engine.git
cd netflix-data-engine
```

**2. Create & activate a virtual environment**

<details>
<summary><b>🪟 Windows (PowerShell)</b></summary>

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
</details>

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
```
</details>

**3. Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```

> 💡 The platform works out-of-the-box with default fallbacks. A live MySQL database is optional — the app automatically uses precomputed analytics and in-memory execution.

---

## ▶️ Running Locally

**Development server**
```bash
python app.py
```
Open **http://localhost:5000/**

**Production WSGI server (Gunicorn)**
```bash
gunicorn --workers=2 --threads=4 --bind=0.0.0.0:5000 app:app
```

---

## 🧪 Automated Testing

```bash
pytest -v
```

```
tests/test_cleaning.py ........                                          [ 38%]
tests/test_analysis.py .......                                           [ 71%]
tests/test_routes.py ......                                              [100%]
============================== 21 passed in 0.96s ==============================
```

---

## 🔐 Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `5000` | HTTP server port |
| `FLASK_ENV` | `production` | Set `development` for auto-reload |
| `DEBUG` | `False` | Flask debug mode |
| `SECRET_KEY` | *(random)* | Session signing |
| `DB_HOST` | `localhost` | MySQL host *(optional)* |
| `DB_PORT` | `3306` | MySQL port *(optional)* |
| `DB_USER` | `root` | MySQL user *(optional)* |
| `DB_PASSWORD` | `""` | MySQL password *(optional)* |
| `DB_NAME` | `netflix_analysis` | MySQL database *(optional)* |

---

## ☁️ Deployment Method A: Render / PaaS

🔴 **Currently live at → [netflix-analytics-2uzs.onrender.com](https://netflix-analytics-2uzs.onrender.com/)**

### Option 1 — One-Click Blueprint (`render.yaml`)
1. Push the repo to **GitHub** or **GitLab**.
2. Open the [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** → **Blueprint**.
4. Connect the repo — Render reads [`render.yaml`](render.yaml) and preconfigures:
   - **Environment**: Python 3.11.9
   - **Build**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start**: `gunicorn --workers=2 --threads=4 --timeout=60 --bind=0.0.0.0:$PORT app:app`
   - **Port**: Render's dynamic `$PORT`
5. Click **Apply** — live in ~2 minutes with free SSL.

### Option 2 — Manual Web Service
1. **New +** → **Web Service** → select your repo.
2. Configure:
   - **Name**: `netflix-analytics`
   - **Region**: Any (e.g., Oregon, Frankfurt)
   - **Branch**: `master`
   - **Runtime**: `Python 3`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn --workers=2 --threads=4 --bind=0.0.0.0:$PORT app:app`
3. Add environment variables:
   - `PYTHON_VERSION` = `3.11.9`
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = *(Generate)*
4. Click **Create Web Service**.

---

## 🐳 Deployment Method B: Docker & Docker Compose

Packages the app, runtime, Gunicorn, datasets, and static assets into one immutable container — runs on AWS ECS, Google Cloud Run, Azure App Service, DigitalOcean, or any Linux VPS.

### Docker Compose
```bash
docker compose up -d --build
```

| Task | Command |
| :--- | :--- |
| Health status | `docker compose ps` |
| Live logs | `docker compose logs -f` |
| Stop | `docker compose down` |

App runs at **http://localhost:5000/**

### Standalone Docker
```bash
docker build -t netflix-analytics:latest .
docker run -d -p 5000:5000 --name netflix_app --restart unless-stopped netflix-analytics:latest
```

### Google Cloud Run / AWS App Runner
The `Dockerfile` binds to `$PORT` and includes `HEALTHCHECK curl -f http://localhost:5000/`:
```bash
gcloud run deploy netflix-analytics \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔍 Asset & Path Validation

Automated audit of all 25 template references, CSS font imports, and static links:

- ✅ **0 Broken Links** — every `url_for('static', filename=...)` resolves
- ✅ **0 Missing Fonts** — every `@font-face` maps to an existing `.woff2`
- ✅ **Case-Sensitivity Compliant** — lowercase/hyphenated paths, safe for Linux hosts

---

## 🚀 Performance & Size Optimization Report

| Optimization | Result |
| :--- | :--- |
| 🗑️ Duplicate root files removed | **118** files dropped |
| 🖼️ Unreferenced assets removed | **54** unused mockups |
| 📉 `static/` directory | 24.20 MB → **3.83 MB** (**−84.2%**) |
| 📦 Total runtime payload | ~59.2 MB → **8.71 MB** (**−85.3%**) |
| ⚡ WSGI concurrency | Gunicorn · 2 workers × 4 threads |

---

## 🧭 Known Limitations & Future Scope

1. **MySQL Offline Fallback** — Without an external MySQL instance, the app uses precomputed analytics. To attach one, set `DB_HOST`, `DB_USER`, and `DB_PASSWORD` in your cloud dashboard.
2. **Catalog Horizon** — Data covers additions through 2020. Scripts in `src/data_cleaning.py` are modular and ready for refreshed Kaggle datasets.

---

## 📜 License & Attributions

- **Code & Application**: [MIT License](LICENSE)
- **Dataset**: Shivam Bansal on [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- **Design Inspiration**: Modern dark-mode aesthetic standards

<div align="center">

<br>

**⭐ If you found this project useful, consider giving it a star! ⭐**

[🚀 View Live Demo](https://netflix-analytics-2uzs.onrender.com/)

</div>