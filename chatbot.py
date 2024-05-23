# chatbot.py
import os
import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer

tf.keras.utils.disable_interactive_logging()

class Chatbot:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        self.INTENTS_FILE = 'intents.json'
        self.WORDS_FILE = 'allPatternsWords.pkl'
        self.CLASSES_FILE = 'allIntentsTags.pkl'
        self.MODEL_FILE = 'chatbot_model.keras'
        self.ERROR_THRESHOLD = 0.25
        self.lemmatizer = WordNetLemmatizer()
        self.words = None
        self.classes = None
        self.model = None
        self.intents_data = None
        self.load_data()

    def load_data(self):
        with open(self.INTENTS_FILE, 'r') as file:
            self.intents_data = json.load(file)
        with open(self.WORDS_FILE, 'rb') as file:
            self.words = pickle.load(file)
        with open(self.CLASSES_FILE, 'rb') as file:
            self.classes = pickle.load(file)
        self.model = tf.keras.models.load_model(self.MODEL_FILE)

    def tokenize_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        return [self.lemmatizer.lemmatize(word) for word in sentence_words]

    def bag_of_words(self, sentence):
        sentence_words = self.tokenize_sentence(sentence)
        bag = [0] * len(self.words)
        for i, word in enumerate(self.words):
            if word in sentence_words:
                bag[i] = 1
        return np.array(bag)

    def predict_top_intent(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        results = [[i, r] for i, r in enumerate(res) if r > self.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        sentence_intents = [{'intent': self.classes[r[0]], 'probability': str(r[1])} for r in results]
        return sentence_intents[0]['intent']

    def get_response_by_intent(self, sentence_intent):
        responses = [intent['responses'] for intent in self.intents_data['intents'] if intent['tag'] == sentence_intent]
        flat_responses = [response for sublist in responses for response in sublist]
        return random.choice(flat_responses)

    def get_welcome_message(self):
        return "Welcome to our bakery chatbot! 🍰🍩 I'm here to assist you with any questions you have about our delicious treats and services. Feel free to ask me anything, from information about our products to placing an order. Let's get started! How can I assist you today?"

    '''
    def send_message(self, message):
        corrected_message = spell_check(message)
        sentence_top_intent = self.predict_top_intent(corrected_message)
        response = self.get_response_by_intent(sentence_top_intent)
        sentiment = analyze_sentiment(corrected_message)
        return [corrected_message, response, sentiment]
    '''

    def send_message(self, message):
        sentence_top_intent = self.predict_top_intent(message)
        return self.get_response_by_intent(sentence_top_intent)
