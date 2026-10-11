"""
Netflix Movies and TV Shows Analysis — Flask Application
Provides clean web routing, server-side template rendering,
cached analytical findings, and graceful error handling.
"""

import sys
from pathlib import Path
# pyrefly: ignore [missing-import]
from flask import Flask, render_template

# Set project root in path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    PROCESSED_DATA_PATH, RAW_DATA_PATH,
    SECRET_KEY, DEBUG, PORT
)
from src.data_analysis import load_processed_data, get_full_summary
from src.database import get_all_query_results

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / 'templates'),
    static_folder=str(PROJECT_ROOT / 'static')
)
app.config['SECRET_KEY'] = SECRET_KEY

# Cached precomputed analytical findings
_CACHED_SUMMARY = None
_CACHED_SAMPLE = None


def get_cached_data():
    """Load or retrieve precomputed analytics cache."""
    global _CACHED_SUMMARY, _CACHED_SAMPLE
    if _CACHED_SUMMARY is None:
        try:
            if Path(PROCESSED_DATA_PATH).exists():
                df = load_processed_data(PROCESSED_DATA_PATH)
            elif Path(RAW_DATA_PATH).exists():
                from src.data_cleaning import clean_dataset
                from src.data_cleaning import load_raw_data
                df = clean_dataset(load_raw_data(RAW_DATA_PATH))
            else:
                df = None

            if df is not None and not df.empty:
                _CACHED_SUMMARY = get_full_summary(df)
                # Sample 10 representative titles
                _CACHED_SAMPLE = df[['show_id', 'type', 'title', 'country', 'release_year', 'rating', 'duration', 'listed_in']].head(10).to_dict(orient='records')
            else:
                _CACHED_SUMMARY = {
                    'overview': {'total_titles': 0, 'movies_count': 0, 'tv_shows_count': 0, 'movie_percentage': 0, 'tv_show_percentage': 0, 'earliest_release_year': 0, 'latest_release_year': 0, 'avg_movie_duration_min': 0, 'avg_tv_seasons': 0},
                    'content_type': [], 'top_countries': [], 'top_genres': [],
                    'ratings': [], 'movie_stats': {'median': 0, 'mean': 0, 'min': 0, 'max': 0},
                    'tv_stats': {'single_season_pct': 0}, 'longest_movies': [], 'longest_tv': []
                }
                _CACHED_SAMPLE = []
        except Exception as e:
            app.logger.error(f"Error initializing data cache: {e}")
            _CACHED_SUMMARY = {
                'overview': {'total_titles': 0, 'movies_count': 0, 'tv_shows_count': 0, 'movie_percentage': 0, 'tv_show_percentage': 0, 'earliest_release_year': 0, 'latest_release_year': 0, 'avg_movie_duration_min': 0, 'avg_tv_seasons': 0},
                'content_type': [], 'top_countries': [], 'top_genres': [],
                'ratings': [], 'movie_stats': {'median': 0, 'mean': 0, 'min': 0, 'max': 0},
                'tv_stats': {'single_season_pct': 0}, 'longest_movies': [], 'longest_tv': []
            }
            _CACHED_SAMPLE = []

    return _CACHED_SUMMARY, _CACHED_SAMPLE


@app.route('/')
def index():
    """Route: Home / Project Overview"""
    summary, sample = get_cached_data()
    return render_template(
        'index.html',
        active_page='index',
        overview=summary.get('overview', {}),
        recent_sample=sample
    )


@app.route('/analysis')
def analysis():
    """Route: Exploratory Data Analysis findings"""
    summary, _ = get_cached_data()
    return render_template(
        'analysis.html',
        active_page='analysis',
        summary=summary
    )


@app.route('/visualizations')
def visualizations():
    """Route: Production Data Visualizations gallery"""
    return render_template(
        'visualizations.html',
        active_page='visualizations'
    )


@app.route('/sql-queries')
def sql_queries():
    """Route: SQL Analytical Questions and Verified Tabular Results"""
    queries = get_all_query_results()
    return render_template(
        'sql_queries.html',
        active_page='sql_queries',
        queries=queries
    )


@app.route('/about')
def about():
    """Route: About, Methodology, Tech Stack, and Limitations"""
    return render_template(
        'about.html',
        active_page='about'
    )


@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', active_page=''), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', active_page=''), 500


if __name__ == '__main__':
    print(f"Starting Netflix Analytics Flask server on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
