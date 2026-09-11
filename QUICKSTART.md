# Quick Start Guide

Get the Job Scraper up and running in minutes!

## 🚀 Option 1: Web Interface (Easiest)

### Prerequisites
- Python 3.8+
- Chrome/Chromium installed

### Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server**
   ```bash
   python app.py
   ```

3. **Open your browser**
   ```
   http://localhost:5000
   ```

4. **Search for jobs**
   - Enter job role (default: "investor relations")
   - Enter location (default: "Mumbai")
   - Click "Start Scraping"
   - Wait for results to load
   - Download as JSON if needed

---

## 🖥️ Option 2: Command Line

### Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper**
   ```bash
   python cli.py
   ```

   Or with custom parameters:
   ```bash
   python cli.py --role "finance analyst" --location "Bangalore"
   ```

3. **View results**
   - Check the console output
   - Results also saved to `investor_relations_mumbai.json`

### Common Commands

```bash
# Default search (investor relations in Mumbai)
python cli.py

# Search for different role
python cli.py --role "finance analyst"

# Search in different location
python cli.py --location "Bangalore"

# Scrape from specific source only
python cli.py --sources indeed

# Show all options
python cli.py --help
```

---

## 🐳 Option 3: Docker

### Steps

1. **Build Docker image**
   ```bash
   docker build -t job-scraper .
   ```

2. **Run container**
   ```bash
   docker run -p 5000:5000 job-scraper
   ```

3. **Access web interface**
   ```
   http://localhost:5000
   ```

Or use docker-compose:
```bash
docker-compose up -d
docker-compose logs -f
```

---

## 📊 Understanding the Output

### Web Interface
- **Status Bar**: Shows scraping progress
- **Jobs List**: Displays found job listings
- **Download Button**: Export results as JSON

### Console Output
```
Job Title
   Company:  TechCorp India
   Location: Mumbai, Maharashtra
   Source:   Indeed
```

### JSON Output
```json
[
  {
    "title": "Investor Relations Manager",
    "company": "TechCorp India",
    "location": "Mumbai, Maharashtra",
    "source": "Indeed",
    "scraped_at": "2026-09-11T10:30:00"
  }
]
```

---

## ⚙️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and modify:
```bash
cp .env.example .env
```

### Custom Parameters (CLI)
```bash
python cli.py \
  --role "investor relations" \
  --location "Mumbai" \
  --sources "indeed,naukri,linkedin" \
  --max-scrolls 5 \
  --output "results.json"
```

---

## 🔍 Features

✅ **Multi-source Scraping**
- Indeed
- Naukri (Indian job portal)
- LinkedIn

✅ **Smart Scrolling**
- Automatically loads more jobs
- Configurable scroll count

✅ **Filtering**
- By role
- By location
- Automatic deduplication

✅ **Multiple Interfaces**
- Beautiful web UI
- Command-line tool
- Python API

✅ **Export Options**
- JSON format
- Filtered and raw data

---

## 🛠️ Troubleshooting

### Chrome/Chromium Not Found
**Solution**: Install Chrome or Chromium
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium

# Windows
# Download from https://www.chromium.org/
```

### WebDriver Issues
**Solution**: Tool auto-downloads ChromeDriver. If issues persist:
```bash
# Clear cache and reinstall
rm -rf ~/.wdm
pip install --upgrade webdriver-manager
```

### No Jobs Found
**Solution**: Check parameters
- Correct spelling of role and location
- Try different sources
- Job portals may have rate limiting (wait a few minutes)

### Slow Performance
**Solution**: Reduce scrolling
```bash
python cli.py --max-scrolls 3 --scroll-pause 1
```

---

## 📚 Learn More

- Full documentation: See `README.md`
- API usage: See `scraper.py` docstrings
- Configuration: See `config.py`

---

## 💡 Tips

1. **Caching**: Results are cached locally. Use `Clear Cache` button in web UI to refresh.

2. **Batch Searches**: Run multiple searches with different parameters:
   ```bash
   python cli.py --role "investor relations"
   python cli.py --role "finance analyst"
   python cli.py --role "business analyst"
   ```

3. **Scheduled Scraping**: Run periodically with cron (Linux/Mac):
   ```bash
   0 9 * * 1 cd /path/to/Job-search-engine && python cli.py
   ```

4. **Rate Limiting**: Add delays between requests:
   ```bash
   python cli.py --scroll-pause 3
   ```

---

## ⚖️ Legal Notice

This tool is for educational purposes. Always:
- Respect website Terms of Service
- Follow `robots.txt` guidelines
- Implement delays between requests
- Don't overload servers

---

## 🤝 Support

Having issues? Try:
1. Check `README.md` for detailed docs
2. Review error messages in console
3. Verify Chrome/Chromium installation
4. Try with different job portals

Happy job hunting! 🎉
