"""
Netflix Movies and TV Shows Data Cleaning Module
Handles loading, validation, normalization, datetime parsing,
duration decomposition, and reproducible export.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import RAW_DATA_PATH, PROCESSED_DATA_PATH

REQUIRED_COLUMNS = [
    'show_id', 'type', 'title', 'director', 'cast', 'country',
    'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description'
]


def load_raw_data(filepath=RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load the raw dataset from CSV file.
    Preserves original data without mutations.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {path}")
    df = pd.read_csv(path)
    return df


def validate_columns(df: pd.DataFrame) -> bool:
    """
    Validate that all required columns are present in the DataFrame.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    return True


def inspect_missing_values(df: pd.DataFrame) -> dict:
    """
    Inspect and return counts and percentages of missing values per column.
    """
    null_counts = df.isnull().sum().to_dict()
    total = len(df)
    null_pct = {col: round((count / total) * 100, 2) if total > 0 else 0.0
                for col, count in null_counts.items()}
    return {
        'counts': null_counts,
        'percentages': null_pct,
        'total_rows': total
    }


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse date_added into valid datetime representations.
    Extracts year_added and month_added as separate fields.
    Preserves NaNs for unrecorded addition dates.
    """
    cleaned_df = df.copy()
    if 'date_added' in cleaned_df.columns:
        date_series = cleaned_df['date_added'].astype(str).str.strip()
        date_series = date_series.replace({'nan': np.nan, 'None': np.nan, '': np.nan})
        
        parsed_dates = pd.to_datetime(date_series, errors='coerce', format='mixed')
        cleaned_df['date_added_clean'] = parsed_dates.dt.strftime('%Y-%m-%d')
        cleaned_df['year_added'] = parsed_dates.dt.year.astype('Int64')
        cleaned_df['month_added'] = parsed_dates.dt.month.astype('Int64')
    return cleaned_df


def clean_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Decompose composite duration column into:
    - duration_minutes (numeric, for Movies)
    - seasons_count (numeric, for TV Shows)
    """
    cleaned_df = df.copy()
    cleaned_df['duration_minutes'] = pd.Series(dtype='Int64')
    cleaned_df['seasons_count'] = pd.Series(dtype='Int64')

    if 'duration' in cleaned_df.columns and 'type' in cleaned_df.columns:
        # Extract digits
        duration_num = cleaned_df['duration'].astype(str).str.extract(r'(\d+)')[0]
        numeric_vals = pd.to_numeric(duration_num, errors='coerce').astype('Int64')

        is_movie = cleaned_df['type'].str.strip().str.lower() == 'movie'
        is_tv = cleaned_df['type'].str.strip().str.lower() == 'tv show'

        cleaned_df.loc[is_movie, 'duration_minutes'] = numeric_vals[is_movie]
        cleaned_df.loc[is_tv, 'seasons_count'] = numeric_vals[is_tv]

    return cleaned_df


def remove_or_report_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and deduplicate by show_id and exact row duplicates.
    Reports duplicate counts.
    """
    initial_len = len(df)
    # Check exact row duplicates
    exact_dups = df.duplicated().sum()
    # Check show_id duplicates
    id_dups = df['show_id'].duplicated().sum()

    # Drop duplicate show_id, keeping the first occurrence
    cleaned_df = df.drop_duplicates(subset=['show_id'], keep='first').copy()
    dropped_count = initial_len - len(cleaned_df)

    return cleaned_df


def clean_dataset(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Full data cleaning pipeline:
    1. Validate required columns.
    2. Normalize string columns (strip whitespace).
    3. Remove or report duplicates.
    4. Clean and decompose dates.
    5. Clean and decompose durations.
    6. Ensure numeric types for release_year.
    """
    validate_columns(raw_df)
    df = raw_df.copy()

    # Normalize string columns
    str_cols = ['type', 'title', 'director', 'cast', 'country', 'rating', 'listed_in', 'description']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

    # Release year numeric validation
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')

    # Deduplicate
    df = remove_or_report_duplicates(df)

    # Date parsing
    df = clean_dates(df)

    # Duration parsing
    df = clean_duration(df)

    return df


def save_cleaned_data(df: pd.DataFrame, output_path=PROCESSED_DATA_PATH) -> Path:
    """
    Save the cleaned dataset to CSV reproducibly.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def run_pipeline() -> pd.DataFrame:
    """
    Command-line execution runner for cleaning pipeline.
    """
    print(f"Loading raw data from: {RAW_DATA_PATH}")
    raw_df = load_raw_data(RAW_DATA_PATH)
    print(f"Raw records loaded: {len(raw_df)}")

    missing_info = inspect_missing_values(raw_df)
    print(f"Missing attributes: {missing_info['counts']}")

    cleaned_df = clean_dataset(raw_df)
    print(f"Cleaned records: {len(cleaned_df)}")

    saved_path = save_cleaned_data(cleaned_df, PROCESSED_DATA_PATH)
    print(f"Cleaned dataset saved successfully to: {saved_path}")

    return cleaned_df


if __name__ == '__main__':
    run_pipeline()
