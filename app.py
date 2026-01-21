from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

app = Flask(__name__)

def detect_sarcasm(text):
    """ 
    Detect sarcasm based on common sarcastic phrases or punctuation.
    """
    sarcastic_phrases = [
        "yeah right", "as if", "sure", "of course", "whatever", 
        "oh great", "oh wonderful", "oh fantastic", "oh brilliant", 
        "real funny", "nice one", "good job"
    ]
    # Check for sarcastic phrases
    if any(phrase in text.lower() for phrase in sarcastic_phrases):
        return True
    # Check for mixed punctuation (e.g., "Oh, great!")
    if "!" in text and ("?" in text or "," in text):
        return True
    return False

def detect_excitement(text):
    """
    Detect excitement based on exclamation marks and positive words.
    """
    excitement_words = [
        "wow", "amazing", "awesome", "excited", "love", 
        "great", "happy", "yay", "fantastic", "thrilled"
    ]
    # Check for excitement words
    if any(word in text.lower() for word in excitement_words):
        return True
    # Check for multiple exclamation marks
    if text.count("!") >= 2:
        return True
    return False

def extract_amazon_reviews(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.amazon.com/",
        "DNT": "1",
    }
    
    try:
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple selectors for different Amazon layouts
        review_selectors = [
            {"data-hook": "review-body"},  # Most common
            {"class": "a-size-base review-text"},  # Alternative
            {"class": "review-text-content"}  # Another alternative
        ]
        
        reviews = []
        for selector in review_selectors:
            found_reviews = soup.find_all("span", selector)
            if found_reviews:
                reviews.extend([review.get_text(strip=True) for review in found_reviews])
                break
        
        # If still no reviews, check if it's a different Amazon domain
        if not reviews and "amazon." in product_url:
            domain = product_url.split("amazon.")[1].split("/")[0]
            if domain != "com":
                # Try with US domain
                us_url = product_url.replace(f"amazon.{domain}", "amazon.com")
                return extract_amazon_reviews(us_url)
        
        return reviews
    
    except Exception as e:
        print(f"Error scraping reviews: {e}")
        return []

def analyze_sentiment(reviews):
    """
    Analyze the sentiment of a list of reviews.
    """
    results = []
    for review in reviews:
        blob = TextBlob(review)
        sentiment = blob.sentiment

        # Determine sentiment label
        if detect_sarcasm(review):
            sentiment_label = 'Sarcasm 😏'  # Sarcasm detected
        elif detect_excitement(review):
            sentiment_label = 'Excitement 🎉'  # Excitement detected
        elif sentiment.polarity> 0:
            sentiment_label = 'Positive 😊'  # Positive sentiment
        elif sentiment.polarity< 0:
            sentiment_label = 'Negative 😠'  # Negative sentiment
        else:
            sentiment_label = 'Neutral 😐'  # Neutral sentiment

        results.append({
            "review": review,
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity,
            "sentiment": sentiment_label
        })
    return results
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_feedback():
    data = request.json
    product_url = data.get('url')
    if not product_url:
        return jsonify({'error': 'No product URL provided'}), 400

    try:
        # Extract reviews from the product URL
        reviews = extract_amazon_reviews(product_url)
        if not reviews:
            return jsonify({'error': 'No reviews found on the page'}), 404

        # Analyze the sentiment of the reviews
        results = analyze_sentiment(reviews)

        # Calculate average sentiment
        avg_polarity = sum(result['polarity'] for result in results) / len(results)
        avg_subjectivity = sum(result['subjectivity'] for result in results) / len(results)

        return jsonify({
            'reviews': results,
            'average_polarity': avg_polarity,
            'average_subjectivity': avg_subjectivity
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
