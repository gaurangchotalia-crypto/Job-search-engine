#!/usr/bin/env python3
"""CLI for Simple HTTP-Based IR Job Scraper"""

import argparse
import sys
from simple_ir_scraper import SimpleIRScraper

def main():
    parser = argparse.ArgumentParser(
        description='Simple HTTP-Based IR Job Scraper - No Chrome/Selenium Required!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_scraper_cli.py
  python simple_scraper_cli.py --location Bangalore
  python simple_scraper_cli.py --role "business analyst"
        """
    )
    parser.add_argument('--role', default='investor relations', help='Job role to search for')
    parser.add_argument('--location', default='Mumbai', help='Location to search in')
    args = parser.parse_args()

    try:
        scraper = SimpleIRScraper()
        jobs = scraper.scrape(role=args.role, location=args.location)
        scraper.print_results(jobs)
        if jobs:
            print(f"💾 Results saved to:")
            print(f"   • ir_jobs_filtered.json (Filtered results)")
            print(f"   • ir_jobs_raw.json (All results)")
            return True
        else:
            print("⚠️  No jobs found. Try different search criteria.")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
