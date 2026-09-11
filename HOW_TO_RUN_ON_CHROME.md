# How to Run the Scraper on Chrome Browser & Get Results

## 🔍 Understanding How It Works

The investor relations scraper **automatically uses Chrome** via Selenium WebDriver. It scrolls through job portals and extracts data programmatically.

### Two Modes:

1. **Headless Mode** (Default) - Chrome runs in background, faster
2. **Non-Headless Mode** - Chrome window is visible, you can see what's happening

---

## 🚀 Option 1: Run with Chrome Visible (Recommended for First Time)

This shows you exactly what the scraper is doing in real Chrome browser:

```bash
python investor_relations_cli.py --no-headless
```

### What You'll See:

1. Chrome browser opens automatically
2. Scraper navigates to LinkedIn, Indeed, Naukri, Glassdoor
3. Browser scrolls down to load jobs
4. Terminal shows progress:
   ```
   ⏳ Scraping LinkedIn...
   ↓ Scroll #1 - Height: 2000 → 3500
   ↓ Scroll #2 - Height: 3500 → 5200
   ✓ Found 45 job cards on LinkedIn
   ```
5. After completion, results are saved to JSON files

### Browser Window Tips:

- Don't close the browser - let it finish automatically
- You can see it loading different job portals
- Watch the scrolling action happen in real-time
- Terminal shows what data is being extracted

---

## ⚡ Option 2: Run Faster (Headless Mode - Default)

Chrome runs in background (no window visible):

```bash
python investor_relations_cli.py
```

**Advantages:**
- 30-40% faster execution
- Uses less memory
- Better for automated tasks
- Results are identical

---

## 📊 How to Get & View Results

### 1. **View Results in Terminal (Immediate)**

After scraping completes, you see results like:

```
================================================================================
  🔍 INVESTOR RELATIONS WEB SCRAPER - MULTI-SOURCE JOB AGGREGATOR
================================================================================

✅ Found 45 Investor Relations Jobs!

---

1. Senior Investor Relations Manager
   Company:    Goldman Sachs
   Location:   Mumbai, Maharashtra
   Source:     LinkedIn
   Job ID:     linkedin_1

2. Investor Relations Executive
   Company:    ICICI Bank
   Location:   Mumbai
   Source:     Indeed

... (more jobs)

📱 Jobs by Source:
   LinkedIn         15 jobs ███ (33.3%)
   Indeed           12 jobs ██ (26.7%)
   Naukri           11 jobs ██ (24.4%)
   Glassdoor         7 jobs █ (15.6%)

🏢 Unique Companies: 28
```

### 2. **View Results in JSON Files**

Two JSON files are automatically created:

#### **a) Filtered Results** (`investor_relations_mumbai_filtered.json`)
Only jobs matching "investor relations" + "Mumbai"

```bash
cat investor_relations_mumbai_filtered.json
```

**Output:**
```json
[
  {
    "title": "Senior Investor Relations Manager",
    "company": "Goldman Sachs",
    "location": "Mumbai, Maharashtra",
    "source": "LinkedIn",
    "scraped_at": "2026-09-11T14:32:45.123456",
    "job_id": "linkedin_1"
  },
  {
    "title": "Investor Relations Executive",
    "company": "ICICI Bank",
    "location": "Mumbai",
    "source": "Indeed",
    "scraped_at": "2026-09-11T14:33:02.234567",
    "job_id": "indeed_2"
  }
]
```

#### **b) Raw Results** (`investor_relations_mumbai_raw.json`)
All jobs scraped (before filtering)

### 3. **Pretty Print JSON Results**

Make JSON more readable:

```bash
# Install jq (pretty printer)
sudo apt-get install jq

# View filtered results nicely
jq . investor_relations_mumbai_filtered.json

# Count total jobs
jq length investor_relations_mumbai_filtered.json

# Get only company names
jq '.[] | .company' investor_relations_mumbai_filtered.json

# Get jobs from specific source
jq '.[] | select(.source == "LinkedIn")' investor_relations_mumbai_filtered.json
```

