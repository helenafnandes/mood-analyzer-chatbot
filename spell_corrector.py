from textblob import TextBlob

def suggest_conversational(word):
    # Define conversational word suggestions
    conversational_words = {
        "helo": "hello",
        "gret": "great",
        "thanx": "thanks",
        "u": "you",
        "ur": "your",
        "plz": "please",
        "luv": "love",
        "cuz": "because",
        "gonna": "going to",
        "wanna": "want to",
        "lemme": "let me",
        "gimme": "give me",
        "nite": "night",
        "wnt": "want",
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