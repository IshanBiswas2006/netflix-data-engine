"""
Netflix Movies and TV Shows Data Visualization Module
Generates 8 production-grade Matplotlib charts styled to match the dark UI template.
Saves all charts into static/images/charts/.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import PROCESSED_DATA_PATH, CHARTS_DIR
from src.data_analysis import (
    load_processed_data,
    get_top_countries,
    get_top_genres
)

# Styling palette conforming to template tokens
DARK_BG = '#0b0d0e'
CARD_BG = '#161616'
TEXT_COLOR = '#ffffff'
MUTED_TEXT = '#9a9a9a'
GRID_COLOR = '#292929'
NETFLIX_RED = '#ff462e'
ACCENT_BLUE = '#009dff'
ACCENT_GREEN = '#14c700'
ACCENT_PURPLE = '#928dab'


def apply_theme(fig, ax):
    """Apply template-harmonious dark styling to a figure and axis."""
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=MUTED_TEXT, labelsize=10)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_linewidth(1.0)
    ax.grid(True, linestyle='--', alpha=0.3, color=GRID_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    ax.title.set_fontweight('bold')
    ax.title.set_fontsize(13)


def chart_01_movies_vs_tv_shows(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """1. Donut Chart: Movies vs. TV Shows Split"""
    counts = df['type'].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    colors = [NETFLIX_RED, ACCENT_BLUE]
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor=CARD_BG, linewidth=2),
        textprops=dict(color=TEXT_COLOR, fontsize=11, fontweight='medium')
    )
    for at in autotexts:
        at.set_color(TEXT_COLOR)
        at.set_fontweight('bold')

    ax.set_title("Catalog Split: Movies vs. TV Shows", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    
    # Center text
    ax.text(0, 0, f"{len(df):,}\nTitles", ha='center', va='center', color=TEXT_COLOR, fontsize=12, fontweight='bold')

    out_path = Path(output_dir) / '01_movies_vs_tv_shows.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_02_titles_by_release_year(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """2. Line / Area Chart: Titles by Release Year (1990 - 2020)"""
    recent = df[df['release_year'] >= 1990]
    yearly = recent.groupby(['release_year', 'type']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    years = yearly.index
    movies = yearly.get('Movie', pd.Series(0, index=years))
    tv = yearly.get('TV Show', pd.Series(0, index=years))

    ax.plot(years, movies, color=NETFLIX_RED, linewidth=2.5, marker='o', markersize=4, label='Movies')
    ax.plot(years, tv, color=ACCENT_BLUE, linewidth=2.5, marker='s', markersize=4, label='TV Shows')
    ax.fill_between(years, movies, color=NETFLIX_RED, alpha=0.15)
    ax.fill_between(years, tv, color=ACCENT_BLUE, alpha=0.15)

    ax.set_title("Content Production Trend by Release Year (1990–2020)", pad=15)
    ax.set_xlabel("Theatrical / TV Release Year")
    ax.set_ylabel("Title Volume")
    ax.legend(facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR, fontsize=10)

    out_path = Path(output_dir) / '02_titles_by_release_year.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_03_top_10_countries(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """3. Horizontal Bar Chart: Top 10 Content Producing Countries"""
    top_c = get_top_countries(df, 10).sort_values(by='count', ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    bars = ax.barh(top_c['country'], top_c['count'], color=NETFLIX_RED, height=0.6, edgecolor=GRID_COLOR)

    # Value annotations on bars
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 25, bar.get_y() + bar.get_height() / 2, f"{int(w):,}",
                ha='left', va='center', color=TEXT_COLOR, fontsize=9, fontweight='medium')

    ax.set_xlim(0, top_c['count'].max() * 1.15)
    ax.set_title("Top 10 Content Producing Countries (Co-Productions Included)", pad=15)
    ax.set_xlabel("Number of Titles")

    out_path = Path(output_dir) / '03_top_10_countries.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_04_top_10_genres(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """4. Horizontal Bar Chart: Top 10 Genres / Categories"""
    top_g = get_top_genres(df, 10).sort_values(by='count', ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    bars = ax.barh(top_g['genre'], top_g['count'], color=ACCENT_BLUE, height=0.6, edgecolor=GRID_COLOR)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 20, bar.get_y() + bar.get_height() / 2, f"{int(w):,}",
                ha='left', va='center', color=TEXT_COLOR, fontsize=9, fontweight='medium')

    ax.set_xlim(0, top_g['count'].max() * 1.15)
    ax.set_title("Top 10 Most Common Catalog Genres / Categories", pad=15)
    ax.set_xlabel("Number of Categorizations")

    out_path = Path(output_dir) / '04_top_10_genres.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_05_content_rating_distribution(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """5. Vertical Bar Chart: Content Maturity Rating Distribution"""
    ratings = df['rating'].fillna('Unrated').value_counts().head(8)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    x = range(len(ratings))
    bars = ax.bar(x, ratings.values, color=ACCENT_GREEN, width=0.6, edgecolor=GRID_COLOR)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 25, f"{int(h):,}",
                ha='center', va='bottom', color=TEXT_COLOR, fontsize=9, fontweight='medium')

    ax.set_xticks(x)
    ax.set_xticklabels(ratings.index, rotation=25, ha='right')
    ax.set_ylim(0, ratings.max() * 1.15)
    ax.set_title("Distribution of Content Maturity Ratings", pad=15)
    ax.set_ylabel("Title Count")

    out_path = Path(output_dir) / '05_content_rating_distribution.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_06_movie_duration_distribution(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """6. Histogram & KDE: Movie Runtime Distribution (Minutes)"""
    runtimes = df[df['type'] == 'Movie']['duration_minutes'].dropna()

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    n, bins, patches = ax.hist(runtimes, bins=35, color=NETFLIX_RED, alpha=0.75, edgecolor=CARD_BG)
    median_val = runtimes.median()
    mean_val = runtimes.mean()

    ax.axvline(median_val, color='#ffd700', linestyle='--', linewidth=2, label=f'Median ({int(median_val)} min)')
    ax.axvline(mean_val, color='#ffffff', linestyle=':', linewidth=2, label=f'Mean ({int(mean_val)} min)')

    ax.set_title("Movie Runtime Distribution (Minutes)", pad=15)
    ax.set_xlabel("Duration (Minutes)")
    ax.set_ylabel("Number of Movies")
    ax.legend(facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR, fontsize=10)

    out_path = Path(output_dir) / '06_movie_duration_distribution.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_07_tv_show_seasons_distribution(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """7. Bar Chart: TV Show Season Count Breakdown"""
    seasons = df[df['type'] == 'TV Show']['seasons_count'].dropna().value_counts().sort_index().head(6)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    labels = [f"{int(s)} Season{'s' if s>1 else ''}" for s in seasons.index]
    bars = ax.bar(labels, seasons.values, color=ACCENT_PURPLE, width=0.55, edgecolor=GRID_COLOR)

    for bar in bars:
        h = bar.get_height()
        pct = (h / seasons.sum()) * 100
        ax.text(bar.get_x() + bar.get_width() / 2, h + 15, f"{int(h):,} ({pct:.1f}%)",
                ha='center', va='bottom', color=TEXT_COLOR, fontsize=9, fontweight='medium')

    ax.set_ylim(0, seasons.max() * 1.15)
    ax.set_title("TV Show Season Count Distribution", pad=15)
    ax.set_ylabel("Number of TV Shows")

    out_path = Path(output_dir) / '07_tv_show_seasons_distribution.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def chart_08_titles_added_over_time(df: pd.DataFrame, output_dir=CHARTS_DIR) -> Path:
    """8. Bar Chart: Ingestion Velocity by Year Added to Netflix"""
    additions = df['year_added'].dropna().astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    apply_theme(fig, ax)

    x = range(len(additions))
    bars = ax.bar(x, additions.values, color=NETFLIX_RED, width=0.6, edgecolor=GRID_COLOR)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 25, f"{int(h):,}",
                ha='center', va='bottom', color=TEXT_COLOR, fontsize=9, fontweight='medium')

    ax.set_xticks(x)
    ax.set_xticklabels(additions.index.astype(str), rotation=20, ha='right')
    ax.set_ylim(0, additions.max() * 1.15)
    ax.set_title("Ingestion Velocity: Titles Added to Netflix per Year", pad=15)
    ax.set_ylabel("Titles Added")
    ax.set_xlabel("Year Added to Netflix")

    out_path = Path(output_dir) / '08_titles_added_over_time.png'
    fig.savefig(out_path, bbox_inches='tight', facecolor=CARD_BG)
    plt.close(fig)
    return out_path


def generate_all_charts(df=None, output_dir=CHARTS_DIR) -> list:
    """
    Generate all 8 standardized analytical charts and return list of file paths.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if df is None:
        df = load_processed_data()

    print(f"Generating 8 analytical charts into: {output_dir}")
    charts = [
        chart_01_movies_vs_tv_shows(df, output_dir),
        chart_02_titles_by_release_year(df, output_dir),
        chart_03_top_10_countries(df, output_dir),
        chart_04_top_10_genres(df, output_dir),
        chart_05_content_rating_distribution(df, output_dir),
        chart_06_movie_duration_distribution(df, output_dir),
        chart_07_tv_show_seasons_distribution(df, output_dir),
        chart_08_titles_added_over_time(df, output_dir)
    ]
    for c in charts:
        print(f"  [OK] Created: {c.name}")
    return charts


if __name__ == '__main__':
    generate_all_charts()
