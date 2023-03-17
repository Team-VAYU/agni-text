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


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/audio/')
def audioObscenity():
    import time
    start = time.time()
    audio = request.args.get('url')
    if audio is None:
        return jsonify({'error': 'no audio url'})
    with tempfile.NamedTemporaryFile(suffix='.wav') as tmp:
        os.system(f"wget {audio} -O {tmp.name}")
        audio, sample_rate = af.read(tmp.name)
        # save as wav with 16k bitrate and 30 random seconds
        start_index = random.randint(0, len(audio) - 480000)
        af.write(tmp.name, audio[start_index:start_index+480000], sample_rate)
        text = stt.main(tmp.name)
        print(text)
        print(time.time() - start)
        return textObscenity(text)

@app.route('/text/<string:input_string>')
def textObscenity(input_string):
    # limit number of words to 80
    if len(input_string.split()) > 80:
        return jsonify({'error': 'too many words'})

    prediction = predict([input_string])
    probability = predict_prob([input_string])
    return jsonify({'prediction': str(prediction[0]), 'probability': str(probability[0])})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)