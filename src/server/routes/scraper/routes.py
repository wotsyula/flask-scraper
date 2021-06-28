#!/usr/bin/env python3
"""
Defines routes for `/scraper` subdirectory
"""
import time
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
from flask import Blueprint, jsonify, abort, request

from .scraper import create_scraper
from .script import SCRIPTS, validate_script

scraper = Blueprint('scraper', __name__, url_prefix='/scraper')
executor = ThreadPoolExecutor(16)

@scraper.route('/status', methods=['GET'])
def get_status():
    """
    Displays the status of api
    """
    return jsonify({
        'status': 0,
        'error': None,
        'result': {
            'scrips': SCRIPTS,
        }
    })

SCRIPT_RESULTS: dict[str, list] = {}
SCRIPT_FUTURES: dict[str, Future] = {}

def execute_script(script: str, **kwargs):
    """
    Thread that executes a script.

    Args:
        script (str): script to execute
    """
    # scrape results
    for result in create_scraper().scrape(script, **kwargs):
        # create list for script results
        if script not in SCRIPT_RESULTS or not isinstance(SCRIPT_RESULTS[script], list):
            SCRIPT_RESULTS[script] = []

        # add result
        SCRIPT_RESULTS[script].append(result)

@scraper.route('/<site>', methods=['GET'], defaults={'script': ''})
@scraper.route('/<site>/<script>', methods=['GET'])
def get_site_script(site, script):
    """
    Starts scripts.

    Args:
        site (str): module for script. ie `google`
        script (str): script to execute. ie 'login.py`

    Returns:
        str: JSON data
    """
    # calculate script
    script = site if len(script) < 2 else f'{site}/{script}'

    # validate script
    if not validate_script(script):
        return abort(404)

    # stop previous scrape
    if script in SCRIPT_FUTURES and isinstance(SCRIPT_FUTURES[script], Future):
        SCRIPT_FUTURES[script].cancel()

    # start scrape
    SCRIPT_FUTURES[script] = executor.submit(execute_script, script, **request.args)

    if script not in SCRIPT_RESULTS or not isinstance(SCRIPT_RESULTS[script], list):
        SCRIPT_RESULTS[script] = []

    # prevent race conditions
    time.sleep(4)

    # empty result
    return jsonify({
        'status': 0,
        'error': None,
        'result': {},
    })

@scraper.route('/<site>/status', methods=['GET'], defaults={'script': ''})
@scraper.route('/<site>/<script>/status')
def get_site_script_status(site, script):
    """
    Retrieves script results.

    Args:
        site (str): module for script. ie `google`
        script (str): script to execute. ie 'login.py`

    Returns:
        str: JSON data
    """
    # calculate script
    script = site if len(script) < 2 else f'{site}/{script}'

    # check if scrape exists
    if script not in SCRIPT_FUTURES or not isinstance(SCRIPT_FUTURES[script], Future):
        return abort(404)

    # get results
    try:
        result = SCRIPT_FUTURES[script].result(timeout=0)
    except TimeoutError:
        result = 'running'

    return jsonify({
        'status': 0,
        'error': None,
        'result': result,
    })

@scraper.route('/<site>/results', methods=['GET'], defaults={'script': ''})
@scraper.route('/<site>/<script>/results')
def get_site_script_results(site, script):
    """
    Retrieves script results.

    Args:
        site (str): module for script. ie `google`
        script (str): script to execute. ie 'login.py`

    Returns:
        str: JSON data
    """
    # calculate script
    script = site if len(script) < 2 else f'{site}/{script}'

    # check if scrape exists
    if script not in SCRIPT_RESULTS or not isinstance(SCRIPT_RESULTS[script], list):
        return abort(404)

    # get results
    result = jsonify({
        'status': 0,
        'error': None,
        'result': SCRIPT_RESULTS[script],
    })
    SCRIPT_RESULTS[script] = []

    return result

@scraper.route('/<site>/cancel', methods=['GET'], defaults={'script': ''})
@scraper.route('/<site>/<script>/cancel')
def get_site_script_cancel(site, script):
    """
    Retrieves script results.

    Args:
        site (str): module for script. ie `google`
        script (str): script to execute. ie 'login.py`

    Returns:
        str: JSON data
    """
    # calculate script
    script = site if len(script) < 2 else f'{site}/{script}'

    # cancel script
    result = False

    if script in SCRIPT_FUTURES or not isinstance(SCRIPT_FUTURES[script], Future):
        result = SCRIPT_FUTURES[script].cancel()

    # get results
    return jsonify({
        'status': 0,
        'error': None,
        'result': result,
    })
