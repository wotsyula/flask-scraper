#!/usr/bin/env python3
"""
Tests for `blueprint` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
from flask import url_for
from flask.testing import FlaskClient

from .index import index

@pytest.fixture
def app(create_app):
    return create_app(__name__, index)

def test_status(client: FlaskClient):
    response = client.get(url_for('index.get_status'))

    assert response.status_code == 200 \
        , 'Should return status code 200'

    assert response.json == {'error': None, 'result': {}, 'status': 0} \
        , 'Should return an empty response'
