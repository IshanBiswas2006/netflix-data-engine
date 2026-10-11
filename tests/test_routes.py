"""
Automated unit and integration tests for Flask web application (app.py).
Tests all routes, status codes, HTML structure, and error handlers using Flask test client.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Provides a test client for the Flask web application."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


def test_index_route(client):
    """Test GET / returns HTTP 200 and expected HTML content."""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "NETFLIX CATALOG" in html
    assert "Total Titles" in html
    assert "Movies vs. TV Shows" in html or "Overview" in html


def test_analysis_route(client):
    """Test GET /analysis returns HTTP 200 and analysis tables."""
    response = client.get('/analysis')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "Exploratory Data Analysis" in html
    assert "Top 10 Content-Producing Nations" in html
    assert "Top 10 Most Common Genres" in html


def test_visualizations_route(client):
    """Test GET /visualizations returns HTTP 200 and image references."""
    response = client.get('/visualizations')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "Production Visualizations" in html
    assert "01_movies_vs_tv_shows.png" in html
    assert "08_titles_added_over_time.png" in html


def test_sql_queries_route(client):
    """Test GET /sql-queries returns HTTP 200 and SQL analytical tables."""
    response = client.get('/sql-queries')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "SQL Analytics Engine" in html
    assert "SELECT" in html
    assert "total_titles" in html or "unique_show_ids" in html


def test_about_route(client):
    """Test GET /about returns HTTP 200 and methodology text."""
    response = client.get('/about')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "Methodology & Architecture" in html
    assert "Data Acquisition & Validation" in html
    assert "Flask" in html


def test_404_not_found(client):
    """Test that requesting an invalid route returns 404 cleanly without crashing."""
    response = client.get('/non-existent-route-404')
    assert response.status_code == 404
