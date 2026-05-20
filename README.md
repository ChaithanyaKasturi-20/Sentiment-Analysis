# Sentiment Analysis Web App

A Flask-based web application that performs sentiment analysis on e-commerce product reviews scraped from Amazon. The app analyzes reviews to determine polarity, subjectivity, and detects sarcasm or excitement.

## Features

- Web scraping of Amazon product reviews
- Sentiment analysis using TextBlob
- Detection of sarcasm and excitement in reviews
- Web-based user interface
- RESTful API endpoint for analysis

## Prerequisites

- Python 3.7 or higher
- Internet connection for scraping reviews

## Installation

1. **Clone or download the repository:**
   ```
   git clone https://github.com/ChaithanyaKasturi-20/Sentiment-Analysis.git
   cd Sentiment-Analysis
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```


## Dependencies

The following Python packages are required:

- Flask==2.3.3 - Web framework
- requests==2.31.0 - HTTP library for web scraping
- beautifulsoup4==4.12.2 - HTML parsing library
- textblob==0.17.1 - Natural language processing library for sentiment analysis
- playwright - Optional browser automation fallback to expand JS-rendered reviews

If you plan to enable the browser fallback install Playwright and the browser binaries after installing packages:

```
playwright install
```

## Running the Application

1. **Start the Flask server:**
   ```
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:5000/
   ```

3. **Usage:**
   - Paste an Amazon product URL into the input field
   - Click "Analyze Feedback" to scrape and analyze reviews
   - View the sentiment analysis results including polarity, subjectivity, and detected emotions

## API Usage

The application also provides a REST API endpoint:

**Endpoint:** `POST /analyze`

**Request Body:**
```json
{
  "url": "https://www.amazon.com/product-url"
}
```

**Response:**
```json
{
  "reviews": [
    {
      "review": "Review text...",
      "polarity": 0.5,
      "subjectivity": 0.3,
      "sentiment": "Positive 😊"
    }
  ],
  "average_polarity": 0.45,
  "average_subjectivity": 0.32
}
```

## Project Structure

```
Sentiment-Analysis/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static files (images, CSS, JS)
│   └── Emojis.jpg        # Background image
└── templates/            # HTML templates
    └── index.html        # Main web interface
```

## How It Works

1. **Review Extraction:** The app scrapes customer reviews from Amazon product pages using BeautifulSoup and requests.

2. **Sentiment Analysis:** Uses TextBlob to analyze the polarity (positive/negative) and subjectivity (opinionated/factual) of each review.

3. **Special Detection:** Custom algorithms detect sarcasm and excitement based on specific phrases and punctuation patterns.

4. **Results Display:** Presents individual review analyses along with overall averages.

## Notes

- The app runs in debug mode by default for development purposes.
- Web scraping may be subject to Amazon's terms of service. Use responsibly.
- For production deployment, consider using a WSGI server like Gunicorn instead of the built-in Flask development server.

## Troubleshooting

- If you encounter import errors, ensure all dependencies are installed: `pip install -r requirements.txt`
- If the web scraper fails, Amazon may have changed their page structure. The app tries multiple selectors to handle this.
- For permission errors on Windows when activating venv, you may need to run PowerShell as administrator or change execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Quick Start Commands

Copy and paste these commands in sequence to set up and run the application:

```bash
git clone https://github.com/ChaithanyaKasturi-20/Sentiment-Analysis.git
cd Sentiment-Analysis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open your browser to `http://127.0.0.1:5000/`