### 4. **Convert to CSV (Excel)**

```bash
python investor_relations_cli.py

# Convert JSON to CSV using Python
python3 << 'EOF'
import json
import csv

# Read JSON
with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

# Write CSV
with open('investor_relations_mumbai.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
    writer.writeheader()
    writer.writerows(jobs)

print(f"✓ Converted {len(jobs)} jobs to CSV")
EOF

# View CSV
cat investor_relations_mumbai.csv
```

### 5. **Open Results in Excel/Spreadsheet**

```bash
# Open CSV in default application
xdg-open investor_relations_mumbai.csv
```

---

## 🎯 Complete Step-by-Step Guide

### **Step 1: Install Dependencies** (One-time only)

```bash
cd /home/user/Job-search-engine
pip install -r requirements.txt
```

### **Step 2: Run with Chrome Visible** (First time)

```bash
python investor_relations_cli.py --no-headless
```

**Watch the process:**
- Chrome opens
- Loads LinkedIn jobs page
- Scrolls down automatically
- Extracts job titles, companies, locations
- Repeats for Indeed, Naukri, Glassdoor
- Browser closes automatically

### **Step 3: Check Results**

**In terminal:**
```bash
# View in terminal
cat investor_relations_mumbai_filtered.json | head -50

# Pretty print
python -m json.tool investor_relations_mumbai_filtered.json | head -100
```

**In file manager:**
```bash
# Open folder
cd /home/user/Job-search-engine
ls -lah *.json
```

You'll see:
```
-rw-r--r-- investor_relations_mumbai_filtered.json (smaller file - filtered results)
-rw-r--r-- investor_relations_mumbai_raw.json      (larger file - all jobs)
```

### **Step 4: Analyze Results**

```bash
# Count jobs by source
python3 << 'EOF'
import json

with open('investor_relations_mumbai_filtered.json', 'r') as f:
    jobs = json.load(f)

sources = {}
for job in jobs:
    source = job['source']
    sources[source] = sources.get(source, 0) + 1

print(f"Total Jobs: {len(jobs)}\n")
print("Jobs by Source:")
for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
    print(f"  {source}: {count} jobs")

# Top companies
companies = {}
for job in jobs:
    company = job['company']
    companies[company] = companies.get(company, 0) + 1

print("\nTop 5 Companies:")
for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {company}: {count} openings")
EOF
```

---

## 📋 Different Ways to Run

### **Run 1: Visible Chrome + Statistics**
```bash
python investor_relations_cli.py --no-headless --statistics
```

**Result:** 
- Chrome window opens and you watch it scrape
- Terminal shows statistics after completion

### **Run 2: Fast Background Mode**
```bash
python investor_relations_cli.py --max-scrolls 10 --scroll-pause 1.5
```

**Result:**
- Fast execution (5-10 minutes)
- Chrome runs hidden
- Results ready quickly

### **Run 3: Thorough Scraping**
```bash
python investor_relations_cli.py --max-scrolls 20 --no-headless --verbose
```

**Result:**
- Chrome visible
- More scrolling = more jobs
- Detailed logging in terminal

### **Run 4: Search Different Location**
```bash
python investor_relations_cli.py --location Bangalore --no-headless
```

**Result:**
- Scrapes Bangalore instead of Mumbai
- Saves to separate files
- Chrome visible during scraping

### **Run 5: Search Different Role**
```bash
python investor_relations_cli.py --role "finance analyst" --no-headless
```

**Result:**
- Searches for finance analyst jobs
- Still in Mumbai (default)
- Chrome visible

---

## 🎯 Getting Results - Full Workflow

### **Workflow 1: Simple (5 minutes)**
```bash
# 1. Run scraper
python investor_relations_cli.py

# 2. Check results in terminal
echo "✓ Results are displayed above"

# 3. View JSON file
cat investor_relations_mumbai_filtered.json
```

