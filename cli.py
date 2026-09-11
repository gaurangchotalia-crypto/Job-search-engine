import argparse
import sys
from scraper import JobScraper
import json
from pathlib import Path

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Job Scraper - Find investor relations jobs in Mumbai',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py                                    # Search for investor relations in Mumbai
  python cli.py --role "finance analyst"          # Search for different role
  python cli.py --location Bangalore               # Search in different location
  python cli.py --sources indeed                   # Scrape only from Indeed
  python cli.py --output my_results.json          # Save to custom file
        """
    )

    parser.add_argument(
        '--role',
        default='investor relations',
        help='Job role to search for (default: investor relations)'
    )

    parser.add_argument(
        '--location',
        default='Mumbai',
        help='Location to search in (default: Mumbai)'
    )

    parser.add_argument(
        '--output',
        default='investor_relations_jobs.json',
        help='Output file name (default: investor_relations_jobs.json)'
    )

    parser.add_argument(
        '--sources',
        default='indeed,naukri,linkedin',
        help='Comma-separated sources to scrape (default: indeed,naukri,linkedin)'
    )

    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in non-headless mode (show browser window)'
    )

    parser.add_argument(
        '--max-scrolls',
        type=int,
        default=5,
        help='Maximum number of scrolls per source (default: 5)'
    )

    parser.add_argument(
        '--scroll-pause',
        type=float,
        default=2,
        help='Pause time between scrolls in seconds (default: 2)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--save-raw',
        action='store_true',
        help='Save raw jobs data to jobs_raw.json'
    )

    return parser.parse_args()

def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("  Job Scraper - Investor Relations")
    print("="*60 + "\n")

def print_results(jobs):
    """Print job results in formatted table"""
    if not jobs:
        print("❌ No jobs found matching your criteria.\n")
        return

    print(f"✅ Found {len(jobs)} jobs!\n")
    print("-" * 60)

    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company:  {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source:   {job['source']}")

    print("\n" + "="*60 + "\n")

def run_scraper(args):
    """Run the scraper with provided arguments"""
    print_header()

    print(f"📍 Role:     {args.role}")
    print(f"📍 Location: {args.location}")
    print(f"📍 Sources:  {args.sources}")
    print(f"📍 Output:   {args.output}\n")

    try:
        scraper = JobScraper(headless=not args.no_headless)

        print("🔍 Initializing WebDriver...")
        scraper.setup_driver()

        sources = [s.strip() for s in args.sources.split(',')]

        if 'indeed' in sources:
            print(f"\n⏳ Scraping Indeed for '{args.role}' in {args.location}...")
            scraper.extract_jobs_from_indeed(args.role, args.location)

        if 'naukri' in sources:
            print(f"⏳ Scraping Naukri for '{args.role}' in {args.location}...")
            scraper.extract_jobs_from_naukri(args.role, args.location)

        if 'linkedin' in sources:
            print(f"⏳ Scraping LinkedIn for '{args.role}' in {args.location}...")
            scraper.extract_jobs_from_linkedin(args.role, args.location)

        print(f"\n📊 Total jobs found: {len(scraper.jobs)}")

        # Filter jobs
        filtered = scraper.filter_jobs(args.role, args.location)

        # Save filtered results
        scraper.save_filtered_jobs_to_json(filtered, args.output)
        print(f"💾 Filtered jobs saved to: {args.output}")

        # Save raw results if requested
        if args.save_raw:
            scraper.save_jobs_to_json("jobs_raw.json")
            print(f"💾 Raw jobs saved to: jobs_raw.json")

        # Print results
        print_results(filtered)

        # Print statistics
        if filtered:
            companies = set(job['company'] for job in filtered)
            sources_count = {}
            for job in filtered:
                sources_count[job['source']] = sources_count.get(job['source'], 0) + 1

            print("📈 Statistics:")
            print(f"  - Unique Companies: {len(companies)}")
            for source, count in sources_count.items():
                print(f"  - {source}: {count} jobs")
            print()

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

    finally:
        print("🔌 Closing WebDriver...")
        scraper.close()

def main():
    """Main entry point"""
    args = parse_arguments()

    # Set up logging if verbose
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    success = run_scraper(args)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
