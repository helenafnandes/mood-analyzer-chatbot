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

# 2) saving training data into binary files

pickle.dump(all_patterns_words, open('allPatternsWords.pkl', 'wb'))
pickle.dump(all_intents_tags, open('allIntentsTags.pkl', 'wb'))


# 3) pre-processing training data

training_data = []
empty_output_vector = [0] * len(all_intents_tags)

for pair in data_pattern_tag_pairs:
    pattern_words_bag = []
    data_pattern_words = pair[0]
    data_pattern_words = [lemmatizer.lemmatize(word.lower()) for word in data_pattern_words]
    for word in all_patterns_words:
        pattern_words_bag.append(1) if word in data_pattern_words else pattern_words_bag.append(0)

    pattern_output_row = list(empty_output_vector)
    pattern_output_row[all_intents_tags.index(pair[1])] = 1
    training_data.append(pattern_words_bag + pattern_output_row)

random.shuffle(training_data)
training_data = np.array(training_data)

trainX = training_data[:, :len(all_patterns_words)]
trainY = training_data[:, len(all_patterns_words):]

# build neural network model

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')
