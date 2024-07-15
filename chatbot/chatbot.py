import os
import random
import json
import pickle
import nltk
import tensorflow as tf
import numpy as np
from nltk.stem import WordNetLemmatizer
import logging

from sentiment_analysis import analyze_sentiment
from spell_corrector import spell_check

tf.keras.utils.disable_interactive_logging()

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

class Chatbot:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        self.INTENTS_FILE = 'personalization_files/intents.json'
        self.WORDS_FILE = './training_generated_files/allPatternsWords.pkl'
        self.CLASSES_FILE = './training_generated_files/allIntentsTags.pkl'
        self.MODEL_FILE = './training_generated_files/chatbot_model.keras'
        self.MESSAGES_FILE = 'personalization_files/messages.json'
        self.ERROR_THRESHOLD = 0.65
        self.lemmatizer = WordNetLemmatizer()
        self.words = None
        self.classes = None
        self.model = None
        self.intents_data = None
        self.messages = None
        self.load_data()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def load_data(self):
        with open(self.INTENTS_FILE, 'r', encoding='utf-8') as file:
            self.intents_data = json.load(file)
        with open(self.WORDS_FILE, 'rb') as file:
            self.words = pickle.load(file)
        with open(self.CLASSES_FILE, 'rb') as file:
            self.classes = pickle.load(file)
        self.model = tf.keras.models.load_model(self.MODEL_FILE)
        with open(self.MESSAGES_FILE, 'r', encoding='utf-8') as file:
            messages_data = json.load(file)
            self.messages = messages_data.get("messages", {})

    def tokenize_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        return [self.lemmatizer.lemmatize(word) for word in sentence_words]

    def bag_of_words(self, sentence):
        sentence_words = self.tokenize_sentence(sentence)
        bag = [0] * len(self.words)
        for i, word in enumerate(self.words):
            if word in sentence_words:
                bag[i] = 1
        return bag

    def predict_top_intent(self, sentence):
        bow = self.bag_of_words(sentence)
        bow = np.array(bow)  # Convert list to numpy array
        res = self.model.predict(np.array([bow]))[0]  # Ensure input is in correct format
        results = [[i, r] for i, r in enumerate(res)]
        results.sort(key=lambda x: x[1], reverse=True)
        if results[0][1] > self.ERROR_THRESHOLD:
            return self.classes[results[0][0]]
        else:
            return "no_match"

    def get_response_by_intent(self, sentence_intent):
        if sentence_intent == "no_match":
            return self.messages.get('no_match', "Default no-match message not found in JSON file")
        responses = [intent['responses'] for intent in self.intents_data['intents'] if intent['tag'] == sentence_intent]
        flat_responses = [response for sublist in responses for response in sublist]
        return random.choice(flat_responses)

    def get_welcome_message(self):
        return self.messages.get('welcome', "Default welcome message not found in JSON file")

    def get_negative_intent_response(self):
        return self.messages.get('negative_intent', "Default negative message response not found in JSON file")

    def send_message(self, message):
        try:
            self.logger.debug(f"Received message: {message}")
            sentence_top_intent = self.predict_top_intent(message)
            self.logger.debug(f"Predicted intent: {sentence_top_intent}")
            response = self.get_response_by_intent(sentence_top_intent)
            self.logger.debug(f"Generated response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error in send_message: {e}")
            return "Sorry, I encountered an error processing your message."

# Usage

if __name__ == "__main__":
    bot = Chatbot()
    print(bot.get_welcome_message())
    while True:
        message = input("You: ")
        message = spell_check(message)
        sentiment = analyze_sentiment(message)
        if sentiment == 'Negative':
            response = bot.get_negative_intent_response()
        else:
            response = bot.send_message(message)
        print("Bot:", response)
        if bot.predict_top_intent(message) == 'goodbye':
            break
