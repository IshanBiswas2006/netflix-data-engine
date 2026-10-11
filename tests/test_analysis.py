"""
Automated unit tests for exploratory data analysis module (src/data_analysis.py).
Tests use synthetic fixtures where mathematical results are pre-calculated and verified.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_analysis import (
    get_catalog_overview,
    get_content_type_distribution,
    get_release_year_distribution,
    get_top_countries,
    get_top_genres,
    get_rating_distribution,
    get_movie_duration_stats,
    get_tv_seasons_stats,
    get_additions_over_time
)


@pytest.fixture
def synthetic_cleaned_df():
    """Provides a controlled dataset with known aggregate outcomes."""
    return pd.DataFrame({
        'show_id': [1, 2, 3, 4, 5, 6],
        'type': ['Movie', 'Movie', 'Movie', 'TV Show', 'TV Show', 'Movie'],
        'title': ['M1', 'M2', 'M3', 'T1', 'T2', 'M4'],
        'country': ['United States', 'India, United States', 'United Kingdom', 'United States', 'India', 'France'],
        'release_year': [2018, 2019, 2020, 2019, 2020, 2015],
        'rating': ['TV-MA', 'TV-MA', 'TV-14', 'TV-14', 'R', None],
        'duration_minutes': [100, 120, 80, np.nan, np.nan, 90],
        'seasons_count': [np.nan, np.nan, np.nan, 1, 3, np.nan],
        'year_added': [2019, 2019, 2020, 2020, 2018, 2017],
        'listed_in': ['Dramas, Comedies', 'Dramas', 'Action & Adventure', 'TV Dramas', 'Comedies', 'Dramas']
    })


def test_get_catalog_overview(synthetic_cleaned_df):
    """Test catalog overview statistics calculation."""
    overview = get_catalog_overview(synthetic_cleaned_df)
    assert overview['total_titles'] == 6
    assert overview['movies_count'] == 4
    assert overview['tv_shows_count'] == 2
    assert overview['movie_percentage'] == 66.67
    assert overview['tv_show_percentage'] == 33.33
    assert overview['earliest_release_year'] == 2015
    assert overview['latest_release_year'] == 2020


def test_get_content_type_distribution(synthetic_cleaned_df):
    """Test content type distribution table."""
    dist = get_content_type_distribution(synthetic_cleaned_df)
    assert len(dist) == 2
    assert dist.loc[dist['type'] == 'Movie', 'count'].values[0] == 4
    assert dist.loc[dist['type'] == 'TV Show', 'count'].values[0] == 2


def test_get_top_countries(synthetic_cleaned_df):
    """Test exploding multi-country entries."""
    top_c = get_top_countries(synthetic_cleaned_df, top_n=5)
    # United States appears in rows 0, 1, 3 -> count 3
    us_count = top_c.loc[top_c['country'] == 'United States', 'count'].values[0]
    assert us_count == 3
    # India appears in rows 1, 4 -> count 2
    india_count = top_c.loc[top_c['country'] == 'India', 'count'].values[0]
    assert india_count == 2


def test_get_top_genres(synthetic_cleaned_df):
    """Test exploding multi-genre entries."""
    top_g = get_top_genres(synthetic_cleaned_df, top_n=5)
    # Dramas appears in rows 0, 1, 5 -> count 3
    dramas_count = top_g.loc[top_g['genre'] == 'Dramas', 'count'].values[0]
    assert dramas_count == 3


def test_get_movie_duration_stats(synthetic_cleaned_df):
    """Test movie duration statistics (80, 90, 100, 120 -> mean 97.5, median 95)."""
    stats = get_movie_duration_stats(synthetic_cleaned_df)
    assert stats['count'] == 4
    assert stats['min'] == 80
    assert stats['max'] == 120
    assert stats['mean'] == 97.5
    assert stats['median'] == 95.0


def test_get_tv_seasons_stats(synthetic_cleaned_df):
    """Test TV show seasons statistics (1, 3 -> 50% single season)."""
    stats = get_tv_seasons_stats(synthetic_cleaned_df)
    assert stats['count'] == 2
    assert stats['min'] == 1
    assert stats['max'] == 3
    assert stats['single_season_pct'] == 50.0


def test_get_additions_over_time(synthetic_cleaned_df):
    """Test timeline grouping of additions by year."""
    additions = get_additions_over_time(synthetic_cleaned_df)
    assert len(additions) == 4  # 2017, 2018, 2019, 2020
    row_2019 = additions.loc[additions['year_added'] == 2019, 'count'].values[0]
    assert row_2019 == 2
