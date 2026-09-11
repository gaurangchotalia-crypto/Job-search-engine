# Job Search Engine - Investor Relations Scraper

A comprehensive web scraping tool to find investor relations job openings in Mumbai from multiple job portals.

## Features

- **Multi-source Scraping**: Scrapes jobs from Indeed, Naukri, iimjobs, and LinkedIn
- **Smart Scrolling**: Automatically scrolls through job listings to load more content
- **Filtering**: Filters jobs by role and location
- **Web Interface**: Beautiful Flask-based web UI for easy interaction
- **CLI Tool**: Command-line interface for automated scraping
- **JSON Export**: Export results to JSON format
- **Real-time Status**: Track scraping progress in real-time

## Prerequisites

- Python 3.8+
- Chrome/Chromium browser
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gaurangchotalia-crypto/Job-search-engine.git
cd Job-search-engine
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

Start the Flask server:
```bash
python app.py
```

Then open your browser and navigate to: `http://localhost:5000`

Features:
- Enter the job role and location
- Click "Start Scraping" to begin
- View results in real-time
- Download results as JSON
- Clear cache to start fresh

### Command Line Interface

Run the scraper directly:
```bash
python cli.py --role "investor relations" --location "Mumbai"
```

Options:
- `--role`: Job role to search for (default: "investor relations")
- `--location`: Location to search in (default: "Mumbai")
- `--output`: Output file name (default: "investor_relations_jobs.json")
- `--sources`: Comma-separated sources to scrape (default: "indeed,naukri,linkedin")

Examples:
```bash
# Search for investor relations in Mumbai
python cli.py

# Search for a different role
python cli.py --role "finance analyst" --location "Bangalore"

# Scrape only from Indeed
python cli.py --sources indeed

# Custom output file
python cli.py --output my_jobs.json
```

### Python API

Use the scraper in your Python code:
```python
from scraper import JobScraper

scraper = JobScraper(headless=True)
jobs = scraper.scrape_all_sources(role="investor relations", location="Mumbai")

# Filter jobs
filtered = scraper.filter_jobs(role="investor relations", location="mumbai")

# Save to file
scraper.save_filtered_jobs_to_json(filtered, "output.json")

scraper.close()
```

## Project Structure

```
Job-search-engine/
├── scraper.py              # Main scraper class
├── app.py                  # Flask web application
├── cli.py                  # Command-line interface
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web UI template
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## How It Works

1. **Initialization**: Sets up a headless Chrome browser with anti-detection measures
2. **Scraping**: Navigates to job portals and scrolls to load more content
3. **Extraction**: Parses HTML to extract job details (title, company, location)
4. **Filtering**: Filters results based on role and location keywords
5. **Storage**: Saves results to JSON files

## Supported Job Portals

- **Indeed** (indeed.com)
- **Naukri** (naukri.com)
- **LinkedIn** (linkedin.com)

## Output Format

Jobs are saved in JSON format with the following structure:
```json
[
  {
    "title": "Investor Relations Manager",
    "company": "TechCorp India",
    "location": "Mumbai, Maharashtra",
    "source": "Indeed",
    "scraped_at": "2026-09-11T10:30:00.000000"
  }
]
```

## Performance Notes

- First run takes longer as it downloads ChromeDriver
- Each job portal takes ~30-60 seconds to scrape
- Total scraping time: 2-3 minutes for all sources
- Results are cached to avoid re-scraping

## Troubleshooting

### WebDriver Issues
- Ensure Chrome/Chromium is installed
- The tool automatically downloads ChromeDriver

### No Jobs Found
- Check that the role and location are correct
- Job portals may have rate limiting
- Try again after a few minutes

### Slow Performance
- Reduce `max_scrolls` parameter for faster scraping
- Use single source instead of all sources

## Legal Notice

This tool is for educational purposes. Respect the Terms of Service of job portals:
- Check their `robots.txt` and `terms_of_service`
- Implement delays between requests
- Don't overload servers with too many requests

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub or contact the project maintainers.
