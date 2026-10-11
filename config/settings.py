"""
Configuration settings for Netflix Movies and TV Shows Analysis project.
Reads environment variables with fallback defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
ENV_PATH = BASE_DIR / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

# Data paths
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_PATH = DATA_DIR / 'raw' / 'netflix_titles.csv'
PROCESSED_DATA_PATH = DATA_DIR / 'processed' / 'netflix_cleaned.csv'

# Static & Reports
STATIC_DIR = BASE_DIR / 'static'
CHARTS_DIR = STATIC_DIR / 'images' / 'charts'
REPORTS_DIR = BASE_DIR / 'reports'

# Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'netflix_analysis')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'netflix-analytics-secret-key-2026')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.getenv('PORT', 5000))
