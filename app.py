import os
from flask import Flask, render_template
import json
from random import random

with open("static/model.json") as json_file:
    model = json.load(json_file)

app = Flask(__name__)

def generate_letter(lm, history, order):
        history = history[-order:]
        dist = lm[history]
        x = random()
        for c,v in dist:
            x = x - v
            if x <= 0: return c

def generate_utterance(lm, order):
    history = "~" * order
    out = []
    c = None
    
    while c != "\n":
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)

    return "".join(out)[:-1]

@app.route('/')
def index():
    return render_template("main.html")

@app.route("/wisdom")
def wisdom():
    return "<p>" + generate_utterance(model, 11) + "</p>"

if __name__ == '__main__':
     # app.run(debug=True, port=5555)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)