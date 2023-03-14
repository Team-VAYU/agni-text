# dummy flask app
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from profanity_check import predict, predict_prob


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/text/<string:input_string>')
def api(input_string):
    # limit number of words to 80
    if len(input_string.split()) > 80:
        return jsonify({'error': 'too many words'})

    prediction = predict([input_string])
    probability = predict_prob([input_string])
    return jsonify({'prediction': str(prediction[0]), 'probability': str(probability[0])})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)