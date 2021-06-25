#!/usr/bin/env python3
"""
Defines fixtures for `server` module
"""
# pylint: disable=missing-function-docstring
from flask.app import Flask
from flask.blueprints import Blueprint
import pytest

from .config import DefaultConfig

@pytest.fixture(scope='session')
def create_app():
    """
    Returns a function used to create an ap in the form:
    `create_app(name: str, blue_print: Blueprint = None)`
    """
    def result(name: str, blue_print: Blueprint = None):
        cfg = DefaultConfig()
        app = Flask(name)

        app.config.from_object(cfg)

        if blue_print is not None:
            app.register_blueprint(blue_print)

        return app

    return result
