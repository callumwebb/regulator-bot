import os
from flask import Flask, render_template
import json
from random import random

with open("static/wayne.json") as json_file:
    wayne_model = json.load(json_file)

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

    return "".join(out)

@app.route('/')
def index():
    return render_template("main.html")

@app.route("/wayne")
def wayne():
    return generate_utterance(wayne_model, 10)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True, port=5555)