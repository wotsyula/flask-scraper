#!/usr/bin/env python3
"""
Tests for `findpeople` script.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest

from .login import Script
from ..scraper import create_driver, create_script, Scraper

@pytest.fixture
def driver():
    return create_driver(**Scraper.DEFAULT_OPTIONS)


@pytest.fixture
def script(driver):
    return create_script('google/login', driver)

class TestScript:
    def test_execute(self, script: Script):
        script.driver.get('http://example.com/')
        script.execute()
        script.execute(user_pass = 'foo')

        assert script.driver.current_url == 'http://example.com/' \
            , 'It should do nothing with no user_name'

        script.execute()
        script.execute(user_name = 'foo')

        assert script.driver.current_url == 'http://example.com/' \
            , 'It should do nothing with no user_pass'

        script.execute(
            user_name = 'foo',
            user_pass = 'bar',
        )

        assert script.driver.current_url == '' \
            , 'It should do nothing with no user_pass'

        assert script.driver.current_url == '' \
            , 'It should do nothing with no user_pass'
