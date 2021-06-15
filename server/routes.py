#!/usr/bin/env python3

from flask import Flask, render_template

from app import app

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

