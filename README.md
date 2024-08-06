# Mood Analyzer Chatbot

This project implements a chatbot tailored for a bakery, capable of engaging in conversation with users to provide information about the bakery's products and services, as well as assist with placing orders. The chatbot utilizes several natural language processing (NLP) techniques including spell checking and sentiment analysis to enhance user experience and interaction quality.

The chatbot is powered by a neural network built with TensorFlow, trained using a JSON file containing specific intents. These intents represent different conversation patterns and associated responses. The neural network has been trained to classify these intents, enabling the chatbot to understand and appropriately respond to user messages.

## Live Demonstration

You can experience the chatbot through a live web application by following this [link](https://chatbot-webapp-one.vercel.app/).
The source code for the web app can be found [here](https://github.com/helenafnandes/chatbot-webapp)

## Functionalities

1. ✅**Spell Checking**: The chatbot corrects spelling errors in user input to improve understanding and ensure accurate responses.

2. ✅**Sentiment Analysis**: Integrated sentiment analysis allows the chatbot to gauge the sentiment of user inputs. In case of negative sentiment, appropriate actions are taken to address the user's concern and escalate it to the bakery staff if needed.

3. ✅**Web-Based Interface for Tests**: A [user-friendly web interface](https://chatbot-webapp-one.vercel.app/) enabling easy viewing and testing of the chatbot.

4. 🔳**Enhanced Spell Checking**: Implement spell checking functionality that leverages keyboard configuration for improved accuracy and efficiency.

## Local Installation

To run the chatbot on your own machine, follow these steps:

1. **Clone the Repository**:

```
git clone https://github.com/helenafnandes/mood-analyzer-chatter-bot.git
cd mood-analyzer-chatter-bot
```

2. **Set Up the Environment**:

Ensure you have Python 3.11 installed. Install the necessary dependencies using the requirements.txt file:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. **Optional: Personalizing and Training the Chatbot**:

- This step is optional. The bot can be run without personalization, and it will function with its pre-trained responses related to a bakery.
- Personalization: To tailor the chatbot to a specific context, modify the contents of the intents.json and messages.json files located in the personalization_files directory.
- Training: After personalization, execute the training.py script to train the neural network with the updated data.

```
python training.py
```

4. **Running the Chatbot Locally**:

Launch the chatbot by running the chatbot.py script:

```
python chatbot.py
```

5. **Running the Chatbot via Flask API**:

   - Launch the Flask API by running the `app.py` script.
   - The API provides the following endpoints:
     | Method | Route | Description |
     |--------|------------------------------|------------------------------------------------------------|
     | POST | /api/chatbot | Sends a message to the chatbot and receives a response. The JSON response includes the user's message corrected after spell check, the detected sentiment from the sentiment analysis, and the chatbot's reply. |
     | GET | /api/welcome_message | Retrieves the chatbot's welcome message. |
     | GET | /api/negative_intent_response| Retrieves the chatbot's response to negative intents. |

6. **Interacting with the Chatbot**:

   - With the original intents.json and messages.json files, users can type messages or questions related to the bakery's products, services, or any other inquiries.
   - The chatbot responds accordingly, providing relevant information or assistance.

7. **Ending the Chat**:
   - To conclude the conversation, simply type "goodbye" or any other exit keyword as defined in the intents.
     - If there is a "goodbye" intent on the intents.json file, the bot detects it and stops the application.

## Use Example

The bot will analyze the intents of the user's message and respond accordingly. Intent recognition and response generation are implemented using NLTK and TensorFlow.

Example:

```
Welcome to our bakery chatbot! 🍰🍩 I'm here to assist you with any questions you have about our delicious treats and services. Feel free to ask me anything, from information about our products to placing an order. Let's get started! How can I assist you today?
You: hello! what are your cake options?
Bot: Our cake selection includes flavors like chocolate, vanilla, red velvet, carrot, and lemon drizzle. Feel free to ask for more details or suggestions!
You: awesome, thanks
Bot: No problem at all! We're here to help if you have any other questions or need suggestions.
```

### Spell Checking

The spell checking functionality is implemented in the `spell_corrector.py` module using TextBlob. It corrects spelling errors in user input, ensuring better comprehension by the chatbot.

Example:

```python
from chatbot.chatbot import spell_check

input_text = "I wnt to oreder a cak"
corrected_text = spell_check(input_text)
print("Corrected text:")
print(corrected_text)  # "i want to order a can"
```

### Sentiment Analysis

Sentiment analysis is performed using spaCy and VADER (Valence Aware Dictionary and sEntiment Reasoner). It allows the chatbot to detect the sentiment of user inputs and take appropriate actions, such as addressing negative sentiment.

Example:

```python
from chatbot.chatbot import analyze_sentiment

text = "I'm very satisfied with your service."
sentiment = analyze_sentiment(text)
print("Sentiment:", sentiment)  # "Sentiment: Positive
```

## Personalizing the Bot

- The chatbot's behavior and responses can be personalized to suit different contexts or businesses. This customization primarily depends on the contents of the `intents.json` and `messages.json` files on the `personalization_files` folder. By modifying or adding intents and their corresponding patterns and messages in those files, the chatbot can be adapted to their specific requirements and industry domain.
- You may also modify the chatbot's actions depending on the intent or the sentiment of the user's sentence. For example, if the user wants to make an order, the bot can start an order making process instead of just showing a message.

## Contributions and Suggestions

Feel free to explore the repository and share your thoughts! Suggestions for improvements or additional features are much appreciated.
