#!/usr/bin/env python3
"""
Defines fixtures for `server` module
"""
# pylint: disable=missing-function-docstring
import time
from typing import Generator
from fake_useragent.fake import UserAgent
from flask.app import Flask
from flask.blueprints import Blueprint
import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from .config import DefaultConfig
from .routes.scraper.scraper import CHROME_USER_AGENT, Scraper, create_driver

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

@pytest.fixture(scope='function')
def driver() -> Generator[WebDriver, None, None]:
    """
    Returns an instance of selenium `WebDriver`.

    Yields:
        WebDriver: selenium driver instance
    """
    user_agent = UserAgent(cache=False, fallback=CHROME_USER_AGENT).chrome
    instance = create_driver(**Scraper.DEFAULT_OPTIONS, user_agent=user_agent)

    # let driver load
    time.sleep(10)

    yield instance

    # NOTE: prevent crashed sessions from failing tests
    try:
        instance.close()
        instance.quit()
    except WebDriverException:
        pass

@pytest.fixture(scope='function')
def session_driver() -> Generator[WebDriver, None, None]:
    """
    Returns an instance of selenium `WebDriver`.

    Yields:
        WebDriver: selenium driver instance
    """
    instance = create_driver(**Scraper.DEFAULT_OPTIONS, save_session=True)

    # let driver load
    time.sleep(10)

    yield instance

    # NOTE: prevent crashed sessions from failing tests
    try:
        instance.close()
        instance.quit()

    except WebDriverException:
        pass
