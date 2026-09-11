from flask import Flask, render_template, request, jsonify, send_file
from scraper import JobScraper
import json
import os
from threading import Thread
import logging

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scraper_status = {
    "running": False,
    "progress": 0,
    "message": ""
}

@app.route('/')
def index():
    """Render home page"""
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def start_scrape():
    """Start scraping job listings"""
    data = request.json
    role = data.get('role', 'investor relations')
    location = data.get('location', 'Mumbai')

    if scraper_status['running']:
        return jsonify({'error': 'Scraper already running'}), 400

    def run_scraper():
        scraper_status['running'] = True
        scraper_status['progress'] = 0
        scraper_status['message'] = 'Starting scraper...'

        try:
            scraper = JobScraper(headless=True)
            jobs = scraper.scrape_all_sources(role, location)

            scraper_status['progress'] = 100
            scraper_status['message'] = f'Found {len(jobs)} jobs'
            scraper_status['running'] = False

            logger.info(f"Scraping completed with {len(jobs)} jobs")

        except Exception as e:
            scraper_status['message'] = f'Error: {str(e)}'
            scraper_status['running'] = False
            logger.error(f"Scraper error: {str(e)}")

    thread = Thread(target=run_scraper)
    thread.daemon = True
    thread.start()

    return jsonify({
        'status': 'started',
        'role': role,
        'location': location
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get scraper status"""
    return jsonify(scraper_status)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get scraped jobs from file"""
    file_path = 'investor_relations_mumbai.json'

    if not os.path.exists(file_path):
        return jsonify({'jobs': [], 'total': 0})

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        return jsonify({'jobs': jobs, 'total': len(jobs)})
    except Exception as e:
        logger.error(f"Error reading jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/download', methods=['GET'])
def download_jobs():
    """Download jobs as JSON"""
    file_path = 'investor_relations_mumbai.json'

    if not os.path.exists(file_path):
        return jsonify({'error': 'No jobs file found'}), 404

    try:
        return send_file(file_path, as_attachment=True, download_name='investor_relations_jobs.json')
    except Exception as e:
        logger.error(f"Error downloading jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/clear', methods=['DELETE'])
def clear_jobs():
    """Clear cached jobs"""
    try:
        if os.path.exists('investor_relations_mumbai.json'):
            os.remove('investor_relations_mumbai.json')
        if os.path.exists('jobs_raw.json'):
            os.remove('jobs_raw.json')
        return jsonify({'status': 'cleared'})
    except Exception as e:
        logger.error(f"Error clearing jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
