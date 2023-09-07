from flask import Flask, render_template, request, jsonify
from chat import get_response
import pyttsx3
import threading

app = Flask(__name__)

def speak_response(response):
    # Initialize the Pyttsx3 engine
    engine = pyttsx3.init()

    # Change to Female Voice
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)

    #Send Voice Output
    engine.say(response)
    engine.runAndWait()
    engine.stop()

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)

    # Use a thread to speak the response
    audio_thread = threading.Thread(target=speak_response, args=(response,))
    audio_thread.start()

    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run()
