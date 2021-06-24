#!/usr/bin/env python3
"""
Defines routes for `/scraper` subdirectory
"""
from flask import Blueprint, jsonify
from .script import SCRIPTS

scraper = Blueprint('scraper', __name__, url_prefix='/scraper')

@scraper.route('/status', methods=['GET'])
def status():
    """
    TODO
    """
    return jsonify({
        'status': 0,
        'error': None,
        'result': {
            'scrips': SCRIPTS,
        }
    })
