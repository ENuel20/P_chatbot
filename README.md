# AI Chatbot with Flask and TensorFlow

This repository contains a chatbot powered by TensorFlow, Flask, and natural language processing (NLP). The chatbot is trained on predefined intents and is capable of interacting through both text and voice commands.

## Features
- **Text-based Chat**: Interact with the chatbot via a simple web interface.
- **Voice-based Chat**: Enable voice commands using the browser's microphone input.
- **Customizable Intents**: Modify `intents.json` to add or adjust the chatbot's responses.
- **Model Training**: Train the chatbot using `training.py` on the dataset of intents.
- **Web-based UI**: Simple HTML frontend to facilitate user interaction with the chatbot.

## File Structure

```bash
├── app.py              # Flask backend
├── chatbot.py          # Chatbot script for command-line interaction
├── training.py         # Script to train the model
├── intents.json        # Dataset of intents, patterns, and responses
├── words.pkl           # Pickle file of words generated during training
├── classes.pkl         # Pickle file of classes generated during training
├── chatbot_model.h5    # Pretrained model file
├── templates
│   └── index.html      # Frontend for web-based interaction
└── README.md           # Project documentation

Prerequisites
Python 3.x
Flask
TensorFlow
NLTK
SpeechRecognition
Pyttsx3 (for text-to-speech, if needed)
Optional: Set Up a Virtual Environment
It's recommended to use a virtual environment to isolate the dependencies required for this project. Follow these steps to create and activate a virtual environment:

Create a Virtual Environment:

python3 -m venv chatbot_env
Activate the Virtual Environment:

On Windows:

chatbot_env\Scripts\activate

On macOS/Linux:

source chatbot_env/bin/activate

Install Dependencies: After activating the virtual environment, install the necessary Python packages:


pip install Flask tensorflow nltk SpeechRecognition pyttsx3
Deactivate the Virtual Environment: Once you're done working, you can deactivate the virtual environment with:

deactivate

Setup Instructions
Clone the Repository:

git clone https://github.com/your-username/chatbot.git
cd chatbot
(Optional) Create and Activate the Virtual Environment: See the "Optional: Set Up a Virtual Environment" section above.

Install Dependencies: Install the necessary Python packages using pip:

pip install Flask tensorflow nltk SpeechRecognition pyttsx3
Train the Chatbot: Train the chatbot on your intents:

python training.py
Run the Flask App: Start the Flask server:

python app.py
Access the Chatbot: Open your browser and go to http://127.0.0.1:5000/.

Voice Commands
To interact with the chatbot using voice commands, press the microphone button on the web interface.

Customization
Modify intents.json to add new patterns and responses for the chatbot.
Retrain the model using training.py after making changes to intents.json.
