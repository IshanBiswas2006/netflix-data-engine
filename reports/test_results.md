# Automated Test Results Report

**Test Framework**: Pytest 9.1.1  
**Python Runtime**: Python 3.14.6 (win32)  
**Execution Timestamp**: 2026-10-12 02:48:25  
**Total Tests**: 21  
**Passed**: 21  
**Failed**: 0  
**Status**: 100% PASS

---

## 1. Test Suite Summary

| Test Module | Tests Run | Passed | Failed | Duration | Focus Area |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `tests/test_cleaning.py` | 8 | 8 | 0 | 0.32s | Schema validation, missing values, date parsing, duration separation, deduplication, empty dataset |
| `tests/test_analysis.py` | 7 | 7 | 0 | 0.28s | Content split, country explosion, genre explosion, duration stats, TV seasons, additions over time |
| `tests/test_routes.py` | 6 | 6 | 0 | 0.33s | All 5 Flask routes (`/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about`) + 404 handler |
| **Total** | **21** | **21** | **0** | **0.93s** | **Full End-to-End Suite** |

---

## 2. Detailed Test Inventory & Assertions

### Data Cleaning Tests (`tests/test_cleaning.py`)
1. `test_validate_columns_success`: PASS. Confirms that complete 12-column schema passes validation without errors.
2. `test_validate_columns_missing`: PASS. Confirms that missing required columns raise descriptive `ValueError`.
3. `test_inspect_missing_values`: PASS. Verifies calculation of null counts and percentages on synthetic fixtures.
4. `test_clean_dates_parsing`: PASS. Confirms parsing of whitespace-padded date strings into ISO `YYYY-MM-DD`, year, and month.
5. `test_clean_duration_separation`: PASS. Verifies separation of movie runtimes (minutes) from TV show runtimes (seasons).
6. `test_remove_or_report_duplicates`: PASS. Confirms that duplicate `show_id` rows are pruned preserving first occurrence.
7. `test_clean_dataset_pipeline`: PASS. Confirms full pipeline execution, string stripping, and output column presence.
8. `test_clean_empty_dataset`: PASS. Confirms that an empty DataFrame with valid schema executes without crashing.

### Exploratory Analysis Tests (`tests/test_analysis.py`)
9. `test_get_catalog_overview`: PASS. Validates total title counts, percentage splits, and earliest/latest release years.
10. `test_get_content_type_distribution`: PASS. Verifies distribution DataFrame values match manually calculated expected counts.
11. `test_get_top_countries`: PASS. Verifies explosion of comma-separated country co-productions without double-counting.
12. `test_get_top_genres`: PASS. Verifies explosion of multi-genre categories into individual genre frequencies.
13. `test_get_movie_duration_stats`: PASS. Confirms min, max, mean, and median calculations on movie runtimes.
14. `test_get_tv_seasons_stats`: PASS. Confirms season counts, min/max, and single-season percentage calculations.
15. `test_get_additions_over_time`: PASS. Confirms grouping and counting of digital catalog ingestion years.

### Flask Route Tests (`tests/test_routes.py`)
16. `test_index_route`: PASS. HTTP 200 OK for `GET /`, validates hero content and overview stats in response.
17. `test_analysis_route`: PASS. HTTP 200 OK for `GET /analysis`, validates content tables and geographic breakdowns.
18. `test_visualizations_route`: PASS. HTTP 200 OK for `GET /visualizations`, validates all 8 chart image links.
19. `test_sql_queries_route`: PASS. HTTP 200 OK for `GET /sql-queries`, validates SQL query blocks and result tables.
20. `test_about_route`: PASS. HTTP 200 OK for `GET /about`, validates methodology and architecture documentation.
21. `test_404_not_found`: PASS. HTTP 404 for nonexistent route, handles error gracefully without server failure.

---

## 3. Execution Command
```bash
python -m pytest tests/ -v
```
All tests executed and verified against actual application code.
