#!/usr/bin/env python3
"""
Defines root blueprint for all flask routes
"""
import os
from flask import Blueprint, jsonify, send_from_directory
from werkzeug.utils import send_file
from .scraper.routes import scraper

STATIC_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../../client/static'
    )
)

index = Blueprint('index', __name__, url_prefix='/')

index.register_blueprint(scraper)

@index.route('/', methods=['GET'])
def get_index():
    return send_file(os.path.join(STATIC_DIR, 'index.htm'))

@index.route('/status', methods=['GET'])
def get_status():
    """Displays the status of api.

    Returns:
        string: JSON data
    """
    return jsonify({
        "status": 0,
        "error": None,
        "result": {},
    })
