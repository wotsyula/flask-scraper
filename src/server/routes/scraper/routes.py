#!/usr/bin/env python3
"""
Defines routes for `/scraper` subdirectory
"""
from flask import Blueprint, jsonify, abort, request

from .scraper import create_scraper
from .script import SCRIPTS, validate_script

scraper = Blueprint('scraper', __name__, url_prefix='/scraper')
instance = create_scraper(save_session=True)

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


@scraper.route('/<script>', methods=['GET'], defaults={'site': ''})
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
    if len(site) > 1:
        script = f'{site}/{script}'

    # validate script
    if not validate_script(script):
        return abort(404)

    # start scrape
    result = instance.scrape(script, **request.args)

    # empty result
    return jsonify({
        'status': 0,
        'error': None,
        'result': result,
    })

@scraper.route('/<script>/status', methods=['GET'], defaults={'site': ''})
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
    if len(site) > 1:
        script = f'{site}/{script}'

    # check if scrape exists
    if not instance.is_script(script):
        return abort(404)

    result = instance.get_status(script)

    return jsonify({
        'status': 0,
        'error': None,
        'result': result,
   })

@scraper.route('/<script>/results', methods=['GET'], defaults={'site': ''})
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
    if len(site) > 1:
        script = f'{site}/{script}'

    # check if scrape exists
    if not instance.is_script(script):
        return abort(404)

    # get results
    results = instance.get_results(script)

    return jsonify({
        'status': 0,
        'error': None,
        'result': results,
    })

@scraper.route('/<script>/cancel', methods=['GET'], defaults={'site': ''})
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
    if len(site) > 1:
        script = f'{site}/{script}'

    # check if scrape exists
    if not instance.is_script(script):
        return abort(404)

    # stop script
    instance.delete_script(script)

    return jsonify({
        'status': 0,
        'error': None,
        'result': True,
    })
