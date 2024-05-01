import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

# Constants
INTENTS_FILE = 'intents.json'
WORDS_FILE = 'allPatternsWords.pkl'
CLASSES_FILE = 'allIntentsTags.pkl'
MODEL_FILE = 'chatbot_model.keras'
ERROR_THRESHOLD = 0.25

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
def predict_class(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

# Get response
def get_response(sentence, intents_data):
    sentence_intents = predict_class(sentence, model)
    top_intent_tag = sentence_intents[0]['intent']
    responses = [intent['responses'] for intent in intents_data['intents'] if intent['tag'] == top_intent_tag]
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


    # Get and print response
    sentence = input("Enter your message: ")
    response = get_response(sentence, intents_data)
    print(response)

if __name__ == "__main__":
    main()
