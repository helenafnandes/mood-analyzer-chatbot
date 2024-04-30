import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
# from tensorflow.keras.models import load_model
import tensorflow as tf

lemmatizer = WordNetLemmatizer
intents = json.load(open('intents.json'))

words = pickle.load(open('allPatternsWords.pkl', 'rb'))
classes = pickle.load(open('allIntentsTags.pkl', 'rb'))
model = tf.keras.models.load_model('chatbot_model.keras')
