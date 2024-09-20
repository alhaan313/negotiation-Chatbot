import spacy
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load the spacy model for NER
nlp = spacy.load("en_core_web_sm")

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

def extract_price(text):
    """
    Extracts the price from the user's input using Named Entity Recognition (NER).
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "MONEY":  # Check if the entity is related to price/money
            return float(ent.text.replace('$', ''))  # Return numeric price
    return None

def get_happiness_level(text):
    """
    Analyzes the sentiment of the user's input and returns a happiness score from 1 to 10.
    """
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']  # Sentiment score ranging from -1 to 1
    # Map compound score to a scale of 1 to 10 for happiness
    happiness_level = round((compound_score + 1) * 5)
    return happiness_level

def calculate_new_price(initial_price, lowest_price, happiness_level):
    """
    Calculates the new price based on the initial price, lowest price, and user's happiness level.
    """
    price_diff = initial_price - lowest_price
    reduction_amount = price_diff * 0.5
    reduction_factor = happiness_level / 10.0
    price_reduction = reduction_amount * reduction_factor
    new_price = initial_price - price_reduction
    return max(new_price, lowest_price)
