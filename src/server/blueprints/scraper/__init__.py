#!/usr/bin/env python3
"""
Defines routes for `/scraper` subdirectory
"""
import re
from os import listdir, path
from flask import jsonify
from .. import bp

SCRAPER_DIR = path.abspath(path.dirname(__file__))
SCRIPTS = []

for directory in listdir(SCRAPER_DIR):
    abs_directory = path.join(SCRAPER_DIR, directory)

    if path.isdir(abs_directory):
        for script in listdir(abs_directory):
            if re.match('^[a-z]+.py$', script) is not None:
                SCRIPTS.append(directory + '/' + script[:-3])


@bp.route('/scraper', methods=['GET'])
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
