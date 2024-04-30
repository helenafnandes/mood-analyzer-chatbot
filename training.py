import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer


# Constants
INTENTS_FILE = 'intents.json'
ALL_PATTERNS_WORDS_FILE = 'allPatternsWords.pkl'
ALL_INTENTS_TAGS_FILE = 'allIntentsTags.pkl'
MODEL_FILE = 'chatbot_model.keras'
#MODEL_FILE = 'chatbot_model.h5'


# Function to load intents data
def load_intents(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Function to preprocess patterns
def preprocess_patterns(patterns, lemmatizer, ignore_letters):
    pattern_words = []
    data_pattern_tag_pairs = []

    for intent in patterns['intents']:
        for pattern in intent['patterns']:
            pattern_words.extend(nltk.word_tokenize(pattern))
            data_pattern_tag_pairs.append((nltk.word_tokenize(pattern), intent['tag']))

    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words if word not in ignore_letters]
    pattern_words = sorted(set(pattern_words))

    all_intents_tags = sorted(set(pair[1] for pair in data_pattern_tag_pairs))

    return pattern_words, data_pattern_tag_pairs, all_intents_tags


# Function to save data to binary files
def save_to_pickle(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


# Function to build neural network model
def build_model(input_shape, output_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, input_shape=input_shape, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(output_shape, activation='softmax')
    ])
    sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model


# Load intents data
intents_data = load_intents(INTENTS_FILE)

# Preprocess patterns
lemmatizer = WordNetLemmatizer()
ignore_letters = ['?', '!', '.', ',']
all_patterns_words, data_pattern_tag_pairs, all_intents_tags = preprocess_patterns(intents_data, lemmatizer,
                                                                                   ignore_letters)

# Save data to binary files
save_to_pickle(all_patterns_words, ALL_PATTERNS_WORDS_FILE)
save_to_pickle(all_intents_tags, ALL_INTENTS_TAGS_FILE)

# Preprocess training data
training_data = []
empty_output_vector = [0] * len(all_intents_tags)

for pair in data_pattern_tag_pairs:
    pattern_words_bag = []
    data_pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pair[0]]
    for word in all_patterns_words:
        pattern_words_bag.append(1) if word in data_pattern_words else pattern_words_bag.append(0)

    pattern_output_row = list(empty_output_vector)
    pattern_output_row[all_intents_tags.index(pair[1])] = 1
    training_data.append(pattern_words_bag + pattern_output_row)

random.shuffle(training_data)
training_data = np.array(training_data)

trainX = training_data[:, :len(all_patterns_words)]
trainY = training_data[:, len(all_patterns_words):]

# Build and train neural network model
model = build_model(input_shape=(len(trainX[0]),), output_shape=len(trainY[0]))
model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)

# Save model
tf.keras.models.save_model(model, MODEL_FILE)
print('Model saved successfully.')
