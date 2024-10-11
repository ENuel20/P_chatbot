import speech_recognition as sr
from flask import Flask, session, request, jsonify

app = Flask(__name__)
app.secret_key = '69a41d5cb465ab826f1c95509fe32b4d193cff574b9b0719'

AUTHORIZED_VOICE_TEXT = "Hey Naval"  # The phrase you use for authentication

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something for authentication:")
        audio = recognizer.listen(source)
        try:
            voice_text = recognizer.recognize_google(audio)
            return voice_text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

@app.route('/start', methods=['POST'])
def start_session():
    voice_text = recognize_voice()
    if voice_text and voice_text.lower() == AUTHORIZED_VOICE_TEXT.lower():
        session['authorized'] = True
        return jsonify({"message": "Voice authenticated, session started!"}), 200
    else:
        return jsonify({"error": "Unauthorized voice."}), 401

@app.route('/respond', methods=['POST'])
def chatbot_response():
    if not session.get('authorized'):
        return jsonify({"error": "Unauthorized. Please start a session first."}), 401

    user_input = request.json.get('message')
    # Your chatbot logic here
    response = get_response(predict_class(user_input), intents)
    return jsonify({"response": response}), 200

if __name__ == "__main__":
    app.run(debug=True)
