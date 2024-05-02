import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize Vader sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    # Process text using spaCy
    doc = nlp(text)

    # Get sentences from the document
    sentences = [sent.text for sent in doc.sents]

    # Analyze sentiment for each sentence using Vader
    overall_sentiment = 0
    for sentence in sentences:
        sentiment_score = analyzer.polarity_scores(sentence)
        overall_sentiment += sentiment_score['compound']

    # Determine overall sentiment label
    if overall_sentiment >= 0.05:
        return 'Positive'
    elif overall_sentiment <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
