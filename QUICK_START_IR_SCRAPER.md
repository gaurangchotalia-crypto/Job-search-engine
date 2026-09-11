# Quick Start: Investor Relations Web Scraper

## 📋 What's New?

A specialized web scraper tool specifically designed to fetch all investor relations job openings in Mumbai with advanced scrolling capabilities.

## 🚀 Quick Start (30 seconds)

### Basic Usage
```bash
python investor_relations_cli.py
```

This will:
- ✓ Scrape LinkedIn, Indeed, Naukri, and Glassdoor
- ✓ Load all available jobs through intelligent scrolling
- ✓ Filter results for investor relations roles in Mumbai
- ✓ Save filtered results to `investor_relations_mumbai_filtered.json`
- ✓ Save raw results to `investor_relations_mumbai_raw.json`

## 📂 Files Created

| File | Purpose |
|------|---------|
| `investor_relations_scraper.py` | Core scraper class with scrolling logic |
| `investor_relations_cli.py` | Command-line interface tool |
| `ir_scraper_examples.py` | 10 usage examples |
| `INVESTOR_RELATIONS_SCRAPER.md` | Full documentation |
| `QUICK_START_IR_SCRAPER.md` | This file |

## 🎯 Common Commands

### Search Different Location
```bash
python investor_relations_cli.py --location Bangalore
```

### Search Different Role
```bash
python investor_relations_cli.py --role "finance analyst"
```

### Show Browser (Debug)
```bash
python investor_relations_cli.py --no-headless
```

### More Thorough Scraping
```bash
python investor_relations_cli.py --max-scrolls 20
```

### View Statistics
```bash
python investor_relations_cli.py --statistics
```

### Verbose Logging
```bash
python investor_relations_cli.py --verbose
```

### Combine Options
```bash
python investor_relations_cli.py \
  --role "investor relations" \
  --location Mumbai \
  --max-scrolls 20 \
  --timeout 20 \
  --statistics \
  --verbose
```

## 🔧 All CLI Options

```
--role              Job role to search (default: investor relations)
--location          Location to search (default: Mumbai)
--output            Output file for filtered results
--output-raw        Output file for raw results
--no-headless       Show browser window
--max-scrolls       Maximum scroll attempts per source (default: 15)
--scroll-pause      Pause between scrolls in seconds (default: 2)
--timeout           WebDriver timeout (default: 15 seconds)
--verbose           Enable detailed logging
--statistics        Show job market statistics
```

## 💻 Python API Usage

```python
from investor_relations_scraper import InvestorRelationsWebScroller

# Create scraper
scroller = InvestorRelationsWebScroller(headless=True)

# Scrape all sources
jobs = scroller.scrape_all_sources(
    role="investor relations",
    location="Mumbai"
)

# Print results
scroller.print_results(jobs)
```

## 📊 Output Format

Results are saved as JSON with this structure:

```json
[
  {
    "title": "Senior Investor Relations Manager",
    "company": "Goldman Sachs",
    "location": "Mumbai, Maharashtra",
    "source": "LinkedIn",
    "scraped_at": "2026-09-11T12:30:45.123456",
    "job_id": "linkedin_1"
  }
]
```

## ⚡ Performance Tips

| Speed | Command |
|-------|---------|
| Fast (5-10 min) | `--max-scrolls 10 --scroll-pause 1.5` |
| Balanced (15-20 min) | `--max-scrolls 15 --scroll-pause 2` (default) |
| Thorough (25-35 min) | `--max-scrolls 20 --scroll-pause 3` |

## 🔗 Job Sources

1. **LinkedIn** - Professional network
2. **Indeed** - Major job portal
3. **Naukri** - India's largest job site
4. **Glassdoor** - Company reviews + jobs

## 🐛 Troubleshooting

### "No jobs found"
```bash
python investor_relations_cli.py --max-scrolls 20 --no-headless
```

### "Timeout errors"
```bash
python investor_relations_cli.py --timeout 25 --scroll-pause 4
```

### "Chrome not found"
```bash
pip install --upgrade webdriver-manager
```

## 📖 More Information

For detailed documentation, see: `INVESTOR_RELATIONS_SCRAPER.md`

For code examples, see: `ir_scraper_examples.py`

## ✨ Key Features

- 🔄 Advanced web scrolling to load all listings
- 🌐 Multi-source aggregation (4 major portals)
- 🔍 Smart filtering by role and location
- ♻️ Automatic duplicate removal
- 📊 Detailed statistics and logging
- 💾 JSON export
- 🎯 Anti-detection techniques
- ⚙️ Highly configurable

---

**Ready to scrape?** Run: `python investor_relations_cli.py`
