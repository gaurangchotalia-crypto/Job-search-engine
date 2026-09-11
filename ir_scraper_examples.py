#!/usr/bin/env python3
"""
Examples demonstrating the Investor Relations Web Scraper usage
Run individual examples to see different scraping scenarios
"""

from investor_relations_scraper import InvestorRelationsWebScroller
import json


def example_1_basic_scraping():
    """Example 1: Basic scraping - search for IR jobs in Mumbai"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic IR Jobs Scraping - Mumbai")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Mumbai"
    )

    print(f"\n✓ Found {len(jobs)} jobs total")
    print(f"✓ Results saved to: investor_relations_mumbai_filtered.json")


def example_2_different_location():
    """Example 2: Search for IR jobs in different location"""
    print("\n" + "="*80)
    print("EXAMPLE 2: IR Jobs Scraping - Bangalore")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Bangalore"
    )

    print(f"\n✓ Found {len(jobs)} jobs in Bangalore")

    # Analyze results by source
    sources = {}
    for job in jobs:
        source = job['source']
        sources[source] = sources.get(source, 0) + 1

    print("\nJobs by source:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {source}: {count} jobs")


def example_3_different_role():
    """Example 3: Search for different role (Business Analyst)"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Different Role - Business Analyst in Mumbai")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="business analyst",
        location="Mumbai"
    )

    print(f"\n✓ Found {len(jobs)} Business Analyst jobs in Mumbai")

    # Show unique companies
    companies = set(job['company'] for job in jobs)
    print(f"✓ From {len(companies)} unique companies")


def example_4_single_source():
    """Example 4: Scrape from a single source only"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Single Source - LinkedIn Only")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    scroller.setup_driver()

    try:
        print("Scraping LinkedIn...")
        linkedin_jobs = scroller.extract_linkedin_jobs("investor relations", "Mumbai")
        print(f"\n✓ Found {len(linkedin_jobs)} jobs on LinkedIn")

        # Save to file
        scroller.save_to_json(linkedin_jobs, "linkedin_ir_mumbai.json")
        print(f"✓ Saved to: linkedin_ir_mumbai.json")

        # Display sample
        if linkedin_jobs:
            print(f"\nSample job:")
            job = linkedin_jobs[0]
            print(f"  Title: {job['title']}")
            print(f"  Company: {job['company']}")
            print(f"  Location: {job['location']}")

    finally:
        scroller.close()


def example_5_aggressive_scrolling():
    """Example 5: Aggressive scrolling for comprehensive results"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Aggressive Scrolling - Maximum Coverage")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(
        headless=True,
        timeout=20,
        scroll_pause=3
    )

    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Mumbai"
    )

    print(f"\n✓ Aggressive scraping found {len(jobs)} total jobs")

    # Analyze job titles
    titles = {}
    for job in jobs:
        title = job['title']
        titles[title] = titles.get(title, 0) + 1

    print(f"\nUnique job titles ({len(titles)} total):")
    for title, count in sorted(titles.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {title}: {count} opening(s)")


def example_6_duplicate_handling():
    """Example 6: Demonstrating duplicate removal"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Duplicate Removal")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    scroller.setup_driver()

    try:
        # Scrape multiple sources
        print("Scraping multiple sources...")
        linkedin_jobs = scroller.extract_linkedin_jobs("investor relations", "Mumbai")
        indeed_jobs = scroller.extract_indeed_jobs("investor relations", "Mumbai")

        scroller.jobs.extend(linkedin_jobs)
        scroller.jobs.extend(indeed_jobs)

        print(f"\nBefore deduplication: {len(scroller.jobs)} jobs")

        # Remove duplicates
        unique_jobs = scroller.remove_duplicates()
        print(f"After deduplication: {len(unique_jobs)} unique jobs")
        print(f"Duplicates removed: {len(scroller.jobs) - len(unique_jobs)}")

    finally:
        scroller.close()


def example_7_advanced_filtering():
    """Example 7: Advanced filtering with custom criteria"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Advanced Filtering")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Mumbai"
    )

    # Custom filtering
    senior_jobs = [j for j in jobs if 'senior' in j['title'].lower()]
    manager_jobs = [j for j in jobs if 'manager' in j['title'].lower()]
    executive_jobs = [j for j in jobs if 'executive' in j['title'].lower()]

    print(f"Total jobs found: {len(jobs)}")
    print(f"Senior positions: {len(senior_jobs)}")
    print(f"Manager positions: {len(manager_jobs)}")
    print(f"Executive positions: {len(executive_jobs)}")

    # Filter by company
    print("\nJobs by company (top 5):")
    companies = {}
    for job in jobs:
        company = job['company']
        companies[company] = companies.get(company, 0) + 1

    for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • {company}: {count} job(s)")


