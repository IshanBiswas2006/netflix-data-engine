-- Schema definition for netflix_analysis database

USE netflix_analysis;

-- 1. Main Titles Table
DROP TABLE IF EXISTS title_genres;
DROP TABLE IF EXISTS title_countries;
DROP TABLE IF EXISTS netflix_titles;

CREATE TABLE netflix_titles (
    show_id BIGINT PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    director TEXT,
    cast TEXT,
    country VARCHAR(255),
    date_added VARCHAR(50),
    date_added_clean DATE,
    release_year INT,
    rating VARCHAR(20),
    duration VARCHAR(50),
    duration_minutes INT,
    seasons_count INT,
    year_added INT,
    month_added INT,
    listed_in TEXT,
    description TEXT,
    INDEX idx_type (type),
    INDEX idx_release_year (release_year),
    INDEX idx_rating (rating),
    INDEX idx_year_added (year_added)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Normalized Title Countries Table (1:N relationship for accurate co-production analysis)
CREATE TABLE title_countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    show_id BIGINT NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (show_id) REFERENCES netflix_titles(show_id) ON DELETE CASCADE,
    INDEX idx_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Normalized Title Genres Table (1:N relationship for accurate genre category queries)
CREATE TABLE title_genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    show_id BIGINT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    FOREIGN KEY (show_id) REFERENCES netflix_titles(show_id) ON DELETE CASCADE,
    INDEX idx_genre (genre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
