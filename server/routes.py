from flask import Flask, render_template

from server.app import app

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)
