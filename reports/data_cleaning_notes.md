# Data Cleaning Notes & Methodological Rationale

## Project: Netflix Movies and TV Shows Analysis
**Source**: `data/raw/netflix_titles.csv`  
**Destination**: `data/processed/netflix_cleaned.csv`  
**Execution Script**: `src/data_cleaning.py`

---

## 1. Column Transformations & Decomposition
1. **Duration Splitting**:
   - *Problem*: The raw `duration` attribute combined movie runtimes in minutes (`"90 min"`) and TV show episode lengths in season counts (`"1 Season"`).
   - *Action*: Extracted the numeric string component using regular expression `r'(\d+)'`.
   - *Result*:
     - Created `duration_minutes` (`Int64`): Populated for all 4,265 movies (range: 3 – 312 minutes, mean: 99.1 minutes). TV shows remain `NaN`.
     - Created `seasons_count` (`Int64`): Populated for all 1,969 TV shows (range: 1 – 15 seasons, median: 1 season). Movies remain `NaN`.
     - Preserves the original `duration` string column for verification and traceability.

2. **Date Added Normalization**:
   - *Problem*: `date_added` strings featured leading and trailing whitespace and human-formatted textual representations (`" September 9, 2019 "`).
   - *Action*: Stripped whitespace and parsed with `pd.to_datetime(format='mixed', errors='coerce')`.
   - *Result*:
     - `date_added_clean`: Formatted as ISO-8601 (`YYYY-MM-DD`). 6,223 dates successfully parsed.
     - `year_added`: Extracted numeric calendar year of addition to Netflix (2008 – 2020).
     - `month_added`: Extracted numeric calendar month (1 – 12).
     - 11 records with unrecorded addition timestamps were preserved as `NaN` rather than imputed with synthetic dates.

3. **String Standardization**:
   - Applied `.str.strip()` across `type`, `title`, `director`, `cast`, `country`, `rating`, `listed_in`, and `description`.
   - Converted placeholder strings like `""`, `"None"`, `"nan"` into canonical `np.nan` values.

4. **Deduplication Audit**:
   - Assessed duplicate rows: 0 exact row duplicates.
   - Evaluated `show_id` uniqueness: All 6,234 IDs are distinct; 0 dropped rows.

---

## 2. Row Summary Statistics

| Dimension | Raw Count | Processed Count | Affected / Transformed Rows |
| :--- | :--- | :--- | :--- |
| Total Catalog Records | 6,234 | 6,234 | 6,234 (100% normalized) |
| Movies | 4,265 | 4,265 | 4,265 assigned `duration_minutes` |
| TV Shows | 1,969 | 1,969 | 1,969 assigned `seasons_count` |
| Date Added Parsed | 6,223 | 6,223 | 6,223 parsed to ISO date |
| Date Added Missing | 11 | 11 | 11 retained as `NaN` |
| Ratings Missing | 10 | 10 | 10 retained as `NaN` |

---

## 3. How to Run Data Cleaning
```bash
python src/data_cleaning.py
```
Outputs verified clean CSV to `data/processed/netflix_cleaned.csv`.
