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
        # Add more conversational word suggestions as needed
    }

    # Check if the word exists in the conversational_words dictionary
    if word in conversational_words:
        return conversational_words[word]
    else:
        return word

def spell_check(text):
    text = suggest_conversational(text)
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get a list of words with spelling corrections
    corrected = blob.correct()

    return str(corrected)

'''
if __name__ == "__main__":
    input_text = input("Enter text to spell check: ")
    corrected_text = spell_check(input_text)
    print("Corrected text:")
    print(corrected_text)
'''
