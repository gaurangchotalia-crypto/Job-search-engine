# How to Run the Investor Relations Web Scraper

## 📋 Step-by-Step Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `selenium==4.15.2` - Browser automation
- `webdriver-manager==4.0.1` - Chrome driver management
- `beautifulsoup4==4.12.2` - HTML parsing
- `requests==2.31.0` - HTTP requests
- `flask==3.0.0` - Web framework
- `python-dotenv==1.0.0` - Environment variables

**Verification:**
```bash
pip list | grep -E "selenium|webdriver-manager"
```

---

### Step 2: Check if Chrome is Installed

The scraper needs Chrome or Chromium browser.

**On Linux:**
```bash
which google-chrome
# or
which chromium-browser
# or
google-chrome --version
```

**On Mac:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

**On Windows:**
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

✅ If you see a version number, Chrome is installed and ready!

---

### Step 3: Run the Scraper

Navigate to the project directory and run:

```bash
python investor_relations_cli.py
```

**Expected Output:**
```
================================================================================
  🔍 INVESTOR RELATIONS WEB SCRAPER - MULTI-SOURCE JOB AGGREGATOR
================================================================================
  Role:     investor relations
  Location: Mumbai
================================================================================

⚙️  Initializing web scraper...
   • Headless mode: ON
   • Max scrolls: 15
   • Scroll pause: 2s
   • Timeout: 15s

✓ WebDriver initialized successfully
📍 Navigating to: https://www.linkedin.com/jobs/search/...
↓ Scroll #1 - Height: 1200 → 2400
↓ Scroll #2 - Height: 2400 → 3600
...
```

**This will take 15-20 minutes (depending on scroll settings)**

---

### Step 4: Wait for Completion

The scraper will:
1. ✓ Open Chrome browser (in headless mode - invisible)
2. ✓ Navigate to LinkedIn, Indeed, Naukri, Glassdoor
3. ✓ Scroll through job listings to load all results
4. ✓ Extract job information
5. ✓ Remove duplicates
6. ✓ Filter by role and location
7. ✓ Save results to JSON files

**Do NOT close the terminal or interrupt the process!**

---

### Step 5: Check the Results

After completion, you'll see:
```
===============================
✅ Scraping Complete!
   Total Raw Jobs: 156
   Filtered Jobs: 42
================================

💾 Filtered results saved to: investor_relations_mumbai_filtered.json
💾 Raw results saved to: investor_relations_mumbai_raw.json

✨ Total relevant jobs found: 42
```

---

## 📊 Output Files Created

### File 1: `investor_relations_mumbai_filtered.json`
**Contains:** Only investor relations jobs in Mumbai (filtered results)

```json
[
  {
    "title": "Senior Investor Relations Manager",
    "company": "Goldman Sachs",
    "location": "Mumbai, Maharashtra",
    "source": "LinkedIn",
    "scraped_at": "2026-09-11T12:30:45.123456",
    "job_id": "linkedin_1"
  },
  {
    "title": "Investor Relations Executive",
    "company": "ICICI Bank",
    "location": "Mumbai",
    "source": "Indeed",
    "scraped_at": "2026-09-11T12:35:22.234567",
    "job_id": "indeed_2"
  }
  // ... more jobs
]
```

### File 2: `investor_relations_mumbai_raw.json`
**Contains:** All jobs scraped (before filtering)
- Useful for analyzing what was scraped
- Shows data from all portals
- Includes jobs that don't match your filter

---

## 🔍 How to View Results

### Option 1: View in VS Code
```bash
code investor_relations_mumbai_filtered.json
```

### Option 2: View in Terminal
```bash
cat investor_relations_mumbai_filtered.json
```

### Option 3: Pretty Print with Python
```bash
python -c "import json; print(json.dumps(json.load(open('investor_relations_mumbai_filtered.json')), indent=2))"
```

### Option 4: Count Jobs
```bash
python -c "import json; jobs = json.load(open('investor_relations_mumbai_filtered.json')); print(f'Total jobs: {len(jobs)}'); sources = {}; [sources.update({job[\"source\"]: sources.get(job[\"source\"], 0) + 1}) for job in jobs]; print('By source:'); [print(f'  {s}: {c}') for s, c in sorted(sources.items())]"
```

### Option 5: View in Python Script
```python
import json

# Load results
with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

# Display
print(f"Total Jobs Found: {len(jobs)}\n")

for i, job in enumerate(jobs, 1):
    print(f"{i}. {job['title']}")
    print(f"   Company:  {job['company']}")
    print(f"   Location: {job['location']}")
    print(f"   Source:   {job['source']}\n")
```

---

## ⚙️ Customization Options

### Search Different Location

```bash
python investor_relations_cli.py --location Bangalore
```

**Output Files:**
- `investor_relations_bangalore_raw.json`
- `investor_relations_bangalore_filtered.json`

### Search Different Role

```bash
python investor_relations_cli.py --role "business analyst"
```

### Faster Scraping (5-10 minutes)

```bash
python investor_relations_cli.py --max-scrolls 10 --scroll-pause 1.5
```

### More Thorough Scraping (25-35 minutes)

```bash
python investor_relations_cli.py --max-scrolls 20 --scroll-pause 3
```

### Show Browser Window (Debug Mode)

```bash
python investor_relations_cli.py --no-headless
```

This shows the browser as it scrapes - useful for debugging.

