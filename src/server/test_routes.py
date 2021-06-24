#!/usr/bin/env python3
"""
Tests for `blueprint` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from flask.helpers import url_for
from flask.testing import FlaskClient
import pytest
from .index import index

@pytest.fixture
def app(create_app):
    test_app = create_app(__name__)

    test_app.register_blueprint(index)

    return test_app

def test_status(client: FlaskClient):
    response = client.get(url_for('index.get_status'))

    assert response.status_code == 200
