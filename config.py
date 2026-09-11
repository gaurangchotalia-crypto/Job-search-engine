"""Configuration settings for the Job Scraper"""

# Scraper Settings
SCRAPER_CONFIG = {
    'headless': True,
    'max_scrolls': 5,
    'scroll_pause': 2,
    'timeout': 30,
}

# Job Portal URLs
PORTALS = {
    'indeed': {
        'base_url': 'https://in.indeed.com',
        'search_path': '/jobs',
        'selectors': {
            'job_cards': 'div.job_seen_beacon',
            'title': 'h2.jobTitle span',
            'company': 'span.companyName',
            'location': 'div.companyLocation',
        }
    },
    'naukri': {
        'base_url': 'https://www.naukri.com',
        'search_path': '/jobs',
        'selectors': {
            'job_cards': 'article.jobTuple',
            'title': 'a.title',
            'company': 'a.comp-name',
            'location': 'span.locSpan',
        }
    },
    'linkedin': {
        'base_url': 'https://www.linkedin.com',
        'search_path': '/jobs/search',
        'selectors': {
            'job_cards': 'div.base-card.relative.w-full.h-full.bg-white',
            'title': 'h3.base-search-card__title',
            'company': 'h4.base-search-card__subtitle',
            'location': 'span.job-search-card__location',
        }
    }
}

# Flask App Settings
FLASK_CONFIG = {
    'DEBUG': False,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'UPLOAD_FOLDER': '/tmp',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file size
}

# Output Settings
OUTPUT_CONFIG = {
    'filtered_jobs_file': 'investor_relations_mumbai.json',
    'raw_jobs_file': 'jobs_raw.json',
    'indent': 2,
    'ensure_ascii': False,
}

# Search Parameters
DEFAULT_SEARCH = {
    'role': 'investor relations',
    'location': 'Mumbai',
    'country': 'India',
}

# Browser User Agents
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

# Logging Settings
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
}
