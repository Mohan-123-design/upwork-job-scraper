from flask import Flask, render_template_string, request, jsonify, send_file
import subprocess
import os
import csv
import threading
import time
import json

app = Flask(__name__)

# Global variables to track scraping status
scraping_status = {
    'running': False,
    'completed': False,
    'error': None,
    'progress': 0,
    'message': 'Ready'
}

def read_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    return render_template_string(read_html())

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    global scraping_status

    if scraping_status['running']:
        return jsonify({'error': 'Scraping already running'}), 400

    # Reset status
    scraping_status = {
        'running': True,
        'completed': False,
        'error': None,
        'progress': 0,
        'message': 'Starting scraper...'
    }

    # Get URL from request
    data = request.get_json()
    search_url = data.get('url') if data else None

    # Start scraping in background thread
    thread = threading.Thread(target=run_scraper, args=(search_url,))
    thread.start()

    return jsonify({'success': True})

def run_scraper(search_url=None):
    global scraping_status

    try:
        # Update your scraper.py to accept URL parameter if needed
        cmd = ['python', 'scraper.py']
        if search_url:
            # You might need to modify your scraper to accept URL as argument
            cmd.extend(['--url', search_url])

        scraping_status['message'] = 'Running scraper...'
        scraping_status['progress'] = 10

        # Run the scraper
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode == 0:
            scraping_status['progress'] = 100
            scraping_status['message'] = 'Completed successfully!'
            scraping_status['completed'] = True
        else:
            scraping_status['error'] = f'Scraper failed: {process.stderr}'

    except Exception as e:
        scraping_status['error'] = f'Error running scraper: {str(e)}'
    finally:
        scraping_status['running'] = False

@app.route('/progress')
def get_progress():
    return jsonify(scraping_status)

@app.route('/results')
def get_results():
    csv_file = 'upwork_job_structured_details.csv'

    if not os.path.exists(csv_file):
        return jsonify({'jobs': []})

    jobs = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append({
                    'title': row.get('Title', ''),
                    'posted': row.get('Posted', ''),
                    'hourly': row.get('Hourly Rate', ''),
                    'location': row.get('Location', ''),
                    'spent': row.get('Spent', ''),
                    'hires': row.get('Hires', ''),
                    'invites_sent': row.get('Invites Sent', ''),
                    'summary': row.get('Summary', '')
                })
    except Exception as e:
        print(f"Error reading CSV: {e}")

    return jsonify({'jobs': jobs})

@app.route('/download')
def download_csv():
    csv_file = 'upwork_job_structured_details.csv'

    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name='upwork_jobs.csv')
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/clear', methods=['POST'])
def clear_results():
    global scraping_status

    try:
        # Remove CSV file
        if os.path.exists('upwork_job_structured_details.csv'):
            os.remove('upwork_job_structured_details.csv')

        # Remove job text files
        if os.path.exists('job_texts'):
            for file in os.listdir('job_texts'):
                os.remove(os.path.join('job_texts', file))

        # Reset status
        scraping_status = {
            'running': False,
            'completed': False,
            'error': None,
            'progress': 0,
            'message': 'Ready'
        }

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
