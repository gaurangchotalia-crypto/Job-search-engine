# Quick Reference: Running the Scraper & Getting Results

## 🚀 Run It Now (Copy & Paste)

### Best First Run (See Chrome + Statistics)
```bash
python investor_relations_cli.py --no-headless --statistics
```

### Fastest Run (Chrome hidden)
```bash
python investor_relations_cli.py
```

---

## 🖥️ What Happens When You Run It

1. **Chrome opens automatically** (or runs hidden)
2. **Scraper navigates** to LinkedIn, Indeed, Naukri, Glassdoor
3. **Scrolls through jobs** to load all listings
4. **Extracts data**: Title, Company, Location
5. **Results printed** in terminal (table format)
6. **Files saved**:
   - `investor_relations_mumbai_filtered.json` (Your main results)
   - `investor_relations_mumbai_raw.json` (All scraped data)

---

## 📊 How to View Results

### **Option 1: Terminal** (Immediate)
Results appear automatically after scraping!

### **Option 2: JSON File**
```bash
# View raw JSON
cat investor_relations_mumbai_filtered.json

# Pretty print (readable)
python -m json.tool investor_relations_mumbai_filtered.json
```

### **Option 3: Excel Spreadsheet**
```bash
# Convert to CSV
python3 << 'EOF'
import json, csv
with open('investor_relations_mumbai_filtered.json') as f:
    jobs = json.load(f)
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    csv.DictWriter(f, fieldnames=jobs[0].keys()).writerows(jobs)
EOF

# Open in Excel
xdg-open results.csv
```

---

## ⚡ Performance Times

| Mode | Time | Command |
|------|------|---------|
| **Fast** | 5-10 min | `--max-scrolls 10 --scroll-pause 1.5` |
| **Balanced** (Default) | 15-20 min | `--max-scrolls 15` |
| **Thorough** | 25-35 min | `--max-scrolls 20` |

---

## 🎯 Common Commands

| Task | Command |
|------|---------|
| Run with Chrome visible | `python investor_relations_cli.py --no-headless` |
| Search Bangalore instead | `python investor_relations_cli.py --location Bangalore` |
| Search different role | `python investor_relations_cli.py --role "finance analyst"` |
| See statistics | `python investor_relations_cli.py --statistics` |
| More thorough search | `python investor_relations_cli.py --max-scrolls 20` |
| Detailed logging | `python investor_relations_cli.py --verbose` |
| Custom output file | `python investor_relations_cli.py --output my_jobs.json` |

---

## 📁 Result File Structure

Each job in JSON contains:
```json
{
  "title": "Senior Investor Relations Manager",
  "company": "Goldman Sachs",
  "location": "Mumbai, Maharashtra",
  "source": "LinkedIn",
  "scraped_at": "2026-09-11T14:32:45.123456",
  "job_id": "linkedin_1"
}
```

---

## ✅ Complete Workflow (Step by Step)

```bash
# Step 1: Navigate to project
cd /home/user/Job-search-engine

# Step 2: Run scraper with Chrome visible + statistics
python investor_relations_cli.py --no-headless --statistics

# Step 3: Wait for results (15-20 minutes)
# Watch Chrome scrape, see progress in terminal

# Step 4: Results appear in terminal automatically
# Shows all jobs in formatted table

# Step 5 (Optional): View as JSON
cat investor_relations_mumbai_filtered.json

# Step 6 (Optional): Convert to Excel
python -m json.tool investor_relations_mumbai_filtered.json > jobs.json
xdg-open jobs.json
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Chrome doesn't open | `sudo apt-get install google-chrome-stable` |
| "No jobs found" | Try `--max-scrolls 20` for more scrolling |
| Too slow? | Remove `--no-headless` to run faster |
| Timeout errors | Add `--timeout 25 --scroll-pause 4` |
| Can't run file | `python3 investor_relations_cli.py` instead |

---

## 💡 Pro Tips

1. **First time?** Use `--no-headless` to see what's happening
2. **Want fast results?** Run without `--no-headless` 
3. **Need more jobs?** Increase `--max-scrolls` (10 → 20)
4. **Verify data?** Check JSON file manually
5. **Share results?** Convert to CSV for others

---

## 📞 Key Files & Docs

- **This Quick Reference**: `QUICK_REFERENCE.md`
- **Detailed Guide**: `HOW_TO_RUN_ON_CHROME.md`
- **Full Documentation**: `INVESTOR_RELATIONS_SCRAPER.md`
- **Code Examples**: `ir_scraper_examples.py`

---

## 🎯 Next Steps

1. Copy the command:
   ```bash
   python investor_relations_cli.py --no-headless --statistics
   ```

2. Paste in terminal and press Enter

3. Watch Chrome open and scrape

4. See results in terminal

5. Check JSON files for structured data

**That's it! You're ready to go!** 🚀
