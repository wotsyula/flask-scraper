#!/usr/bin/env python3
"""
Tests for `blueprint` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import json
import pytest
from flask import url_for
from flask.testing import FlaskClient

from . import index

@pytest.fixture
def app(create_app):
    return create_app(__name__, index)

def test_get_status(client: FlaskClient):
    response = client.get(url_for('index.get_status'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json == {'status': 0, 'error': None, 'result': True} \
        , 'Should return an empty response'

def test_handle_exception(client: FlaskClient):
    response = client.get('/non-existent-endpoint')

    assert response.content_type == 'application/json' \
        , 'Should return a json response'

    assert json.loads(response.data) == {"status": 404, "error": "Not Found", "result": None} \
        , 'Should return a json response'
