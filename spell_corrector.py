from textblob import TextBlob

def suggest_conversational(word):
    # Define conversational word suggestions
    conversational_words = {
        "helo": "hello",
        "hi": "hello",
        "hey": "hello",
        "howdy": "hello",
        "gret": "great",
        "good": "great",
        "thanx": "thanks",
        "thx": "thanks",
        "thank": "thanks",
        "u": "you",
        "ur": "your",
        "yours": "your",
        "plz": "please",
        "pls": "please",
        "luv": "love",
        "cuz": "because",
        "cos": "because",
        "coz": "because",
        "gonna": "going to",
        "wanna": "want to",
        "lemme": "let me",
        "gimme": "give me",
        "nite": "night",
        "wnt": "want",
        "what": "what",
        "wat": "what",
        "bot": "bot",
        "bots": "bots",
        "what's": "what's",
        "whats": "what's",
        "that's": "that's",
        "thats": "that's",
        "there's": "there's",
        "theres": "there's",
        "cud": "could",
        "could": "could",
        "What's": "What's"
        # Add more conversational word suggestions as needed
    }

    # Check if the word exists in the conversational_words dictionary
    if word in conversational_words:
        return conversational_words[word]
    else:
        return word

def spell_check(text):
    # Split the text into individual words
    words = text.split()

    corrected_words = []
    for word in words:
        # Apply conversational word correction
        corrected_word = suggest_conversational(word)
        corrected_words.append(corrected_word)

    # Join the corrected words back into a sentence
    corrected_text = ' '.join(corrected_words)

    # Perform general spell check using TextBlob
    blob = TextBlob(corrected_text)
    corrected = blob.correct()

    return str(corrected)

'''
if __name__ == "__main__":
    input_text = input("Enter text to spell check: ")
    corrected_text = spell_check(input_text)
    print("Corrected text:")
    print(corrected_text)
'''