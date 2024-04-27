import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from nltk.stem import WordNetLemmatizer

# 1) loading and formatting data from intents.json for training

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

all_patterns_words = []
all_intents_tags = []
data_pattern_tag_pairs = []
ignoreLetters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        pattern_words = nltk.word_tokenize(pattern)
        all_patterns_words.extend(pattern_words)
        data_pattern_tag_pairs.append((pattern_words, intent['tag']))
        if intent['tag'] not in all_intents_tags:
            all_intents_tags.append(intent['tag'])



all_patterns_words = [lemmatizer.lemmatize(word) for word in all_patterns_words if word not in ignoreLetters]
all_patterns_words = sorted(set(all_patterns_words))  # "set" to eliminate duplicates

all_intents_tags = sorted(set(all_intents_tags))



