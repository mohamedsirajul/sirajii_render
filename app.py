from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import random
import json
import pickle
import numpy as np
# import wikipedia
import nltk
import cv2
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
import atexit 
from tkinter import *



app = Flask(__name__)
CORS(app)

lemmatizer = WordNetLemmatizer()

# Load the chatbot model and intents data
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
chatbot_model = keras.models.load_model('chatbotmodel.h5')


def clean_up():
    cv2.destroyAllWindows()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = chatbot_model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['message']
    ints = predict_class(user_input)
    res = get_response(ints, intents)

    return jsonify({'response': res})



# Run the Flask app
if __name__ == '__main__':
    atexit.register(clean_up)  # Register cleanup function
    app.run(port=5000)
