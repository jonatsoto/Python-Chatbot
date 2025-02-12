import spacy
from fuzzywuzzy import fuzz
import random
import re
from nltk.chat.util import Chat, reflections

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Extended list of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!", "Hi! How can I help you today?",]
    ],
    [
        r"what is your name?",
        ["I am a chatbot created by Python. You can call me ChatBot.",]
    ],
    [
        r"how are you?",
        ["I'm doing great, how about you?", "I'm good! How are you?",]
    ],
    [
        r"sorry (.*)",
        ["No problem at all!", "No worries!", "It's alright!",]
    ],
    [
        r"I am (.*) good",
        ["Nice to hear that!", "That's great!", "Awesome!",]
    ],
    [
        r"thank you|thanks",
        ["You're welcome!", "No problem!", "Glad to help!"]
    ],
    [
        r"what can you do?",
        ["I can chat with you, provide information, and help with various tasks. Try asking me something!", "I can help you with information, tasks, and have a friendly chat!",]
    ],
    [
        r"how old are you?",
        ["I'm as old as the code I'm running on!", "Age is just a number when you're a chatbot!",]
    ],
    [
        r"who created you?",
        ["I was created by a team of developers who love Python.", "A group of talented developers!",]
    ],
    [
        r"where are you from?",
        ["I'm from the world of code and algorithms.", "I live in the digital realm!",]
    ],
    [
        r"what is your favorite (.*)?",
        ["I don't have personal preferences, but I can tell you a lot about %1!",]
    ],
    [
        r"do you know (.*)?",
        ["I'm familiar with many things, including %1.", "Yes, I know about %1!",]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day!", "See you later!", "Bye for now!"]
    ],
]

# Default reflections
my_reflections = {
    "go": "gone",
    "hello": "hi",
    "i am": "you are",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you": "me",
    "me": "you"
}

# Custom function to handle fuzzy matching
def fuzzy_match(user_input, patterns):
    max_ratio = 0
    best_pair = None
    for pattern, responses in patterns:
        pattern_str = pattern.pattern  # Convert the regex pattern to a string
        ratio = fuzz.ratio(user_input.lower(), pattern_str.lower())
        if ratio > max_ratio:
            max_ratio = ratio
            best_pair = (pattern, responses)
    return best_pair if max_ratio >= 50 else None

# Custom function to handle wildcards in responses
def replace_wildcards(response, user_input):
    wildcards = {
        r"%1": r"(.+)",
    }
    for wildcard, pattern in wildcards.items():
        user_input_parts = re.findall(pattern, user_input)
        if user_input_parts:
            response = response.replace(wildcard, user_input_parts[0])
    return response

# Overriding the respond method to include fuzzy matching and exact match fallback
class FuzzyChat(Chat):
    def respond(self, str):
        doc = nlp(str)  # Process user input with spaCy
        cleaned_input = " ".join([token.lemma_ for token in doc])  # Lemmatize the input

        # Check for exact matches for common greetings
        exact_matches = {
            "hi": "Hello!",
            "hey": "Hey there!",
            "hello": "Hi! How can I help you today?"
        }
        if cleaned_input in exact_matches:
            return exact_matches[cleaned_input]

        pair = fuzzy_match(cleaned_input, self._pairs)
        if pair:
            pattern, responses = pair
            response = replace_wildcards(random.choice(responses), str)
            return response
        else:
            return "Sorry, I didn't understand that. Could you please rephrase?"

# Create chatbot
def chatbot():
    print("Hi, I'm the ChatBot you created. Type 'quit' to exit.")
    chat = FuzzyChat(pairs, reflections)
    chat.converse()

# Run chatbot
if __name__ == "__main__":
    chatbot()
