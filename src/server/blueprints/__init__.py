#!/usr/bin/env python3
"""
Defines root blueprint for all flask routes
"""
from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

from .scraper import *

@bp.route('/', methods=['GET'])
def get_index():
    """Displays empty JSON response.

    Returns:
        string: JSON data
    """
    return jsonify({
        "status": 0,
        "error": None,
        "result": {},
    })

@bp.route('/status', methods=['GET'])
def get_status():
    """Displays the status of api.

    Returns:
        string: JSON data
    """
    return get_index()
