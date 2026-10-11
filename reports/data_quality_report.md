# Data Quality Report

## Dataset: Netflix Movies and TV Shows (`data/raw/netflix_titles.csv`)

### 1. Executive Summary
- **Source**: Kaggle / Shivam Bansal Netflix Shows Catalog
- **File Size**: 2,410,660 bytes
- **Total Records**: 6,234 rows
- **Total Attributes**: 12 columns
- **Primary Key Integrity**: `show_id` is 100% unique across all 6,234 rows with zero duplicates.
- **Record Integrity**: 0 complete duplicate rows detected.

---

### 2. Schema Specification & Attribute Audit

| Column Name | Raw Data Type | Non-Null Count | Null Count | Null % | Detected Format / Nature |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `show_id` | `int64` | 6,234 | 0 | 0.00% | Unique integer identifier (e.g., `81145628`) |
| `type` | `object` | 6,234 | 0 | 0.00% | Binary categorical: `Movie` (4,265), `TV Show` (1,969) |
| `title` | `object` | 6,234 | 0 | 0.00% | Media title string (UTF-8) |
| `director` | `object` | 4,265 | 1,969 | 31.58% | Comma-separated director names; high missingness in TV shows |
| `cast` | `object` | 5,664 | 570 | 9.14% | Comma-separated actor/actress names |
| `country` | `object` | 5,758 | 476 | 7.64% | Primary / co-producing countries (comma-separated) |
| `date_added` | `object` | 6,223 | 11 | 0.18% | Date string (e.g., `"September 9, 2019"`); contains leading whitespace |
| `release_year` | `int64` | 6,234 | 0 | 0.00% | Theatrical / broadcast release year (Range: 1925 – 2020) |
| `rating` | `object` | 6,224 | 10 | 0.16% | Content maturity rating (TV-MA, TV-14, R, PG-13, etc.) |
| `duration` | `object` | 6,234 | 0 | 0.00% | Composite string (minutes for movies, seasons for TV shows) |
| `listed_in` | `object` | 6,234 | 0 | 0.00% | Comma-separated category/genre classifications |
| `description` | `object` | 6,234 | 0 | 0.00% | Synopsis / summary textual narrative |

---

### 3. Missing Value Analysis & Business Implications
1. **`director` (31.58% Missing)**:
   - High missing rate is predominantly driven by episodic TV shows where directorial credits vary by episode or are uncredited in catalog metadata.
   - *Strategy*: Do not drop rows. Retain missing values as `None`/`NaN` or explicit indicator where appropriate to preserve catalog completeness.
2. **`cast` (9.14% Missing)**:
   - Missing in certain documentaries, animations, or unlisted productions.
   - *Strategy*: Retain rows; exclude only when running cast-specific co-occurrence queries.
3. **`country` (7.64% Missing)**:
   - 476 entries lack production country metadata.
   - *Strategy*: Retain catalog records; exclude missing countries during geographic rankings rather than misattributing to "Unknown" or arbitrary nations.
4. **`date_added` (0.18% Missing)**:
   - 11 entries lack an official digital addition timestamp.
   - *Strategy*: Parse valid dates into `datetime64[ns]`; retain nulls for addition timeline calculations.
5. **`rating` (0.16% Missing)**:
   - 10 entries lack an official age rating.
   - *Strategy*: Tag as `Unrated` / `NR` or preserve `None`.

---

### 4. Structural Issues & Data Quality Flags
- **Duration Homogeneity**: The `duration` attribute combines two fundamentally different measurement units:
  - Movies: Measured in elapsed runtime minutes (e.g., `90 min`, `124 min`).
  - TV Shows: Measured in cumulative season counts (e.g., `1 Season`, `3 Seasons`).
  - *Correction Needed*: Split into separate numeric columns `duration_minutes` (for Movies) and `seasons_count` (for TV Shows).
- **Whitespace & String Inconsistencies**: Several strings contain unstripped leading and trailing spaces (notably in `date_added`, `title`, and `country`).
- **Multi-Valued Fields**: `country`, `listed_in`, `director`, and `cast` contain comma-separated entries. For accurate category aggregations, individual elements must be parsed and trimmed without double-counting unique titles.

---

### 5. Quality Conclusion
The raw dataset is structurally intact, has 100% unique primary keys, zero duplicate rows, and valid ranges across core numerical dimensions. Systematic cleaning can proceed deterministically.
