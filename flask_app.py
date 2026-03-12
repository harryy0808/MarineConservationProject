from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/plastic_game')
def plastic_game():
    return render_template('game.html')

