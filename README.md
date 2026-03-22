# Upwork Job Scraper

A full-stack Flask web application that scrapes Upwork job listings on demand, shows real-time scraping progress in the browser, and exports results as a downloadable CSV — plus an n8n workflow for automated Apify-based job exports to Google Sheets.

## Features

- **Web UI** — paste a search URL, click start, watch live progress
- **Background threading** — scraping runs in a background thread; UI polls for updates
- **Error recovery** — a single failed page doesn't stop the entire run
- **CSV export** — download results directly from the browser when complete
- **n8n workflow** — automated Upwork job export via Apify actor to Google Sheets

## Contents

| File | Description |
|------|-------------|
| `flask_app/app.py` | Flask backend with threading + progress API |
| `flask_app/scraper.py` | Core Upwork scraping logic (Selenium) |
| `flask_app/index.html` | Frontend with real-time progress display |
| `flask_app/upworktaks.py` | Standalone scraper script version |
| `n8n_workflows/` | Apify-based Upwork export n8n workflow JSON |

## Setup (Flask App)

```bash
pip install flask selenium pandas

# Make sure Chrome and ChromeDriver are installed
# ChromeDriver must match your Chrome version

cd flask_app
python app.py
```

Then open `http://localhost:5000` in your browser.

## Usage

1. Go to Upwork and search for jobs with your filters
2. Copy the search results URL
3. Paste it into the web app and click **Start Scraping**
4. Watch the progress bar update in real-time
5. Click **Download CSV** when complete

## n8n Workflow (Apify)

The `n8n_workflows/` folder contains an n8n workflow that:
- Triggers on a schedule or manually
- Calls the Apify Upwork scraper actor
- Exports job listings directly to a Google Sheet

**To import:** Open n8n → Workflows → Import from file → select the JSON

## Tech Stack

- Python, Flask
- Selenium + ChromeDriver
- Threading (Python standard library)
- HTML/CSS/JS (vanilla frontend)
- n8n + Apify (workflow version)

## Output Fields

`Job Title | Client | Budget | Posted Date | Skills Required | Job URL | Description`
