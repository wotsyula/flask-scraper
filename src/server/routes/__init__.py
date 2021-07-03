#!/usr/bin/env python3
"""
Defines root blueprint for all flask routes
"""
from flask import Blueprint, jsonify, current_app
from .scraper.routes import scraper

index = Blueprint('index', __name__, url_prefix='/')

index.register_blueprint(scraper)

@index.route('/', methods=['GET'])
def get_index():
    """
    Home page

    Returns:
        str: HTML
    """
    return current_app.send_static_file('index.htm')


@index.route('/status', methods=['GET'])
def get_status():
    """Displays the status of api.

    Returns:
        string: JSON data
    """
    return jsonify({
        "status": 0,
        "error": None,
        "result": True,
    })
