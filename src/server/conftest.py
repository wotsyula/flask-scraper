#!/usr/bin/env python3
"""
Defines fixtures for `server` module
"""
# pylint: disable=missing-function-docstring
from fake_useragent.fake import UserAgent
from flask.app import Flask
from flask.blueprints import Blueprint
import pytest

from .config import DefaultConfig
from .routes.scraper.scraper import Scraper, create_driver

@pytest.fixture(scope='session')
def create_app():
    """
    Returns a function used to create a Flask app in the form:
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

@pytest.fixture(scope='module')
def driver():
    """
    Returns an instance of selenium `WebDriver`.

    Yields:
        WebDriver: selenium driver instance
    """
    instance = create_driver(
        **Scraper.DEFAULT_OPTIONS,
        user_agent = UserAgent(cache=False).chrome,
    )

    yield instance

    instance.close()
    instance.quit()
