# Suppress TensorFlow's log messages for cleaner chatbot interaction
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow's log messages

import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

from sentiment_analysis import analyze_sentiment

# Constants
INTENTS_FILE = 'intents.json'
WORDS_FILE = 'allPatternsWords.pkl'
CLASSES_FILE = 'allIntentsTags.pkl'
MODEL_FILE = 'chatbot_model.keras'
ERROR_THRESHOLD = 0.25

tf.keras.utils.disable_interactive_logging()

lemmatizer = WordNetLemmatizer()

# Load intents data
def load_intents(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load words and classes
def load_data(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Load trained model
def load_model(file_path):
    return tf.keras.models.load_model(file_path)

# Tokenize sentence
def tokenize_sentence(sentence, lemmatizer):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word) for word in sentence_words]

# Create bag of words
def bag_of_words(sentence, words):
    sentence_words = tokenize_sentence(sentence, lemmatizer)
    bag = [0] * len(words)
    for i, word in enumerate(words):
        if word in sentence_words:
            bag[i] = 1
    return np.array(bag)

# Predict class/intent
def predict_intents(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

def predict_top_intent(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    sentence_intents = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    top_intent_tag = sentence_intents[0]['intent']
    return top_intent_tag

# Get response
def get_response(sentence, intents_data):
    sentence_intents = predict_intents(sentence, model)
    top_intent_tag = sentence_intents[0]['intent']
    responses = [intent['responses'] for intent in intents_data['intents'] if intent['tag'] == top_intent_tag]
    flat_responses = [response for sublist in responses for response in sublist]
    return random.choice(flat_responses)

def get_response_by_intent(sentence_intent, intents_data):
    responses = [intent['responses'] for intent in intents_data['intents'] if intent['tag'] == sentence_intent]
    flat_responses = [response for sublist in responses for response in sublist]
    return random.choice(flat_responses)


# Main function
def main():
    global lemmatizer, words, classes, model

    # Load data
    intents_data = load_intents(INTENTS_FILE)
    words = load_data(WORDS_FILE)
    classes = load_data(CLASSES_FILE)
    model = load_model(MODEL_FILE)

    while True:
        # Get and print response
        sentence = input("You: ")
        sentiment = analyze_sentiment(sentence)
        if sentiment == 'Negative':
            print("Your satisfaction is our priority. I'll make sure to escalate your concern to one of our "
                  "attendants, who will assist you promptly. Please hang tight; we'll have someone with you shortly.")
            break
        else:
            sentence_top_intent = predict_top_intent(sentence, model)
            response = get_response_by_intent(sentence_top_intent, intents_data)
            print("Bot: ", response)
            if sentence_top_intent == 'goodbye':
                break


if __name__ == "__main__":
    main()
