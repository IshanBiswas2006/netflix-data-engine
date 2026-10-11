"""
Netflix Movies and TV Shows Data Analysis Module
Performs exploratory data analysis, computes aggregate statistics,
and prepares structured results for visualizations, SQL comparison, and Flask routes.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import PROCESSED_DATA_PATH


def load_processed_data(filepath=PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Load cleaned dataset from processed CSV."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at: {path}")
    return pd.read_csv(path)


def get_catalog_overview(df: pd.DataFrame) -> dict:
    """
    Compute top-level summary metrics for catalog overview.
    """
    total_titles = len(df)
    movies_count = int((df['type'] == 'Movie').sum())
    tv_count = int((df['type'] == 'TV Show').sum())

    movie_pct = round((movies_count / total_titles) * 100, 2) if total_titles else 0.0
    tv_pct = round((tv_count / total_titles) * 100, 2) if total_titles else 0.0

    earliest_release = int(df['release_year'].min()) if not df['release_year'].dropna().empty else 0
    latest_release = int(df['release_year'].max()) if not df['release_year'].dropna().empty else 0

    return {
        'total_titles': total_titles,
        'movies_count': movies_count,
        'tv_shows_count': tv_count,
        'movie_percentage': movie_pct,
        'tv_show_percentage': tv_pct,
        'earliest_release_year': earliest_release,
        'latest_release_year': latest_release,
        'avg_movie_duration_min': round(df['duration_minutes'].mean(), 1) if 'duration_minutes' in df.columns else 0.0,
        'avg_tv_seasons': round(df['seasons_count'].mean(), 1) if 'seasons_count' in df.columns else 0.0
    }


def get_content_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return distribution of Movies vs TV Shows.
    """
    counts = df['type'].value_counts().reset_index()
    counts.columns = ['type', 'count']
    counts['percentage'] = (counts['count'] / len(df) * 100).round(2)
    return counts


def get_release_year_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return count of titles per release year sorted chronologically.
    """
    dist = df['release_year'].dropna().astype(int).value_counts().sort_index().reset_index()
    dist.columns = ['release_year', 'count']
    return dist


def get_top_countries(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Explode comma-separated country entries to avoid miscounting co-productions.
    Returns top N producing countries.
    """
    s = df['country'].dropna().astype(str).str.split(',').explode().str.strip()
    s = s[s != '']
    top = s.value_counts().head(top_n).reset_index()
    top.columns = ['country', 'count']
    return top


def get_top_genres(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Explode comma-separated listed_in categories.
    Returns top N genres.
    """
    s = df['listed_in'].dropna().astype(str).str.split(',').explode().str.strip()
    s = s[s != '']
    top = s.value_counts().head(top_n).reset_index()
    top.columns = ['genre', 'count']
    return top


def get_rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return content ratings distribution ordered by title count descending.
    """
    dist = df['rating'].fillna('Unrated').value_counts().reset_index()
    dist.columns = ['rating', 'count']
    dist['percentage'] = (dist['count'] / len(df) * 100).round(2)
    return dist


def get_movie_duration_stats(df: pd.DataFrame) -> dict:
    """
    Compute descriptive statistics for movie runtime in minutes.
    """
    movies = df[df['type'] == 'Movie']['duration_minutes'].dropna()
    if movies.empty:
        return {}
    return {
        'count': int(movies.count()),
        'mean': round(float(movies.mean()), 2),
        'median': round(float(movies.median()), 2),
        'std': round(float(movies.std()), 2),
        'min': int(movies.min()),
        'max': int(movies.max()),
        'q25': round(float(movies.quantile(0.25)), 2),
        'q75': round(float(movies.quantile(0.75)), 2)
    }


def get_tv_seasons_stats(df: pd.DataFrame) -> dict:
    """
    Compute descriptive statistics for TV show seasons.
    """
    tv = df[df['type'] == 'TV Show']['seasons_count'].dropna()
    if tv.empty:
        return {}
    return {
        'count': int(tv.count()),
        'mean': round(float(tv.mean()), 2),
        'median': round(float(tv.median()), 2),
        'min': int(tv.min()),
        'max': int(tv.max()),
        'single_season_pct': round((tv == 1).sum() / len(tv) * 100, 2)
    }


def get_additions_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return yearly addition counts to Netflix catalog.
    """
    years = df['year_added'].dropna().astype(int).value_counts().sort_index().reset_index()
    years.columns = ['year_added', 'count']
    return years


def get_top_directors(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Explode comma-separated directors and count titles.
    """
    s = df['director'].dropna().astype(str).str.split(',').explode().str.strip()
    s = s[s != '']
    top = s.value_counts().head(top_n).reset_index()
    top.columns = ['director', 'count']
    return top


def get_longest_movies(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Return top N longest movies with runtime in minutes.
    """
    movies = df[df['type'] == 'Movie'].dropna(subset=['duration_minutes'])
    longest = movies.sort_values(by='duration_minutes', ascending=False).head(top_n)
    return longest[['title', 'duration_minutes', 'release_year', 'country']]


def get_tv_shows_most_seasons(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Return top N TV shows with the most seasons.
    """
    tv = df[df['type'] == 'TV Show'].dropna(subset=['seasons_count'])
    longest = tv.sort_values(by='seasons_count', ascending=False).head(top_n)
    return longest[['title', 'seasons_count', 'release_year', 'country']]


def get_full_summary(df=None) -> dict:
    """
    Compile complete analytical summary dict.
    """
    if df is None:
        df = load_processed_data()
    return {
        'overview': get_catalog_overview(df),
        'content_type': get_content_type_distribution(df).to_dict(orient='records'),
        'top_countries': get_top_countries(df, 10).to_dict(orient='records'),
        'top_genres': get_top_genres(df, 10).to_dict(orient='records'),
        'ratings': get_rating_distribution(df).to_dict(orient='records'),
        'movie_stats': get_movie_duration_stats(df),
        'tv_stats': get_tv_seasons_stats(df),
        'additions_over_time': get_additions_over_time(df).to_dict(orient='records'),
        'top_directors': get_top_directors(df, 10).to_dict(orient='records'),
        'longest_movies': get_longest_movies(df, 5).to_dict(orient='records'),
        'longest_tv': get_tv_shows_most_seasons(df, 5).to_dict(orient='records')
    }


if __name__ == '__main__':
    df = load_processed_data()
    summary = get_full_summary(df)
    print("Overview:", summary['overview'])
    print("Top Countries:", summary['top_countries'][:3])
    print("Top Genres:", summary['top_genres'][:3])
