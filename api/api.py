import flask
import numpy as np
from flask import request, jsonify
from model_load import generate_text


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/generator', methods=['GET'])
def make_text():
    if 'text' in request.args:
        results = []
        text = str(request.args['text'])
        seed = np.random.randint(1,100)
        length = 400
        answer = generate_text(seed, length, text)[0]
        results.append(answer)
    return jsonify(results)

app.run(host='0.0.0.0', port='80')