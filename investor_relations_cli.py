#!/usr/bin/env python3
"""
CLI Tool for Investor Relations Job Scraper with Web Scrolling
Scrapes investor relations jobs from multiple sources in specified locations
"""

import argparse
import sys
import json
from pathlib import Path
from investor_relations_scraper import InvestorRelationsWebScroller


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Investor Relations Web Scraper - Multi-source job aggregator with advanced scrolling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python investor_relations_cli.py                              # Default: IR jobs in Mumbai
  python investor_relations_cli.py --location Bangalore         # Search in Bangalore
  python investor_relations_cli.py --role "business analyst"    # Different role
  python investor_relations_cli.py --no-headless                # Show browser window
  python investor_relations_cli.py --max-scrolls 20 --timeout 20 # More aggressive scrolling
  python investor_relations_cli.py --output custom_results.json # Save to custom file
  python investor_relations_cli.py --scroll-pause 3             # 3 second pause between scrolls
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
        default='investor_relations_mumbai_filtered.json',
        help='Output file for filtered results (default: investor_relations_mumbai_filtered.json)'
    )

    parser.add_argument(
        '--output-raw',
        default='investor_relations_mumbai_raw.json',
        help='Output file for raw results (default: investor_relations_mumbai_raw.json)'
    )

    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in non-headless mode (display browser window)'
    )

    parser.add_argument(
        '--max-scrolls',
        type=int,
        default=15,
        help='Maximum scrolls per source (default: 15)'
    )

    parser.add_argument(
        '--scroll-pause',
        type=float,
        default=2,
        help='Pause time between scrolls in seconds (default: 2)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=15,
        help='WebDriver timeout in seconds (default: 15)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging output'
    )

    parser.add_argument(
        '--statistics',
        action='store_true',
        help='Display detailed statistics after scraping'
    )

    return parser.parse_args()


def print_header(role, location):
    """Print application header"""
    print("\n" + "="*80)
    print("  🔍 INVESTOR RELATIONS WEB SCRAPER - MULTI-SOURCE JOB AGGREGATOR")
    print("="*80)
    print(f"  Role:     {role}")
    print(f"  Location: {location}")
    print("="*80 + "\n")


def print_results(jobs, show_detailed=False):
    """Print job results in formatted display"""
    if not jobs:
        print("\n❌ No jobs found matching your criteria.\n")
        return

    print(f"\n✅ Found {len(jobs)} Investor Relations Jobs!\n")
    print("-" * 80)

    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company:    {job['company']}")
        print(f"   Location:   {job['location']}")
        print(f"   Source:     {job['source']}")
        if show_detailed:
            print(f"   Job ID:     {job.get('job_id', 'N/A')}")
            print(f"   Scraped:    {job['scraped_at']}")

    print("\n" + "-" * 80 + "\n")


def print_statistics(jobs):
    """Print detailed statistics"""
    if not jobs:
        return

    print("📊 STATISTICS\n" + "-" * 80)

    # Source breakdown
    sources = {}
    for job in jobs:
        source = job['source']
        sources[source] = sources.get(source, 0) + 1

    print("\n📱 Jobs by Source:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(jobs)) * 100
        bar = "█" * int(percentage / 5)
        print(f"   {source:12} {count:3} jobs {bar} ({percentage:.1f}%)")

    # Company breakdown
    companies = {}
    for job in jobs:
        company = job['company']
        companies[company] = companies.get(company, 0) + 1

    print(f"\n🏢 Unique Companies: {len(companies)}")
    print("\n   Top 10 Companies with Most Openings:")
    for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {company}: {count} opening(s)")

    # Title variations
    titles = {}
    for job in jobs:
        title = job['title']
        titles[title] = titles.get(title, 0) + 1

    print(f"\n📋 Unique Job Titles: {len(titles)}")
    print("\n   Most Common Titles:")
    for title, count in sorted(titles.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   • {title}: {count} opening(s)")

    print("\n" + "-" * 80 + "\n")


def run_scraper(args):
    """Run the scraper with provided arguments"""
    print_header(args.role, args.location)

    try:
        print(f"⚙️  Initializing web scraper...")
        print(f"   • Headless mode: {'OFF' if args.no_headless else 'ON'}")
        print(f"   • Max scrolls: {args.max_scrolls}")
        print(f"   • Scroll pause: {args.scroll_pause}s")
        print(f"   • Timeout: {args.timeout}s\n")

        scroller = InvestorRelationsWebScroller(
            headless=not args.no_headless,
            timeout=args.timeout,
            scroll_pause=args.scroll_pause
        )

        # Run scraper
        filtered_jobs = scroller.scrape_all_sources(
            role=args.role,
            location=args.location
        )

        # Print results
        print_results(filtered_jobs, show_detailed=args.verbose)

        # Print statistics if requested
        if args.statistics:
            print_statistics(filtered_jobs)

        # Summary
        print(f"💾 Filtered results saved to: {args.output}")
        print(f"💾 Raw results saved to: {args.output_raw}")

        if filtered_jobs:
            print(f"\n✨ Total relevant jobs found: {len(filtered_jobs)}")
            return True
        else:
            print("\n⚠️  No relevant jobs found. Try different search criteria.")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


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
