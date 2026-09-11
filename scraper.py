import os
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.jobs = []

    def setup_driver(self):
        """Initialize Chrome WebDriver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("WebDriver initialized successfully")

    def scroll_to_load_jobs(self, url, max_scrolls=10, scroll_pause=2):
        """Navigate to URL and scroll to load more jobs"""
        try:
            logger.info(f"Navigating to {url}")
            self.driver.get(url)
            time.sleep(3)

            scroll_count = 0
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while scroll_count < max_scrolls:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    logger.info("No more content to load")
                    break

                last_height = new_height
                scroll_count += 1
                logger.info(f"Scroll count: {scroll_count}")

            logger.info(f"Completed scrolling after {scroll_count} scrolls")

        except Exception as e:
            logger.error(f"Error during scrolling: {str(e)}")

    def extract_jobs_from_linkedin(self, role_keyword="investor relations", location="mumbai"):
        """Extract job listings from LinkedIn"""
        url = f"https://www.linkedin.com/jobs/search/?keywords={role_keyword}&location={location}"
        self.scroll_to_load_jobs(url, max_scrolls=5)

        try:
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.base-card.relative.w-full.h-full.bg-white")
            logger.info(f"Found {len(job_cards)} job cards")

            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text
                    company = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "LinkedIn",
                        "scraped_at": datetime.now().isoformat()
                    }

                    self.jobs.append(job_data)
                    logger.info(f"Extracted: {title} at {company}")

                except Exception as e:
                    logger.debug(f"Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting jobs from LinkedIn: {str(e)}")

    def extract_jobs_from_indeed(self, role_keyword="investor relations", location="Mumbai"):
        """Extract job listings from Indeed"""
        url = f"https://in.indeed.com/jobs?q={role_keyword}&l={location}"
        self.scroll_to_load_jobs(url, max_scrolls=5)

        try:
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            logger.info(f"Found {len(job_cards)} job cards on Indeed")

            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text
                    company = card.find_element(By.CSS_SELECTOR, "span.companyName").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "div.companyLocation").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "Indeed",
                        "scraped_at": datetime.now().isoformat()
                    }

                    self.jobs.append(job_data)
                    logger.info(f"Extracted: {title} at {company}")

                except Exception as e:
                    logger.debug(f"Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting jobs from Indeed: {str(e)}")

    def extract_jobs_from_naukri(self, role_keyword="investor relations", location="Mumbai"):
        """Extract job listings from Naukri (popular in India)"""
        url = f"https://www.naukri.com/jobs-{'-'.join(role_keyword.split())}--in-{location}"
        self.scroll_to_load_jobs(url, max_scrolls=5)

        try:
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "article.jobTuple")
            logger.info(f"Found {len(job_cards)} job cards on Naukri")

            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "a.title").text
                    company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text
                    location_elem = card.find_element(By.CSS_SELECTOR, "span.locSpan").text

                    job_data = {
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location_elem.strip(),
                        "source": "Naukri",
                        "scraped_at": datetime.now().isoformat()
                    }

                    self.jobs.append(job_data)
                    logger.info(f"Extracted: {title} at {company}")

                except Exception as e:
                    logger.debug(f"Error extracting job card: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting jobs from Naukri: {str(e)}")

    def filter_jobs(self, role_keyword="investor relations", location="mumbai"):
        """Filter jobs by role and location"""
        filtered = []
        role_lower = role_keyword.lower()
        location_lower = location.lower()

        for job in self.jobs:
            title_match = role_lower in job["title"].lower()
            location_match = location_lower in job["location"].lower()

            if title_match and location_match:
                filtered.append(job)

        logger.info(f"Filtered to {len(filtered)} jobs matching criteria")
        return filtered

    def save_jobs_to_json(self, filename="jobs.json"):
        """Save extracted jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, ensure_ascii=False, indent=2)
            logger.info(f"Jobs saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving jobs: {str(e)}")

    def save_filtered_jobs_to_json(self, filtered_jobs, filename="filtered_jobs.json"):
        """Save filtered jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(filtered_jobs, f, ensure_ascii=False, indent=2)
            logger.info(f"Filtered jobs saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving filtered jobs: {str(e)}")

    def close(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")

    def scrape_all_sources(self, role="investor relations", location="Mumbai"):
        """Scrape from all job sources"""
        try:
            self.setup_driver()

            logger.info("Starting scrape from Indeed...")
            self.extract_jobs_from_indeed(role, location)

            logger.info("Starting scrape from Naukri...")
            self.extract_jobs_from_naukri(role, location)

            logger.info("Starting scrape from LinkedIn...")
            self.extract_jobs_from_linkedin(role, location)

            self.save_jobs_to_json("jobs_raw.json")

            filtered = self.filter_jobs(role, location)
            self.save_filtered_jobs_to_json(filtered, "investor_relations_mumbai.json")

            logger.info(f"Scraping completed! Found {len(filtered)} relevant jobs")
            return filtered

        except Exception as e:
            logger.error(f"Error in scrape_all_sources: {str(e)}")
            return []

        finally:
            self.close()

def main():
    """Main execution function"""
    scraper = JobScraper(headless=True)
    jobs = scraper.scrape_all_sources(role="investor relations", location="Mumbai")

    print("\n" + "="*60)
    print(f"Total Jobs Found: {len(jobs)}")
    print("="*60)

    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")

if __name__ == "__main__":
    main()
