"""
Examples of how to use the Job Scraper as a Python module
"""

from scraper import JobScraper
import json

# Example 1: Basic Usage
print("=" * 60)
print("Example 1: Basic Scraping")
print("=" * 60)

scraper = JobScraper(headless=True)
jobs = scraper.scrape_all_sources(
    role="investor relations",
    location="Mumbai"
)
scraper.close()

print(f"Found {len(jobs)} jobs")
for job in jobs[:5]:  # Print first 5
    print(f"- {job['title']} at {job['company']}")

# Example 2: Scrape from Specific Sources
print("\n" + "=" * 60)
print("Example 2: Scrape from Specific Sources")
print("=" * 60)

scraper = JobScraper(headless=True)
scraper.setup_driver()

# Only scrape Indeed
print("Scraping Indeed...")
scraper.extract_jobs_from_indeed("investor relations", "Mumbai")
print(f"Found {len(scraper.jobs)} jobs from Indeed")

# Save to file
scraper.save_jobs_to_json("indeed_jobs.json")
scraper.close()

# Example 3: Advanced Filtering
print("\n" + "=" * 60)
print("Example 3: Advanced Filtering")
print("=" * 60)

scraper = JobScraper(headless=True)
jobs = scraper.scrape_all_sources(role="investor relations", location="Mumbai")

# Custom filtering
filtered = []
for job in jobs:
    # Only include jobs from specific companies
    if any(company in job['company'].lower() for company in ['tech', 'finance', 'bank']):
        filtered.append(job)

print(f"Filtered to {len(filtered)} jobs from tech/finance/bank companies")

# Save filtered results
scraper.save_filtered_jobs_to_json(filtered, "filtered_tech_jobs.json")
scraper.close()

# Example 4: Processing Results
print("\n" + "=" * 60)
print("Example 4: Processing and Analyzing Results")
print("=" * 60)

# Load saved results
with open("investor_relations_mumbai.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# Group by company
companies = {}
for job in jobs:
    company = job['company']
    if company not in companies:
        companies[company] = []
    companies[company].append(job)

print(f"Jobs from {len(companies)} unique companies:")
for company, company_jobs in sorted(companies.items()):
    print(f"  {company}: {len(company_jobs)} opening(s)")

# Group by source
sources = {}
for job in jobs:
    source = job['source']
    if source not in sources:
        sources[source] = 0
    sources[source] += 1

print(f"\nJobs by source:")
for source, count in sources.items():
    print(f"  {source}: {count} jobs")

# Example 5: Batch Processing
print("\n" + "=" * 60)
print("Example 5: Batch Processing Multiple Searches")
print("=" * 60)

roles = ["investor relations", "finance analyst", "business analyst"]
locations = ["Mumbai", "Bangalore"]

all_jobs = []

for role in roles:
    for location in locations:
        print(f"Scraping {role} in {location}...")
        scraper = JobScraper(headless=True)
        jobs = scraper.scrape_all_sources(role=role, location=location)
        all_jobs.extend(jobs)
        scraper.close()
        print(f"  Found {len(jobs)} jobs")

# Save all results
with open("all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)

print(f"\nTotal: {len(all_jobs)} jobs saved")

# Example 6: Custom Web Scraping
print("\n" + "=" * 60)
print("Example 6: Custom Scrolling Configuration")
print("=" * 60)

scraper = JobScraper(headless=True)
scraper.setup_driver()

# Scrape with custom scroll settings
url = "https://in.indeed.com/jobs?q=investor%20relations&l=Mumbai"
scraper.scroll_to_load_jobs(url, max_scrolls=10, scroll_pause=3)

# Extract jobs (using custom CSS selectors if needed)
job_cards = scraper.driver.find_elements("css selector", "div.job_seen_beacon")
print(f"Found {len(job_cards)} job cards")

scraper.close()

# Example 7: Error Handling
print("\n" + "=" * 60)
print("Example 7: Error Handling")
print("=" * 60)

try:
    scraper = JobScraper(headless=True)
    jobs = scraper.scrape_all_sources(role="xyz", location="xyz")

    if len(jobs) == 0:
        print("No jobs found with the specified criteria")
    else:
        print(f"Found {len(jobs)} jobs")

except Exception as e:
    print(f"Error during scraping: {e}")

finally:
    scraper.close()

# Example 8: Integration with Data Analysis
print("\n" + "=" * 60)
print("Example 8: Data Analysis")
print("=" * 60)

# Load jobs
with open("investor_relations_mumbai.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

if jobs:
    # Find most common companies
    from collections import Counter
    companies = Counter(job['company'] for job in jobs)

    print("Top 5 companies with most openings:")
    for company, count in companies.most_common(5):
        print(f"  {company}: {count} opening(s)")

    # Most common sources
    sources = Counter(job['source'] for job in jobs)
    print("\nJobs by source:")
    for source, count in sources.items():
        print(f"  {source}: {count}")
else:
    print("No jobs found to analyze")

print("\n" + "=" * 60)
print("End of Examples")
print("=" * 60)
