
from flask import Flask, request, jsonify, render_template
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import speech_recognition as sr
import pyttsx3

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open("words.pkl", 'rb'))
classes = pickle.load(open("classes.pkl", 'rb'))
model = load_model('chatbot_model.h5')

app = Flask(__name__)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if w == word:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
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
        if i['tags'] == tag:
            result = random.choice(i['Responses'])
            break
    return result

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    message = request.json.get('message')
    ints = predict_class(message)
    if ints:
        res = get_response(ints, intents)
        speak(res)  # Output the response via text-to-speech
        return jsonify({"response": res})
    else:
        error_message = "I don't understand, please try again."
        speak(error_message)  # Output the error message via text-to-speech
        return jsonify({"response": error_message})

@app.route('/voice', methods=['POST'])
def voice_chat():
    # Recognize speech from the microphone
    voice_input = recognize_speech()
    if voice_input:
        # Process the recognized speech with the chatbot
        ints = predict_class(voice_input)
        if ints:
            res = get_response(ints, intents)
            speak(res)  # Output the response via text-to-speech
            return jsonify({"response": res})
        else:
            error_message = "I don't understand, please try again."
            speak(error_message)  # Output the error message via text-to-speech
            return jsonify({"response": error_message})
    else:
        error_message = "Sorry, I didn't catch that."
        speak(error_message)  # Output the error message via text-to-speech
        return jsonify({"response": error_message})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
