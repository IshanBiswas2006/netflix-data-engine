# Key Analytical Findings Report

## Dataset: Netflix Movies and TV Shows (`data/processed/netflix_cleaned.csv`)
**Total Records Analyzed**: 6,234 unique titles

---

### Finding 1: Catalog Composition — Film Dominance
- **Movies**: 4,265 titles (**68.42%**)
- **TV Shows**: 1,969 titles (**31.58%**)
- *Interpretation*: The Netflix catalog is overwhelmingly composed of standalone films (~2.17 movies for every 1 TV show). Standalone movies offer immediate variety, whereas episodic TV shows generate ongoing subscriber watch time.

---

### Finding 2: Geographic Content Production Hotspots
*Methodology: Exploded multi-nation co-productions into individual country occurrences to prevent double-counting bias while capturing all creative contributions.*
- **Top 10 Producing Countries**:
  1. **United States**: 2,610 titles
  2. **India**: 838 titles
  3. **United Kingdom**: 602 titles
  4. **Canada**: 318 titles
  5. **France**: 271 titles
  6. **Japan**: 231 titles
  7. **Spain**: 178 titles
  8. **South Korea**: 162 titles
  9. **Germany**: 151 titles
  10. **Mexico**: 129 titles
- *Interpretation*: While the United States remains the primary production source (over 41% of geographic associations), India ranks as a prominent second, followed closely by the UK, France, Japan, and South Korea, highlighting significant regional investment in Bollywood, anime, and K-drama markets.

---

### Finding 3: Genre and Categorical Leadership
*Methodology: Individual genre category extraction from multi-genre listings.*
- **Top 10 Genres**:
  1. **International Movies**: 1,927 titles
  2. **Dramas**: 1,623 titles
  3. **Comedies**: 1,113 titles
  4. **International TV Shows**: 1,001 titles
  5. **Documentaries**: 668 titles
  6. **TV Dramas**: 599 titles
  7. **Action & Adventure**: 597 titles
  8. **Independent Movies**: 552 titles
  9. **TV Comedies**: 436 titles
  10. **Thrillers**: 392 titles
- *Interpretation*: "International" classifications lead across both film and television, representing global licensing efforts and localized originals tailored for international subscriber expansion.

---

### Finding 4: Audience Maturity Demographics
- **TV-MA (Mature Audiences)**: 2,027 titles (32.52%)
- **TV-14 (Parents Strongly Cautioned)**: 1,698 titles (27.24%)
- **TV-PG (Parental Guidance)**: 701 titles (11.25%)
- **R (Restricted / 17+)**: 508 titles (8.15%)
- **PG-13**: 286 titles (4.59%)
- **All Others / Family (TV-Y, TV-G, etc.)**: 1,014 titles (16.27%)
- *Interpretation*: Nearly 60% of the entire library is rated TV-MA or TV-14, indicating a strategic focus on adolescent and adult demographics over purely young children content.

---

### Finding 5: Runtime and Seasonality Dynamics
- **Movie Runtime**:
  - Minimum: 3 minutes (Silent/Micro-short film)
  - 25th Percentile: 86.0 minutes
  - Median: 98.0 minutes
  - Mean: 99.1 minutes
  - 75th Percentile: 115.0 minutes
  - Maximum: 312 minutes (*Black Mirror: Bandersnatch* interactive narrative)
  - Other top runtimes: *Sangam* (228 min), *Lagaan* (224 min), *Jodhaa Akbar* (214 min), *The Irishman* (209 min).
- **TV Show Season Lengths**:
  - 1 Season: 1,321 shows (**67.09%** of all TV shows)
  - 2 Seasons: 304 shows (15.44%)
  - 3 Seasons: 158 shows (8.02%)
  - 4+ Seasons: 186 shows (9.45%)
  - Longest series: *Grey's Anatomy* (15 seasons), *NCIS* (15 seasons), *Supernatural* (14 seasons), *Red vs. Blue* (13 seasons).
- *Interpretation*: Two-thirds of all TV shows only have a single season, highlighting rapid series testing, limited mini-series structures, and early cancellations.

---

### Finding 6: Content Ingestion Timeline vs. Release Year
- **Theatrical Release vs Digital Addition**:
  - The earliest release year is **1925** (*Pioneers: First Women Filmmakers*).
  - Digital addition onto Netflix began in **2008** (2 titles) and remained modest through 2014 (25 titles).
  - Ingestion experienced exponential acceleration:
    - 2015: 90 additions
    - 2016: 456 additions
    - 2017: 1,300 additions
    - 2018: 1,782 additions
    - 2019: **2,349 additions** (Peak historical velocity)
- *Interpretation*: Netflix's transition to an aggressive catalog aggregator and global streaming leader accelerated markedly from 2016 onward, peaking in 2019 prior to studio licensing reclamation by competing direct-to-consumer platforms (Disney+, HBO Max).