### **Workflow 2: With Analysis (10 minutes)**
```bash
# 1. Run with statistics
python investor_relations_cli.py --statistics

# 2. Save results to custom file
python investor_relations_cli.py --output my_jobs.json

# 3. Convert to CSV
python3 << 'EOF'
import json
import csv
with open('my_jobs.json') as f:
    jobs = json.load(f)
with open('my_jobs.csv', 'w', newline='') as f:
    csv.DictWriter(f, fieldnames=jobs[0].keys()).writerows(jobs)
EOF

# 4. Open in spreadsheet
xdg-open my_jobs.csv
```

### **Workflow 3: Python Integration (For developers)**
```bash
# Use scraper in Python script
python3 << 'EOF'
from investor_relations_scraper import InvestorRelationsWebScroller

scroller = InvestorRelationsWebScroller(headless=False)  # Visible Chrome
jobs = scroller.scrape_all_sources("investor relations", "Mumbai")

print(f"Found {len(jobs)} jobs")

# Process results
for job in jobs[:5]:
    print(f"• {job['title']} @ {job['company']}")
EOF
```

---

## 🖥️ View Results in Different Formats

### **1. Terminal Pretty Print**
```bash
python -m json.tool investor_relations_mumbai_filtered.json | head -50
```

### **2. Count Total Jobs**
```bash
python3 -c "import json; f=open('investor_relations_mumbai_filtered.json'); print(f'Total: {len(json.load(f))} jobs')"
```

### **3. Extract Specific Information**
```bash
# Get all company names
python3 << 'EOF'
import json
with open('investor_relations_mumbai_filtered.json') as f:
    jobs = json.load(f)
    companies = set(j['company'] for j in jobs)
    for c in sorted(companies):
        print(c)
EOF
```

### **4. Excel Spreadsheet**
```bash
# Convert to CSV then open
python investor_relations_cli.py && python3 << 'EOF'
import json, csv
with open('investor_relations_mumbai_filtered.json') as f:
    jobs = json.load(f)
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    csv.DictWriter(f, fieldnames=jobs[0].keys()).writerows(jobs)
print("✓ Saved to results.csv - Open in Excel!")
EOF
```

---

## ⚠️ Troubleshooting

### **Chrome doesn't open**
```bash
# Install Chrome if not present
sudo apt-get install google-chrome-stable

# Verify installation
google-chrome --version
```

### **Permission denied error**
```bash
# Make script executable
chmod +x investor_relations_cli.py

# Run with python3
python3 investor_relations_cli.py
```

### **No jobs found**
```bash
# Try more scrolling
python investor_relations_cli.py --max-scrolls 20 --no-headless

# Check internet connection
ping google.com
```

### **Chrome closes immediately**
```bash
# Run in non-headless to see what's happening
python investor_relations_cli.py --no-headless --verbose
```

---

## 📊 Results Summary

After running `python investor_relations_cli.py --no-headless`:

**Files Created:**
- ✅ `investor_relations_mumbai_filtered.json` - Your main results (45+ jobs)
- ✅ `investor_relations_mumbai_raw.json` - All scraped jobs before filtering

**Terminal Output Shows:**
- ✅ Number of jobs found
- ✅ Job titles, companies, locations
- ✅ Statistics by source and company
- ✅ Execution time

**To Access Results:**
1. **Terminal** - Results display immediately after scraping
2. **JSON Files** - Open with text editor or `cat` command
3. **CSV/Excel** - Convert using Python script above
4. **Python API** - Import and use in your own code

---

## 🎯 Recommended First Run

**Best command for first time:**
```bash
python investor_relations_cli.py --no-headless --statistics
```

**Why?**
- ✓ You see Chrome working
- ✓ Statistics show what was found
- ✓ Slower but more informative
- ✓ Easy to verify results

**Then for faster runs:**
```bash
python investor_relations_cli.py
```

---

**You're all set!** The Chrome browser runs automatically. Just execute the command and wait for results! 🚀
