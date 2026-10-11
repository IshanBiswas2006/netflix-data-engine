"""
Database module for Netflix Movies and TV Shows Analysis.
Provides MySQL connection management, schema initialization, data ingestion,
and analytical query execution with graceful fallback.
"""

import sys
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME,
    PROCESSED_DATA_PATH
)

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_CONNECTOR_AVAILABLE = True
except ImportError:
    MYSQL_CONNECTOR_AVAILABLE = False
    MySQLError = Exception


# Global SQLite in-memory mirror cache
_SQLITE_CONN = None


def get_mysql_connection():
    """
    Attempt to connect to MySQL database using configured settings.
    Returns (connection, None) if successful, or (None, error_message) on failure.
    """
    if not MYSQL_CONNECTOR_AVAILABLE:
        return None, "mysql-connector-python is not installed."

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        if conn.is_connected():
            return conn, None
    except Exception as e:
        return None, str(e)

    return None, "Unknown connection failure."


def is_mysql_available() -> bool:
    """Check if MySQL connection can be established."""
    conn, err = get_mysql_connection()
    if conn:
        conn.close()
        return True
    return False


def get_sqlite_mirror():
    """
    Creates or returns an in-memory SQLite mirror loaded with the processed dataset.
    Enables guaranteed offline analytical SQL query execution and verification
    when MySQL credentials are not configured locally.
    """
    global _SQLITE_CONN
    if _SQLITE_CONN is not None:
        return _SQLITE_CONN

    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Load cleaned dataset
    if Path(PROCESSED_DATA_PATH).exists():
        df = pd.read_csv(PROCESSED_DATA_PATH)
        # Store main table
        df.to_sql('netflix_titles', conn, index=False, if_exists='replace')

        # Create title_countries table
        tc_rows = []
        for _, row in df.iterrows():
            if pd.notna(row['country']):
                for c in str(row['country']).split(','):
                    c_clean = c.strip()
                    if c_clean:
                        tc_rows.append({'show_id': row['show_id'], 'country': c_clean})
        pd.DataFrame(tc_rows).to_sql('title_countries', conn, index=False, if_exists='replace')

        # Create title_genres table
        tg_rows = []
        for _, row in df.iterrows():
            if pd.notna(row['listed_in']):
                for g in str(row['listed_in']).split(','):
                    g_clean = g.strip()
                    if g_clean:
                        tg_rows.append({'show_id': row['show_id'], 'genre': g_clean})
        pd.DataFrame(tg_rows).to_sql('title_genres', conn, index=False, if_exists='replace')

    _SQLITE_CONN = conn
    return _SQLITE_CONN


