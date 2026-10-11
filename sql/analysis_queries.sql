-- Netflix Movies & TV Shows SQL Analysis Queries
USE netflix_analysis;

-- Query 1: Total Catalog Size
-- Analytical Question: What is the total volume of distinct catalog titles ingested?
SELECT 
    COUNT(*) AS total_titles,
    COUNT(DISTINCT show_id) AS unique_show_ids
FROM netflix_titles;


-- Query 2: Content Breakdown: Movies vs. TV Shows
-- Analytical Question: What is the exact split and proportion between Movies and TV Shows?
SELECT 
    type,
    COUNT(*) AS count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles)), 2) AS percentage
FROM netflix_titles
GROUP BY type
ORDER BY count DESC;


-- Query 3: Temporal Catalog Vintage: Titles by Release Year
-- Analytical Question: How are titles distributed across theatrical release years?
SELECT 
    release_year,
    COUNT(*) AS title_count
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year DESC;


-- Query 4: Top 10 Content Producing Nations
-- Analytical Question: Which countries produce the highest volume of catalog titles (accounting for multi-country co-productions)?
SELECT 
    tc.country,
    COUNT(DISTINCT tc.show_id) AS title_count
FROM title_countries tc
WHERE tc.country IS NOT NULL AND tc.country != ''
GROUP BY tc.country
ORDER BY title_count DESC
LIMIT 10;


-- Query 5: Top 10 Most Common Genres / Categories
-- Analytical Question: Which genres represent the largest segments of the Netflix library?
SELECT 
    tg.genre,
    COUNT(DISTINCT tg.show_id) AS title_count
FROM title_genres tg
WHERE tg.genre IS NOT NULL AND tg.genre != ''
GROUP BY tg.genre
ORDER BY title_count DESC
LIMIT 10;


-- Query 6: Content Maturity Rating Distribution
-- Analytical Question: How is the library distributed across maturity ratings (TV-MA, TV-14, etc.)?
SELECT 
    COALESCE(rating, 'Unrated') AS rating,
    COUNT(*) AS count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM netflix_titles)), 2) AS percentage
FROM netflix_titles
GROUP BY rating
ORDER BY count DESC;


-- Query 7: Longest Movies by Runtime
-- Analytical Question: What are the longest runtime feature films available on Netflix?
SELECT 
    title,
    duration_minutes,
    release_year,
    country
FROM netflix_titles
WHERE type = 'Movie' AND duration_minutes IS NOT NULL
ORDER BY duration_minutes DESC
LIMIT 10;


-- Query 8: TV Shows with the Most Seasons
-- Analytical Question: Which television series have achieved the longest syndication / season counts?
SELECT 
    title,
    seasons_count,
    release_year,
    country
FROM netflix_titles
WHERE type = 'TV Show' AND seasons_count IS NOT NULL
ORDER BY seasons_count DESC
LIMIT 10;


-- Query 9: Ingestion Velocity: Titles Added per Year
-- Analytical Question: How has Netflix's rate of catalog additions grown across digital ingestion years?
SELECT 
    year_added,
    COUNT(*) AS titles_added
FROM netflix_titles
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added ASC;


-- Query 10: Top Directors with the Most Catalog Titles
-- Analytical Question: Which directors have the highest volume of films and series hosted on Netflix?
SELECT 
    TRIM(SUBSTRING_INDEX(director, ',', 1)) AS primary_director,
    COUNT(*) AS title_count
FROM netflix_titles
WHERE director IS NOT NULL AND director != ''
GROUP BY primary_director
ORDER BY title_count DESC
LIMIT 10;
