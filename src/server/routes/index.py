#!/usr/bin/env python3
"""
Defines root blueprint for all flask routes
"""
import logging
from flask import Blueprint, jsonify, json
from werkzeug.exceptions import HTTPException

from .scraper import scraper

index = Blueprint('index', __name__, url_prefix='/')

index.register_blueprint(scraper)

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

@index.app_errorhandler(HTTPException)
def handle_exception(err: HTTPException):
    """
    Return JSON instead of HTML for HTTP errors.
    """
    logging.exception(err.name, exc_info=err)

    # start with the correct headers and status code from the error
    response = err.get_response()
    # replace the body with JSON
    response.content_type = 'application/json'
    response.data = json.dumps({
        'status': err.code,
        'error': err.name,
        'result': None
    })

    return response
