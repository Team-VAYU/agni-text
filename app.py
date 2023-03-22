# dummy flask app
import os
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from profanity_check import predict, predict_prob
from audio import stt
import tempfile
import audiofile as af
import random
import whisper
import numpy as np


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/audio/', methods=['POST'])
def audioObscenity():
    import time
    start = time.time()
    req = request.get_json()
    audio = req['url']
    if audio is None:
        return jsonify({'error': 'no audio url'})
    with tempfile.NamedTemporaryFile(suffix='.wav') as tmp:
        os.system(f"wget {audio} -O {tmp.name}")
        audio_data, sample_rate = af.read(tmp.name)
        model = whisper.load_model("tiny")
        text = model.transcribe(audio_data)
        text = text["text"]
        print(text)
        print(time.time() - start)
        prediction = predict([text])
        probability = predict_prob([text])
        return jsonify({'prediction': str(prediction[0]), 'probability': str(probability[0])})

@app.route('/text/', methods=['POST'])
def textObscenity():
    # limit number of words to 80
    # get input string from body of request
    req = request.get_json()
    input_string = req['text']
    if len(input_string.split()) > 80:
        return jsonify({'error': 'too many words'})

    prediction = predict([input_string])
    probability = predict_prob([input_string])
    return jsonify({'prediction': str(prediction[0]), 'probability': str(probability[0])})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)