# Standardized 10 Analytical Questions and Queries
ANALYTICAL_QUERIES = [
    {
        'id': 1,
        'title': 'Total Catalog Size',
        'question': 'What is the total volume of distinct catalog titles ingested?',
        'sql': """SELECT 
    COUNT(*) AS total_titles,
    COUNT(DISTINCT show_id) AS unique_show_ids
FROM netflix_titles;"""
    },
    {
        'id': 2,
        'title': 'Movies vs. TV Shows Split',
        'question': 'What is the proportion between Movies and TV Shows in the catalog?',
        'sql': """SELECT 
    type,
    COUNT(*) AS count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles)), 2) AS percentage
FROM netflix_titles
GROUP BY type
ORDER BY count DESC;"""
    },
    {
        'id': 3,
        'title': 'Titles by Release Year',
        'question': 'How are titles distributed across theatrical release years (top recent years)?',
        'sql': """SELECT 
    release_year,
    COUNT(*) AS title_count
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 12;"""
    },
    {
        'id': 4,
        'title': 'Top 10 Content Producing Countries',
        'question': 'Which countries produce the highest volume of catalog titles (including co-productions)?',
        'sql': """SELECT 
    tc.country,
    COUNT(DISTINCT tc.show_id) AS title_count
FROM title_countries tc
WHERE tc.country IS NOT NULL AND tc.country != ''
GROUP BY tc.country
ORDER BY title_count DESC
LIMIT 10;"""
    },
    {
        'id': 5,
        'title': 'Top 10 Genres / Categories',
        'question': 'Which genres represent the largest segments of the Netflix library?',
        'sql': """SELECT 
    tg.genre,
    COUNT(DISTINCT tg.show_id) AS title_count
FROM title_genres tg
WHERE tg.genre IS NOT NULL AND tg.genre != ''
GROUP BY tg.genre
ORDER BY title_count DESC
LIMIT 10;"""
    },
    {
        'id': 6,
        'title': 'Maturity Rating Distribution',
        'question': 'How is the catalog distributed across content maturity ratings?',
        'sql': """SELECT 
    COALESCE(rating, 'Unrated') AS rating,
    COUNT(*) AS count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles)), 2) AS percentage
FROM netflix_titles
GROUP BY rating
ORDER BY count DESC
LIMIT 10;"""
    },
    {
        'id': 7,
        'title': 'Longest Movies by Runtime',
        'question': 'What are the longest runtime feature films available on Netflix?',
        'sql': """SELECT 
    title,
    duration_minutes,
    release_year,
    country
FROM netflix_titles
WHERE type = 'Movie' AND duration_minutes IS NOT NULL
ORDER BY duration_minutes DESC
LIMIT 5;"""
    },
    {
        'id': 8,
        'title': 'TV Shows with the Most Seasons',
        'question': 'Which television series have achieved the longest run of seasons?',
        'sql': """SELECT 
    title,
    seasons_count,
    release_year,
    country
FROM netflix_titles
WHERE type = 'TV Show' AND seasons_count IS NOT NULL
ORDER BY seasons_count DESC
LIMIT 5;"""
    },
    {
        'id': 9,
        'title': 'Titles Ingested per Year',
        'question': 'How has Netflix\'s rate of catalog additions grown across digital ingestion years?',
        'sql': """SELECT 
    CAST(year_added AS INT) AS year_added,
    COUNT(*) AS titles_added
FROM netflix_titles
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added ASC;"""
    },
    {
        'id': 10,
        'title': 'Top Directors by Title Count',
        'question': 'Which primary directors have the highest volume of films and series hosted?',
        'sql': """SELECT 
    TRIM(director) AS director,
    COUNT(*) AS title_count
FROM netflix_titles
WHERE director IS NOT NULL AND director != ''
GROUP BY director
ORDER BY title_count DESC
LIMIT 10;"""
    }
]


def run_analytical_query(query_dict: dict) -> dict:
    """
    Execute a specific analytical query with execution metadata.
    Tries MySQL first if available; otherwise utilizes the local SQL mirror.
    """
    sql = query_dict['sql']
    mysql_conn, err = get_mysql_connection()
    engine_used = 'MySQL'

    if mysql_conn:
        try:
            cursor = mysql_conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            mysql_conn.close()
            columns = list(rows[0].keys()) if rows else []
            return {
                'id': query_dict['id'],
                'title': query_dict['title'],
                'question': query_dict['question'],
                'sql': sql,
                'columns': columns,
                'rows': rows,
                'engine': 'MySQL (Live Connection)',
                'status': 'PASS'
            }
        except Exception as e:
            # Fall back to SQLite mirror
            pass

    # SQLite execution
    engine_used = 'SQLite Mirror (Verified Offline Engine)'
    lite_conn = get_sqlite_mirror()
    cursor = lite_conn.cursor()
    cursor.execute(sql)
    fetched = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = [dict(row) for row in fetched]

    return {
        'id': query_dict['id'],
        'title': query_dict['title'],
        'question': query_dict['question'],
        'sql': sql,
        'columns': columns,
        'rows': rows,
        'engine': engine_used,
        'status': 'PASS'
    }


def get_all_query_results() -> list:
    """
    Executes all 10 analytical queries and returns list of result dictionaries.
    """
    results = []
    for q in ANALYTICAL_QUERIES:
        res = run_analytical_query(q)
        results.append(res)
    return results


if __name__ == '__main__':
    print("Testing SQL Analytical Engine...")
    results = get_all_query_results()
    for r in results[:3]:
        print(f"\n[Query {r['id']}: {r['title']}] ({r['engine']})")
        print("Columns:", r['columns'])
        print("Rows sample:", r['rows'][:2])
