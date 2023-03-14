# dummy flask app
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from profanity_check import predict, predict_prob
import asr_module as asr


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


def speech_to_text(wav_file):
    decoder = asr.Decoder(lang='en')
    ans = decoder.decode_wav(wav_file)
    return ans["nbest"][0]["sentence"]

@app.route('/audio/<string:url>', methods=['POST'])
def audioObscenity(url):
    # check if url is valid
    if not url.startswith('https://') or not url.endswith('.wav') or not url.startswith('http://'):
        return jsonify({'error': 'invalid url'})
    
    # download audio file and save it to a temporary file
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(requests.get(url).content)
    text_from_audio = speech_to_text(tmp.name)
    pred = predict([text_from_audio])
    probability = predict_prob([text_from_audio])
    tmp.close()
    return jsonify({'prediction': str(pred[0]), 'probability': str(probability[0])})   

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