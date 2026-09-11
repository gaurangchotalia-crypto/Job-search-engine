#!/usr/bin/env python3
"""Simple Investor Relations Job Scraper - HTTP-based (No Chrome Required!)"""

import requests
import json
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleIRScraper:
    """Simple HTTP-based scraper for IR jobs - No Chrome needed!"""

    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_indeed(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Scrape jobs from Indeed India"""
        jobs = []
        try:
            logger.info(f"🔎 Scraping Indeed for '{role}' in {location}...")
            url = f"https://in.indeed.com/jobs?q={role}&l={location}&sort=date"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                logger.info(f"   Found {len(job_cards)} job cards on Indeed")
                for idx, card in enumerate(job_cards[:15], 1):
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        if title_elem and company_elem:
                            job = {
                                "title": title_elem.get_text(strip=True),
                                "company": company_elem.get_text(strip=True),
                                "location": location_elem.get_text(strip=True) if location_elem else "Not specified",
                                "source": "Indeed",
                                "scraped_at": datetime.now().isoformat(),
                                "job_id": f"indeed_{idx}"
                            }
                            jobs.append(job)
                            logger.info(f"   ✓ [{idx}] {job['title']} @ {job['company']}")
                    except Exception as e:
                        logger.debug(f"   Error parsing job: {str(e)}")
                        continue
        except Exception as e:
            logger.error(f"✗ Error scraping Indeed: {str(e)}")
        return jobs

    def scrape_naukri(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Scrape jobs from Naukri"""
        jobs = []
        try:
            logger.info(f"🏢 Scraping Naukri for '{role}' in {location}...")
            role_formatted = '-'.join(role.split())
            url = f"https://www.naukri.com/jobs-{role_formatted}--in-{location}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('article', class_='jobTuple')
                logger.info(f"   Found {len(job_cards)} job cards on Naukri")
                for idx, card in enumerate(job_cards[:15], 1):
                    try:
                        title_elem = card.find('a', class_='title')
                        company_elem = card.find('a', class_='comp-name')
                        location_elem = card.find('span', class_='locSpan')
                        if title_elem and company_elem:
                            job = {
                                "title": title_elem.get_text(strip=True),
                                "company": company_elem.get_text(strip=True),
                                "location": location_elem.get_text(strip=True) if location_elem else "Not specified",
                                "source": "Naukri",
                                "scraped_at": datetime.now().isoformat(),
                                "job_id": f"naukri_{idx}"
                            }
                            jobs.append(job)
                            logger.info(f"   ✓ [{idx}] {job['title']} @ {job['company']}")
                    except Exception as e:
                        logger.debug(f"   Error parsing job: {str(e)}")
                        continue
        except Exception as e:
            logger.error(f"✗ Error scraping Naukri: {str(e)}")
        return jobs

    def filter_jobs(self, role="investor relations", location="mumbai") -> List[Dict]:
        """Filter jobs by role and location"""
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
        """Remove duplicate jobs"""
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
        """Save jobs to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Saved {len(jobs)} jobs to {filename}")
            return True
        except Exception as e:
            logger.error(f"✗ Error saving to {filename}: {str(e)}")
            return False

    def print_results(self, jobs: List[Dict]):
        """Print formatted results"""
        if not jobs:
            print("\n❌ No jobs found.\n")
            return
        print(f"\n✅ Found {len(jobs)} Investor Relations Jobs!\n")
        print("-" * 80)
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company:  {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Source:   {job['source']}")
        print("\n" + "-" * 80)
        sources = {}
        for job in jobs:
            source = job['source']
            sources[source] = sources.get(source, 0) + 1
        print(f"\n📊 Summary:")
        for source, count in sorted(sources.items()):
            print(f"   • {source}: {count} jobs")
        unique_companies = set(job['company'] for job in jobs)
        print(f"   • Unique Companies: {len(unique_companies)}\n")

    def scrape(self, role="investor relations", location="Mumbai") -> List[Dict]:
        """Main scraping function"""
        print("\n" + "="*80)
        print(f"  🔍 SIMPLE INVESTOR RELATIONS JOB SCRAPER (HTTP-Based)")
        print("="*80)
        print(f"  Role:     {role}")
        print(f"  Location: {location}")
        print("="*80 + "\n")
        logger.info(f"Starting HTTP-based scraper for '{role}' in '{location}'")
        indeed_jobs = self.scrape_indeed(role, location)
        self.jobs.extend(indeed_jobs)
        time.sleep(1)
        naukri_jobs = self.scrape_naukri(role, location)
        self.jobs.extend(naukri_jobs)
        time.sleep(1)
        self.remove_duplicates()
        self.save_to_json(self.jobs, "ir_jobs_raw.json")
        filtered = self.filter_jobs(role, location)
        self.save_to_json(filtered, "ir_jobs_filtered.json")
        print(f"\n✨ Scraping Complete!")
        print(f"   Total Raw Jobs: {len(self.jobs)}")
        print(f"   Filtered Jobs: {len(filtered)}\n")
        return filtered

def main():
    """Main execution"""
    scraper = SimpleIRScraper()
    jobs = scraper.scrape(role="investor relations", location="Mumbai")
    scraper.print_results(jobs)

if __name__ == "__main__":
    main()
