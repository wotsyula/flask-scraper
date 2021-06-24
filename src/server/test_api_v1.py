#!/usr/bin/env python3
"""
Tests for `blueprint` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from flask.helpers import url_for
import pytest
from .app import app as base_app

@pytest.fixture(scope='session')
def app():
    return base_app

def test_api_v1_index(client):
    response = client.get(url_for('.'))

    assert response.status == 400
