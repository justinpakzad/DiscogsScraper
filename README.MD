# Discogs Scraper

Discogs Scraper is a web scraper built using Python and Scrapy, designed to extract detailed release data from [Discogs.com](https://www.discogs.com/). It provides flexibility in specifying search parameters like years, genres, formats, and styles, and supports exporting the scraped data in CSV or JSON formats.

## Features
- Scrape detailed release data from Discogs based on user-defined criteria.
- Specify search parameters like start and end years, release formats, genres, and optional styles.
- Control the number of pages to scrape.
- Export data to either CSV or JSON format.
- Extracted data fields include:
  - Artist
  - Title
  - Label
  - Country
  - Format
  - Release Date
  - Genre
  - Styles
  - Number of Users Who Have/Want This Release
  - Number of Ratings
  - Average Rating
  - Lowest, Median, and Highest Sold Price

## Installation
1. Clone the repository:
```
git clone https://github.com/justinpakzad/discogs-scraper.git
```
2. Install required dependencies:
```cd discogs_scraper
pip install -r requirements.txt
```
## Command Line Options
- `--start_year`: Start year for filtering (default: 1990)
- `--end_year`: End year for filtering (default: 2000)
- `--genre`: Release genre (default: Electronic)
- `--format`: Release format (default: Vinyl)
- `--style`: Release style (optional)
- `--pages`: Limit the number of pages to scrape (default: 20)
- `-o`, `--output`: Specify the output file name (default output format is CSV)

## Example usage:
```
scrapy crawl discogs_scraper -a start_year=199 -a end_year=2005 -a genre=Electronic -a format=Vinyl -a style=Electro -a pages=15 -o electro.csv
```
