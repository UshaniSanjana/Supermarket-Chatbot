import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Goods location mapping
GOODS_LOCATION = {
    "fruits": 1,
    "vegetables": 2,
    "detergent": 3,
    "eggs": 4,
    "flour": 5,
    "meat": 6,
    "beverages": 7,
    "bakery": 8,
    "snacks": 9,
    "skincare": 10
}

def process_input(input_text):
    tokens = word_tokenize(input_text)
    tagged = pos_tag(tokens)
    return tagged

def respond_to_greeting(input_text):
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(word in input_text.lower() for word in greetings):
        return "Hello! How can I assist you today?"
    else:
        return None

def get_goods_location(goods_list):
    locations = {}
    for good in goods_list:
        # Convert input to lowercase for case insensitivity
        normalized_good = good.lower()
        if normalized_good in GOODS_LOCATION:
            locations[good] = GOODS_LOCATION[normalized_good]
        else:
            locations[good] = "Not found"
    return locations