### View Statistics

```bash
python investor_relations_cli.py --statistics
```

**Output includes:**
```
📊 STATISTICS

📱 Jobs by Source:
   LinkedIn        15 jobs ███ (33.3%)
   Indeed          12 jobs ██ (26.7%)
   Naukri          11 jobs ██ (24.4%)
   Glassdoor        7 jobs █ (15.6%)

🏢 Unique Companies: 28

   Top 10 Companies with Most Openings:
   • Goldman Sachs: 3 opening(s)
   • ICICI Bank: 2 opening(s)
   • HDFC Bank: 2 opening(s)
```

### Combine Multiple Options

```bash
python investor_relations_cli.py \
  --location Mumbai \
  --role "investor relations" \
  --max-scrolls 20 \
  --scroll-pause 3 \
  --statistics \
  --verbose
```

---

## 📈 Typical Results

For "Investor Relations" + "Mumbai":
- **Raw Jobs Scraped:** 100-200 (from all 4 portals)
- **Filtered Results:** 30-50 (matching your criteria)
- **Time Taken:** 15-20 minutes
- **Unique Companies:** 20-30

---

## 🐛 Troubleshooting

### Issue: "No module named selenium"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Chrome driver not found"

**Solution:**
```bash
pip install --upgrade webdriver-manager
python investor_relations_cli.py
```
(It will auto-download the Chrome driver)

### Issue: "No jobs found"

**Solution:**
```bash
# Try with more scrolls
python investor_relations_cli.py --max-scrolls 20

# Or show the browser to see what's happening
python investor_relations_cli.py --no-headless
```

### Issue: "Timeout errors"

**Solution:**
```bash
python investor_relations_cli.py --timeout 25 --scroll-pause 4
```

### Issue: "Permission denied"

**Solution:**
```bash
# Make script executable
chmod +x investor_relations_cli.py

# Then run
python investor_relations_cli.py
```

---

## 💡 Python Usage (Programmatic)

You can also use the scraper in your own Python code:

### Basic Usage

```python
from investor_relations_scraper import InvestorRelationsWebScroller

# Create scraper instance
scraper = InvestorRelationsWebScroller(headless=True)

# Run scraper
jobs = scraper.scrape_all_sources(
    role="investor relations",
    location="Mumbai"
)

# Print results
scraper.print_results(jobs)
```

### Advanced Usage

```python
from investor_relations_scraper import InvestorRelationsWebScroller
import json

scraper = InvestorRelationsWebScroller(
    headless=True,
    timeout=20,
    scroll_pause=3
)

# Scrape all sources
jobs = scraper.scrape_all_sources("investor relations", "Mumbai")

# Analyze results
print(f"Total jobs: {len(jobs)}")

# Group by company
companies = {}
for job in jobs:
    company = job['company']
    companies[company] = companies.get(company, 0) + 1

# Show top companies
for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{company}: {count} jobs")

# Save to custom file
scraper.save_to_json(jobs, "my_results.json")
```

### Scrape Specific Portal Only

```python
from investor_relations_scraper import InvestorRelationsWebScroller

scraper = InvestorRelationsWebScroller()
scraper.setup_driver()

try:
    # Only scrape LinkedIn
    linkedin_jobs = scraper.extract_linkedin_jobs("investor relations", "Mumbai")
    print(f"Found {len(linkedin_jobs)} on LinkedIn")
    
    # Only scrape Indeed
    indeed_jobs = scraper.extract_indeed_jobs("investor relations", "Mumbai")
    print(f"Found {len(indeed_jobs)} on Indeed")
    
finally:
    scraper.close()
```

---

## 📝 Data Analysis Examples

### Count jobs by source

```python
import json

with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

sources = {}
for job in jobs:
    source = job['source']
    sources[source] = sources.get(source, 0) + 1

print("Jobs by source:")
for source, count in sorted(sources.items()):
    print(f"  {source}: {count}")
```

### Find jobs from specific company

```python
import json

with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

# Find all jobs from Goldman Sachs
goldman_jobs = [j for j in jobs if 'goldman' in j['company'].lower()]
print(f"Goldman Sachs jobs: {len(goldman_jobs)}")
```

### Export to CSV

```python
import json
import csv

with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

with open('investor_relations_mumbai.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'company', 'location', 'source'])
    writer.writeheader()
    writer.writerows(jobs)

print("Exported to CSV!")
```

---

## ✅ Quick Reference

```bash
# Default run
python investor_relations_cli.py

# Different location
python investor_relations_cli.py --location Bangalore

# Different role
python investor_relations_cli.py --role "finance analyst"

# Show browser
python investor_relations_cli.py --no-headless

# More jobs (longer time)
python investor_relations_cli.py --max-scrolls 20

# View statistics
python investor_relations_cli.py --statistics

# All options combined
python investor_relations_cli.py --location Mumbai --role "investor relations" --max-scrolls 20 --statistics --verbose
```

---

## 🎯 Summary

1. **Install:** `pip install -r requirements.txt`
2. **Run:** `python investor_relations_cli.py`
3. **Wait:** 15-20 minutes for scraping to complete
4. **Results:** Check `investor_relations_mumbai_filtered.json`
5. **Analyze:** Use JSON file or Python script to view/process data

**That's it!** You now have all investor relations jobs in Mumbai from 4 major job portals! 🎉
