"""
Automated unit tests for data cleaning module (src/data_cleaning.py).
Tests use isolated synthetic fixtures without modifying production data.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import (
    validate_columns,
    inspect_missing_values,
    clean_dates,
    clean_duration,
    remove_or_report_duplicates,
    clean_dataset
)


@pytest.fixture
def sample_raw_data():
    """Provides a synthetic test DataFrame covering various data edge cases."""
    return pd.DataFrame({
        'show_id': [101, 102, 103, 104, 105],
        'type': ['Movie', 'TV Show', 'Movie', 'TV Show', 'Movie'],
        'title': ['Film Alpha ', ' Series Beta', 'Film Gamma', 'Series Delta', 'Film Epsilon'],
        'director': ['Director A', None, 'Director B, Director C', None, 'Director D'],
        'cast': ['Actor 1, Actor 2', 'Actor 3', None, 'Actor 4', 'Actor 5'],
        'country': ['United States', 'India, United States', None, 'United Kingdom', 'Canada'],
        'date_added': [' September 9, 2019 ', 'March 15, 2020', 'invalid-date', None, 'January 1, 2018'],
        'release_year': [2019, 2020, 2018, 2015, 1999],
        'rating': ['TV-MA', 'TV-14', 'R', None, 'PG-13'],
        'duration': ['90 min', '2 Seasons', '120 min', '1 Season', 'invalid_duration'],
        'listed_in': ['Dramas, Comedies', 'International TV Shows', 'Action & Adventure', 'TV Dramas', 'Documentaries'],
        'description': ['Description Alpha', 'Description Beta', 'Description Gamma', 'Description Delta', 'Description Epsilon']
    })


def test_validate_columns_success(sample_raw_data):
    """Test that complete required schema passes validation."""
    assert validate_columns(sample_raw_data) is True


def test_validate_columns_missing():
    """Test that missing required columns raise ValueError."""
    incomplete_df = pd.DataFrame({'show_id': [1], 'title': ['Test']})
    with pytest.raises(ValueError) as excinfo:
        validate_columns(incomplete_df)
    assert "missing required columns" in str(excinfo.value)


def test_inspect_missing_values(sample_raw_data):
    """Test missing value inspection statistics."""
    stats = inspect_missing_values(sample_raw_data)
    assert stats['total_rows'] == 5
    assert stats['counts']['director'] == 2
    assert stats['percentages']['director'] == 40.0


def test_clean_dates_parsing(sample_raw_data):
    """Test parsing dates into clean ISO format and extracted year/month."""
    cleaned = clean_dates(sample_raw_data)
    assert 'date_added_clean' in cleaned.columns
    assert 'year_added' in cleaned.columns
    assert 'month_added' in cleaned.columns
    # Row 0: ' September 9, 2019 ' -> 2019-09-09, year 2019, month 9
    assert cleaned.loc[0, 'date_added_clean'] == '2019-09-09'
    assert cleaned.loc[0, 'year_added'] == 2019
    assert cleaned.loc[0, 'month_added'] == 9
    # Invalid date handled gracefully
    assert pd.isna(cleaned.loc[2, 'date_added_clean'])


def test_clean_duration_separation(sample_raw_data):
    """Test decomposition of duration into minutes vs seasons."""
    cleaned = clean_duration(sample_raw_data)
    # Movie 90 min
    assert cleaned.loc[0, 'duration_minutes'] == 90
    assert pd.isna(cleaned.loc[0, 'seasons_count'])
    # TV Show 2 Seasons
    assert cleaned.loc[1, 'seasons_count'] == 2
    assert pd.isna(cleaned.loc[1, 'duration_minutes'])
    # Movie 120 min
    assert cleaned.loc[2, 'duration_minutes'] == 120


def test_remove_or_report_duplicates():
    """Test deduplication by show_id."""
    dups_df = pd.DataFrame({
        'show_id': [1, 1, 2],
        'type': ['Movie', 'Movie', 'TV Show'],
        'title': ['A', 'A duplicate', 'B']
    })
    deduped = remove_or_report_duplicates(dups_df)
    assert len(deduped) == 2
    assert list(deduped['show_id']) == [1, 2]


def test_clean_dataset_pipeline(sample_raw_data):
    """Test the full end-to-end cleaning pipeline on synthetic data."""
    cleaned = clean_dataset(sample_raw_data)
    assert len(cleaned) == 5
    # Verify string trimming
    assert cleaned.loc[0, 'title'] == 'Film Alpha'
    assert cleaned.loc[1, 'title'] == 'Series Beta'
    # Verify output columns
    expected_new_cols = ['date_added_clean', 'year_added', 'month_added', 'duration_minutes', 'seasons_count']
    for col in expected_new_cols:
        assert col in cleaned.columns


def test_clean_empty_dataset():
    """Test that an empty DataFrame with required schema is handled without crashes."""
    empty_df = pd.DataFrame(columns=[
        'show_id', 'type', 'title', 'director', 'cast', 'country',
        'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description'
    ])
    cleaned = clean_dataset(empty_df)
    assert len(cleaned) == 0
    assert 'duration_minutes' in cleaned.columns
