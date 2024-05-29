import os
import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer

from sentiment_analysis import analyze_sentiment
from spell_corrector import spell_check

tf.keras.utils.disable_interactive_logging()


class Chatbot:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        self.INTENTS_FILE = 'intents.json'
        self.WORDS_FILE = 'allPatternsWords.pkl'
        self.CLASSES_FILE = 'allIntentsTags.pkl'
        self.MODEL_FILE = 'chatbot_model.keras'
        self.MESSAGES_FILE = 'messages.json'
        self.ERROR_THRESHOLD = 0.60
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
            print(results[0][1], self.classes[results[0][0]], results[1][1], self.classes[results[1][0]], results[2][1], self.classes[results[2][0]])
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
        message = spell_check(message)
        sentiment = analyze_sentiment(message)
        if(sentiment == 'Negative'):
            response = bot.get_negative_intent_response()
        else:
            response = bot.send_message(message)
        print("Bot:", response)
        if(bot.predict_top_intent(message) == 'goodbye'):
            break
