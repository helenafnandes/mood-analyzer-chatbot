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
        self.MESSAGES_FILE = 'messages.json'
        self.ERROR_THRESHOLD = 0.50
        self.lemmatizer = WordNetLemmatizer()
        self.words = None
        self.classes = None
        self.model = None
        self.intents_data = None
        self.messages = None
        self.load_data()

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
        return np.array(bag)

    def predict_top_intent(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        results = [[i, r] for i, r in enumerate(res)]
        results.sort(key=lambda x: x[1], reverse=True)
        if results[0][1] > self.ERROR_THRESHOLD:
            return self.classes[results[0][0]]
        else:
            return "no_match"

    def get_response_by_intent(self, sentence_intent):
        if sentence_intent == "no_match":
            return self.messages.get('no_match', "Sorry, I didn't understand what you said. Could you please rephrase or ask something else?")
        responses = [intent['responses'] for intent in self.intents_data['intents'] if intent['tag'] == sentence_intent]
        flat_responses = [response for sublist in responses for response in sublist]
        return random.choice(flat_responses)

    def get_welcome_message(self):
        return self.messages.get('welcome', "Welcome to our bakery chatbot! 🍰🍩 I'm here to assist you with any questions you have about our delicious treats and services. Feel free to ask me anything, from information about our products to placing an order. Let's get started! How can I assist you today?")

    def get_negative_intent_response(self):
        return self.messages.get('negative_intent', "Your satisfaction is our priority. I'll make sure to escalate your concern to one of our attendants, who will assist you promptly. Please hang tight; we'll have someone with you shortly.")

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

# Usage
if __name__ == "__main__":
    bot = Chatbot()
    print(bot.get_welcome_message())
    while True:
        message = input("You: ")
        response = bot.send_message(message)
        print("Bot:", response)
