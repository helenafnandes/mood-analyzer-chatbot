# app.py
from flask import Flask, jsonify, request
from chatbot import Chatbot

from sentiment_analysis import analyze_sentiment
from spell_corrector import spell_check

app = Flask(__name__)
chatbot = Chatbot()


# Manually configure CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response


# Chatbot route
@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.json
    message = data['message'].lower()
    corrected_message = spell_check(message)
    sentiment = analyze_sentiment(corrected_message)
    if sentiment == 'Negative':
        response = chatbot.get_negative_intent_response()
    else:
        response = chatbot.send_message(corrected_message)
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
    app.run(debug=True)
