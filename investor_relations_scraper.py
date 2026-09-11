import os
import json
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvestorRelationsWebScroller:
    """Specialized web scrolling tool for Investor Relations jobs in Mumbai"""

    def __init__(self, headless=True, timeout=15, scroll_pause=2):
        self.headless = headless
        self.timeout = timeout
        self.scroll_pause = scroll_pause
        self.driver = None
        self.jobs = []
        self.wait = None

    def setup_driver(self):
        """Initialize Chrome WebDriver with anti-detection options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features')

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info("✓ WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"✗ Failed to initialize WebDriver: {str(e)}")
            raise

    def scroll_until_complete(self, url: str, max_scrolls: int = 15) -> bool:
        """Advanced scrolling mechanism to load all job listings"""
        try:
            logger.info(f"📍 Navigating to: {url}")
            self.driver.get(url)
            time.sleep(3)

            scroll_count = 0
            consecutive_no_change = 0
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while scroll_count < max_scrolls and consecutive_no_change < 2:
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.scroll_pause)

                # Wait for new content to load
                time.sleep(1)

                # Get new height
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    consecutive_no_change += 1
                    logger.info(f"⚠️  No new content loaded (attempt {consecutive_no_change}/2)")
                else:
                    consecutive_no_change = 0
                    scroll_count += 1
                    logger.info(f"↓ Scroll #{scroll_count} - Height: {last_height} → {new_height}")

                last_height = new_height

            logger.info(f"✓ Scrolling completed after {scroll_count} scrolls")
            return True

        except Exception as e:
            logger.error(f"✗ Scrolling error: {str(e)}")
            return False

    def extract_linkedin_jobs(self, role="investor relations", location="mumbai") -> List[Dict]:
        """Extract investor relations jobs from LinkedIn"""
        url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}&sort=M"
        jobs = []

        try:
            self.scroll_until_complete(url, max_scrolls=10)

            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.base-card.relative.w-full.h-full.bg-white")
            logger.info(f"📊 Found {len(job_cards)} job cards on LinkedIn")

            for idx, card in enumerate(job_cards, 1):
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text
                    company = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "LinkedIn",
                        "scraped_at": datetime.now().isoformat(),
                        "job_id": f"linkedin_{idx}"
                    }

                    jobs.append(job_data)
                    logger.info(f"  ✓ [{idx}] {title} @ {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"✗ Error on LinkedIn: {str(e)}")

        return jobs

    def extract_indeed_jobs(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Extract investor relations jobs from Indeed India"""
        url = f"https://in.indeed.com/jobs?q={role}&l={location}&sort=date"
        jobs = []

        try:
            self.scroll_until_complete(url, max_scrolls=10)

            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            logger.info(f"📊 Found {len(job_cards)} job cards on Indeed")

            for idx, card in enumerate(job_cards, 1):
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text
                    company = card.find_element(By.CSS_SELECTOR, "span.companyName").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "div.companyLocation").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "Indeed",
                        "scraped_at": datetime.now().isoformat(),
                        "job_id": f"indeed_{idx}"
                    }

                    jobs.append(job_data)
                    logger.info(f"  ✓ [{idx}] {title} @ {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"✗ Error on Indeed: {str(e)}")

        return jobs

    def extract_naukri_jobs(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Extract investor relations jobs from Naukri"""
        url = f"https://www.naukri.com/jobs-{'-'.join(role.split())}--in-{location}?sort=recent"
        jobs = []

        try:
            self.scroll_until_complete(url, max_scrolls=10)

            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "article.jobTuple")
            logger.info(f"📊 Found {len(job_cards)} job cards on Naukri")

            for idx, card in enumerate(job_cards, 1):
                try:
                    title = card.find_element(By.CSS_SELECTOR, "a.title").text
                    company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "span.locSpan").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "Naukri",
                        "scraped_at": datetime.now().isoformat(),
                        "job_id": f"naukri_{idx}"
                    }

                    jobs.append(job_data)
                    logger.info(f"  ✓ [{idx}] {title} @ {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"✗ Error on Naukri: {str(e)}")

        return jobs

    def extract_glassdoor_jobs(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Extract investor relations jobs from Glassdoor India"""
        url = f"https://www.glassdoor.co.in/Jobs/{role}-jobs-SRCH_IL.0,6_KO7,{len(role)}.htm?location={location}"
        jobs = []

        try:
            self.scroll_until_complete(url, max_scrolls=8)

            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.JobCard_jobCardContainer__base")
            logger.info(f"📊 Found {len(job_cards)} job cards on Glassdoor")

            for idx, card in enumerate(job_cards, 1):
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.JobCard_jobTitle").text
                    company = card.find_element(By.CSS_SELECTOR, "div.EmployerLogo_companyName").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "div.JobCard_location").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "Glassdoor",
                        "scraped_at": datetime.now().isoformat(),
                        "job_id": f"glassdoor_{idx}"
                    }

                    jobs.append(job_data)
                    logger.info(f"  ✓ [{idx}] {title} @ {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"✗ Error on Glassdoor: {str(e)}")

        return jobs

    def filter_jobs(self, role="investor relations", location="mumbai") -> List[Dict]:
        """Filter jobs by exact role and location keywords"""
        filtered = []
        role_lower = role.lower()
        location_lower = location.lower()

        for job in self.jobs:
            title_match = role_lower in job["title"].lower()
            location_match = location_lower in job["location"].lower()

            if title_match and location_match:
                filtered.append(job)

        logger.info(f"✓ Filtered to {len(filtered)} jobs matching '{role}' in '{location}'")
        return filtered

    def remove_duplicates(self) -> List[Dict]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []

        for job in self.jobs:
            key = (job["title"].lower(), job["company"].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        logger.info(f"✓ Removed duplicates: {len(self.jobs)} → {len(unique_jobs)} unique jobs")
        self.jobs = unique_jobs
        return unique_jobs

    def save_to_json(self, jobs: List[Dict], filename: str) -> bool:
        """Save jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Saved {len(jobs)} jobs to {filename}")
            return True
        except Exception as e:
            logger.error(f"✗ Error saving to {filename}: {str(e)}")
            return False

    def close(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("🔌 WebDriver closed")

    def scrape_all_sources(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Scrape investor relations jobs from all sources with scrolling"""
        try:
            self.setup_driver()

            logger.info("\n" + "="*60)
            logger.info(f"🔍 Starting Investor Relations Web Scraper")
            logger.info(f"   Role: {role}")
            logger.info(f"   Location: {location}")
            logger.info("="*60 + "\n")

            # Scrape from LinkedIn
            logger.info("📱 Scraping LinkedIn...")
            linkedin_jobs = self.extract_linkedin_jobs(role, location)
            self.jobs.extend(linkedin_jobs)
            logger.info(f"   └─ Added {len(linkedin_jobs)} jobs from LinkedIn\n")

            # Scrape from Indeed
            logger.info("🔎 Scraping Indeed...")
            indeed_jobs = self.extract_indeed_jobs(role, location)
            self.jobs.extend(indeed_jobs)
            logger.info(f"   └─ Added {len(indeed_jobs)} jobs from Indeed\n")

            # Scrape from Naukri
            logger.info("🏢 Scraping Naukri...")
            naukri_jobs = self.extract_naukri_jobs(role, location)
            self.jobs.extend(naukri_jobs)
            logger.info(f"   └─ Added {len(naukri_jobs)} jobs from Naukri\n")

            # Scrape from Glassdoor
            logger.info("⭐ Scraping Glassdoor...")
            glassdoor_jobs = self.extract_glassdoor_jobs(role, location)
            self.jobs.extend(glassdoor_jobs)
            logger.info(f"   └─ Added {len(glassdoor_jobs)} jobs from Glassdoor\n")

            # Remove duplicates
            self.remove_duplicates()

            # Save raw data
            self.save_to_json(self.jobs, "investor_relations_mumbai_raw.json")

            # Filter and save
            filtered = self.filter_jobs(role, location)
            self.save_to_json(filtered, "investor_relations_mumbai_filtered.json")

            logger.info("\n" + "="*60)
            logger.info(f"✅ Scraping Complete!")
            logger.info(f"   Total Raw Jobs: {len(self.jobs)}")
            logger.info(f"   Filtered Jobs: {len(filtered)}")
            logger.info("="*60 + "\n")

            return filtered

        except Exception as e:
            logger.error(f"✗ Error in scrape_all_sources: {str(e)}")
            return []

        finally:
            self.close()

    def print_results(self, jobs: List[Dict]):
        """Print formatted results"""
        if not jobs:
            print("\n❌ No jobs found matching your criteria.\n")
            return

        print(f"\n✅ Found {len(jobs)} Investor Relations Jobs in Mumbai!\n")
        print("-" * 80)

        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company:    {job['company']}")
            print(f"   Location:   {job['location']}")
            print(f"   Source:     {job['source']}")
            print(f"   Scraped:    {job['scraped_at']}")

        print("\n" + "-" * 80)
        print(f"\n📊 Summary:")
        sources = {}
        for job in jobs:
            source = job['source']
            sources[source] = sources.get(source, 0) + 1

        for source, count in sorted(sources.items()):
            print(f"   • {source}: {count} jobs")

        unique_companies = set(job['company'] for job in jobs)
        print(f"   • Unique Companies: {len(unique_companies)}")
        print()


def main():
    """Main execution function"""
    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Mumbai"
    )
    scroller.print_results(jobs)


if __name__ == "__main__":
    main()
