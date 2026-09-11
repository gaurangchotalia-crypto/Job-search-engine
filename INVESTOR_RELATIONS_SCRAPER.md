# Investor Relations Web Scraper

A specialized, multi-source web scraper with advanced scrolling capabilities designed to aggregate all investor relations job openings in Mumbai from leading job portals.

## Features

✨ **Advanced Features:**
- 🔄 **Progressive Web Scrolling**: Intelligently scrolls through job listings to load all available positions
- 🌐 **Multi-Source Aggregation**: Scrapes from LinkedIn, Indeed, Naukri, and Glassdoor simultaneously
- 🔍 **Smart Filtering**: Filters results by job title and location
- ♻️ **Duplicate Removal**: Automatically removes duplicate job listings
- 📊 **Detailed Statistics**: Provides comprehensive job market insights
- 💾 **JSON Export**: Saves results in structured JSON format
- 🎯 **Anti-Detection**: Uses stealth techniques to avoid detection

## Installation

### Prerequisites
- Python 3.7+
- Chrome/Chromium browser installed
- Dependencies from `requirements.txt`

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify Chrome installation**:
```bash
which chromium-browser  # or google-chrome
```

## Usage

### Quick Start

**Run with default settings (IR jobs in Mumbai)**:
```bash
python investor_relations_cli.py
```

### Advanced Usage

**Search for different role in Mumbai**:
```bash
python investor_relations_cli.py --role "business analyst"
```

**Search in different location**:
```bash
python investor_relations_cli.py --location Bangalore
```

**Show browser window (non-headless)**:
```bash
python investor_relations_cli.py --no-headless
```

**More aggressive scrolling**:
```bash
python investor_relations_cli.py --max-scrolls 20 --scroll-pause 3
```

**Custom output filename**:
```bash
python investor_relations_cli.py --output my_results.json
```

**Display detailed statistics**:
```bash
python investor_relations_cli.py --statistics
```

**Verbose logging**:
```bash
python investor_relations_cli.py --verbose
```

**Combined options**:
```bash
python investor_relations_cli.py \
  --role "investor relations" \
  --location Mumbai \
  --max-scrolls 20 \
  --timeout 20 \
  --scroll-pause 3 \
  --output results.json \
  --statistics \
  --verbose
```

## Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--role` | `investor relations` | Job role to search for |
| `--location` | `Mumbai` | Location to search in |
| `--output` | `investor_relations_mumbai_filtered.json` | Output file for filtered results |
| `--output-raw` | `investor_relations_mumbai_raw.json` | Output file for raw results |
| `--no-headless` | False | Display browser window during scraping |
| `--max-scrolls` | 15 | Maximum scrolls per source (higher = more jobs) |
| `--scroll-pause` | 2 | Seconds to wait between scrolls |
| `--timeout` | 15 | WebDriver timeout in seconds |
| `--verbose` | False | Enable detailed logging |
| `--statistics` | False | Display job market statistics |

## Output Files

### Filtered Results (`investor_relations_mumbai_filtered.json`)
Contains only jobs matching the search criteria (role + location):
```json
[
  {
    "title": "Senior Investor Relations Manager",
    "company": "Tech Company XYZ",
    "location": "Mumbai, Maharashtra",
    "source": "LinkedIn",
    "scraped_at": "2026-09-11T12:30:45.123456",
    "job_id": "linkedin_1"
  }
]
```

### Raw Results (`investor_relations_mumbai_raw.json`)
Contains all jobs scraped before filtering (useful for analysis).

## Sources

The scraper aggregates data from:
1. **LinkedIn Jobs** - Professional network
2. **Indeed India** - Job search engine
3. **Naukri** - India's largest job portal
4. **Glassdoor** - Company reviews and jobs

## Performance Tips

### For Better Results

1. **Increase max-scrolls** for more comprehensive results:
   ```bash
   python investor_relations_cli.py --max-scrolls 25
   ```

2. **Increase timeout** if experiencing timeouts:
   ```bash
   python investor_relations_cli.py --timeout 25
   ```

3. **Adjust scroll-pause** for slower networks:
   ```bash
   python investor_relations_cli.py --scroll-pause 4
   ```

4. **Use non-headless mode** for debugging:
   ```bash
   python investor_relations_cli.py --no-headless --verbose
   ```

### Performance Characteristics

- **Fast Mode** (default): 5-10 minutes for all sources
  - `--max-scrolls 10 --scroll-pause 1.5`
  
- **Balanced Mode** (recommended): 15-20 minutes
  - `--max-scrolls 15 --scroll-pause 2`
  
- **Comprehensive Mode**: 25-35 minutes
  - `--max-scrolls 20 --scroll-pause 3`

## Python API Usage

### Direct Library Usage

```python
from investor_relations_scraper import InvestorRelationsWebScroller

# Initialize scraper
scroller = InvestorRelationsWebScroller(
    headless=True,
    timeout=15,
    scroll_pause=2
)

# Scrape from all sources
jobs = scroller.scrape_all_sources(
    role="investor relations",
    location="Mumbai"
)

# Print results
scroller.print_results(jobs)
```

