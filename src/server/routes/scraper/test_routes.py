#!/usr/bin/env python3
"""
Tests for `blueprint` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import time
import pytest
from flask import url_for
from flask.testing import FlaskClient

from .routes import scraper
from .test_script import MOCK_RESULT

@pytest.fixture
def app(create_app):
    return create_app(__name__, scraper)

def test_get_status(client: FlaskClient):
    response = client.get(url_for('scraper.get_status'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json['status'] == 0 \
        , 'Should return status of 0'

    assert response.json['error'] is None \
        , 'Should return no error'

    assert isinstance(response.json['result'], dict) \
        , 'Should return a dict result'

def test_get_site_script(client: FlaskClient):
    response = client.get(url_for('scraper.get_site_script', script='test_script'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json == {'status':0, 'error':None, 'result':'done'} \
        , 'Should return a success response'

def test_get_site_script_status(client: FlaskClient):
    client.get(url_for('scraper.get_site_script', script='test_script'))
    response = client.get(url_for('scraper.get_site_script_status', script='test_script'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json == {'status':0, 'error':None, 'result':'done'} \
        , 'Should return a done state'

def test_get_site_script_cancel(client: FlaskClient):
    client.get(url_for('scraper.get_site_script', script='test_script'))
    response = client.get(url_for('scraper.get_site_script_cancel', script='test_script'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json['status'] == 0 \
        , 'Should return status of 0'

    assert response.json['error'] is None \
        , 'Should return no error'

    assert isinstance(response.json['result'], bool) \
        , 'Should return a boolean result'

def test_get_site_script_results(client: FlaskClient):
    client.get(url_for('scraper.get_site_script', script='test_script'))
    response = client.get(url_for('scraper.get_site_script_results', script='test_script'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json == {'status': 0, 'error': None, 'result': [MOCK_RESULT]} \
        , 'Should return test result'

    response = client.get(url_for('scraper.get_site_script_results', script='test_script'))

    assert response.json['result'] == [] \
        , 'Should consume results stored by scrapper'
