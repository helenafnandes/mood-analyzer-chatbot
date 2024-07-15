import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot import Chatbot
from sentiment_analysis import analyze_sentiment
from spell_corrector import spell_check
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()


@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json(force=True)
    if 'message' not in data or not isinstance(data['message'], str):
        logging.error('Invalid request format')
        return jsonify({'error': 'Invalid request format'}), 400

    message = data['message'].lower()
    logging.debug(f'Received message: {message}')
    corrected_message = spell_check(message)
    logging.debug(f'Corrected message: {corrected_message}')
    sentiment = analyze_sentiment(corrected_message)
    logging.debug(f'Sentiment: {sentiment}')

    if sentiment == 'Negative':
        response = chatbot.get_negative_intent_response()
    else:
        response = chatbot.send_message(corrected_message)
    logging.debug(f'Response: {response}')

    return jsonify({
        'corrected_message': corrected_message,
        'sentiment': sentiment,
        'response': response
    })


@app.route('/api/welcome_message', methods=['GET'])
def welcome_message():
    return jsonify({"message": chatbot.get_welcome_message()})


@app.route('/api/negative_intent_response', methods=['GET'])
def negative_intent_message():
    return jsonify({"message": chatbot.get_negative_intent_response()})



if __name__ == '__main__':
    app.run()