### Individual Source Scraping

```python
from investor_relations_scraper import InvestorRelationsWebScroller

scroller = InvestorRelationsWebScroller()
scroller.setup_driver()

# Scrape specific sources
linkedin_jobs = scroller.extract_linkedin_jobs("investor relations", "Mumbai")
indeed_jobs = scroller.extract_indeed_jobs("investor relations", "Mumbai")
naukri_jobs = scroller.extract_naukri_jobs("investor relations", "Mumbai")

scroller.close()
```

### Custom Filtering

```python
# Filter by specific criteria
filtered = scroller.filter_jobs(
    role="investor relations",
    location="mumbai"
)

# Remove duplicates
unique_jobs = scroller.remove_duplicates()

# Save to file
scroller.save_to_json(unique_jobs, "output.json")
```

## Output Examples

### Console Output

```
================================================================================
  🔍 INVESTOR RELATIONS WEB SCRAPER - MULTI-SOURCE JOB AGGREGATOR
================================================================================
  Role:     investor relations
  Location: Mumbai
================================================================================

✅ Found 45 Investor Relations Jobs!

---

1. Senior Investor Relations Manager
   Company:    Goldman Sachs
   Location:   Mumbai, Maharashtra
   Source:     LinkedIn
   Job ID:     linkedin_1
   Scraped:    2026-09-11T12:30:45.123456

2. Investor Relations Executive
   Company:    ICICI Bank
   Location:   Mumbai
   Source:     Indeed
   Job ID:     indeed_2
   Scraped:    2026-09-11T12:31:02.234567

📊 STATISTICS

📱 Jobs by Source:
   LinkedIn         15 jobs ███ (33.3%)
   Indeed           12 jobs ██ (26.7%)
   Naukri           11 jobs ██ (24.4%)
   Glassdoor         7 jobs █ (15.6%)

🏢 Unique Companies: 28

   Top 10 Companies with Most Openings:
   • Goldman Sachs: 3 opening(s)
   • ICICI Bank: 2 opening(s)
   • HDFC Bank: 2 opening(s)
   ...

📋 Unique Job Titles: 12

   Most Common Titles:
   • Senior Investor Relations Manager: 8 opening(s)
   • Investor Relations Executive: 6 opening(s)
   ...

---

💾 Filtered results saved to: investor_relations_mumbai_filtered.json
💾 Raw results saved to: investor_relations_mumbai_raw.json

✨ Total relevant jobs found: 45
```

## Troubleshooting

### Issue: "No jobs found"
**Solution**: 
- Increase `--max-scrolls`: `python investor_relations_cli.py --max-scrolls 20`
- Try `--no-headless` to see what's happening
- Check internet connection

### Issue: Timeout errors
**Solution**:
- Increase `--timeout`: `python investor_relations_cli.py --timeout 25`
- Increase `--scroll-pause`: `python investor_relations_cli.py --scroll-pause 4`
- Use non-headless mode to diagnose

### Issue: "WebDriver initialization failed"
**Solution**:
- Reinstall ChromeDriver: `pip install --upgrade webdriver-manager`
- Ensure Chrome is installed: `google-chrome --version`

### Issue: Duplicate results
**Solution**:
- The scraper automatically removes duplicates
- Check the raw JSON file for debugging
- Results are deduplicated based on title + company combination

## Performance Monitoring

### View raw scraping logs

```bash
python investor_relations_cli.py --verbose 2>&1 | tee scraper.log
```

### Monitor job extraction

```python
# Python script to count jobs per source
import json

with open('investor_relations_mumbai_raw.json', 'r') as f:
    jobs = json.load(f)

sources = {}
for job in jobs:
    source = job['source']
    sources[source] = sources.get(source, 0) + 1

for source, count in sorted(sources.items()):
    print(f"{source}: {count} jobs")
```

## Data Structure

Each job object contains:
- `title` (str): Job title
- `company` (str): Company name
- `location` (str): Job location
- `source` (str): Source portal (LinkedIn/Indeed/Naukri/Glassdoor)
- `scraped_at` (str): ISO format timestamp
- `job_id` (str): Unique identifier

## Limitations

- Requires active internet connection
- Subject to rate limiting on job portals
- Some portals may block automated access
- Results dependent on job portal data availability
- Filtering is keyword-based (not semantic)

## Future Enhancements

- [ ] Proxy rotation for rate limiting
- [ ] Salary information extraction
- [ ] Job description details
- [ ] Application deadline tracking
- [ ] Email notifications
- [ ] Database integration
- [ ] Web API endpoint
- [ ] Scheduled scraping

## License

See LICENSE file in repository.

## Support

For issues or feature requests, please create an issue in the repository.

---

**Last Updated**: 2026-09-11  
**Version**: 1.0.0
