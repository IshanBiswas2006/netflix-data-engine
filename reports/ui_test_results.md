# UI Test Results & Asset Verification Report

**Date**: 2026-10-12  
**Target URL**: `http://localhost:5000/`  
**Test Suite**: Route Responses, Static Assets, and CSS/Typography Load Integrity

---

## 1. Route Response & Markup Verification

| Route | HTTP Status | Response Size | Layout Elements Verified |
| :--- | :--- | :--- | :--- |
| `GET /` | `200 OK` | 15,015 bytes | Header, Hero, 4 Stat Cards, 3 Feature Cards, Recent Titles Table, Footer |
| `GET /analysis` | `200 OK` | 16,319 bytes | Content Type Table, Runtime Stats, Top 10 Countries, Top 10 Genres, Longest Content |
| `GET /visualizations` | `200 OK` | 11,110 bytes | 8 Figure Cards, Matplotlib Chart Images, Insights Callouts |
| `GET /sql-queries` | `200 OK` | 53,429 bytes | 10 Query Accordions, Code Blocks, Dynamic Search Input, Execution Results |
| `GET /about` | `200 OK` | 9,195 bytes | Methodology, Pipeline Steps, Tech Stack Badges, Limitations |

---

## 2. Static Asset Availability

| Asset Path | HTTP Status | Content Type | Verification Note |
| :--- | :--- | :--- | :--- |
| `/static/css/style.css` | `200 OK` | `text/css` | Design system tokens, typography rules, layout breakpoints |
| `/static/js/main.js` | `200 OK` | `application/javascript` | Accordion toggling, table search, mobile drawer |
| `/static/icons/default-favicon-dark.v1.png` | `200 OK` | `image/png` | Favicon loaded |
| `/static/images/charts/01_movies_vs_tv_shows.png` | `200 OK` | `image/png` | High-res donut chart (49.8 KB) |
| `/static/images/charts/02_titles_by_release_year.png` | `200 OK` | `image/png` | High-res line trend (95.2 KB) |
| `/static/images/charts/03_top_10_countries.png` | `200 OK` | `image/png` | High-res country bar chart (75.7 KB) |
| `/static/images/charts/04_top_10_genres.png` | `200 OK` | `image/png` | High-res genre bar chart (92.1 KB) |
| `/static/images/charts/05_content_rating_distribution.png` | `200 OK` | `image/png` | High-res rating bar chart (59.2 KB) |
| `/static/images/charts/06_movie_duration_distribution.png` | `200 OK` | `image/png` | High-res runtime histogram (69.7 KB) |
| `/static/images/charts/07_tv_show_seasons_distribution.png` | `200 OK` | `image/png` | High-res seasons distribution (72.1 KB) |
| `/static/images/charts/08_titles_added_over_time.png` | `200 OK` | `image/png` | High-res ingestion velocity chart (80.8 KB) |

---

## 3. Interaction Verification
- **Header sticky positioning**: Functional with frosted glass backdrop filter.
- **Accordion expand/collapse**: Functional on query headers.
- **Real-time table search**: Functional filtering table rows based on user input.
- **Card hover lifts**: Functional with smooth cubic-bezier transitions.