def example_8_export_formats():
    """Example 8: Export results in different formats"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Export Formats")
    print("="*80 + "\n")

    scroller = InvestorRelationsWebScroller(headless=True)
    jobs = scroller.scrape_all_sources(
        role="investor relations",
        location="Mumbai"
    )

    # JSON export
    scroller.save_to_json(jobs, "ir_jobs_export.json")
    print("✓ Exported to JSON: ir_jobs_export.json")

    # CSV export
    if jobs:
        import csv
        with open('ir_jobs_export.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
            writer.writeheader()
            writer.writerows(jobs)
        print("✓ Exported to CSV: ir_jobs_export.csv")

    # Markdown export
    with open('ir_jobs_export.md', 'w', encoding='utf-8') as f:
        f.write("# Investor Relations Jobs in Mumbai\n\n")
        f.write(f"**Total Jobs Found**: {len(jobs)}\n\n")

        for i, job in enumerate(jobs, 1):
            f.write(f"## {i}. {job['title']}\n")
            f.write(f"- **Company**: {job['company']}\n")
            f.write(f"- **Location**: {job['location']}\n")
            f.write(f"- **Source**: {job['source']}\n\n")

    print("✓ Exported to Markdown: ir_jobs_export.md")


def example_9_performance_comparison():
    """Example 9: Compare different scrolling strategies"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Performance Comparison")
    print("="*80 + "\n")

    import time

    configs = [
        ("Fast", {"max_scrolls": 5, "scroll_pause": 1}),
        ("Balanced", {"max_scrolls": 15, "scroll_pause": 2}),
        ("Comprehensive", {"max_scrolls": 20, "scroll_pause": 3}),
    ]

    for config_name, params in configs:
        print(f"\n{config_name} Mode:")
        print(f"  Max scrolls: {params['max_scrolls']}")
        print(f"  Scroll pause: {params['scroll_pause']}s")

        start_time = time.time()

        scroller = InvestorRelationsWebScroller(
            headless=True,
            scroll_pause=params['scroll_pause']
        )
        scroller.setup_driver()

        try:
            linkedin_jobs = scroller.extract_linkedin_jobs("investor relations", "Mumbai")
            elapsed = time.time() - start_time

            print(f"  Jobs found: {len(linkedin_jobs)}")
            print(f"  Time taken: {elapsed:.2f} seconds")

        finally:
            scroller.close()


def example_10_multi_location():
    """Example 10: Scrape from multiple locations"""
    print("\n" + "="*80)
    print("EXAMPLE 10: Multi-Location Search")
    print("="*80 + "\n")

    locations = ["Mumbai", "Bangalore", "Delhi"]
    all_jobs = {}

    scroller = InvestorRelationsWebScroller(headless=True)

    for location in locations:
        print(f"\nScraping {location}...")
        jobs = scroller.scrape_all_sources(
            role="investor relations",
            location=location
        )
        all_jobs[location] = jobs
        print(f"✓ Found {len(jobs)} jobs in {location}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for location, jobs in all_jobs.items():
        print(f"{location}: {len(jobs)} jobs")

    total = sum(len(jobs) for jobs in all_jobs.values())
    print(f"\nTotal across all locations: {total} jobs")


# Run examples
if __name__ == "__main__":
    print("\n" + "="*80)
    print("INVESTOR RELATIONS WEB SCRAPER - USAGE EXAMPLES")
    print("="*80)
    print("\nUncomment the example you want to run in the main block below.")
    print("Each example demonstrates different features and use cases.\n")

    # Uncomment one of the examples to run:

    # example_1_basic_scraping()
    # example_2_different_location()
    # example_3_different_role()
    # example_4_single_source()
    # example_5_aggressive_scrolling()
    # example_6_duplicate_handling()
    # example_7_advanced_filtering()
    # example_8_export_formats()
    # example_9_performance_comparison()
    # example_10_multi_location()

    print("To run examples, uncomment them in the main block of this script.")
