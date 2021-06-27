#!/usr/bin/env python3
"""
Tests for `findpeople` script.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest

from .findpeople import Script
from ..scraper import create_driver, create_script, Scraper

@pytest.fixture
def driver():
    return create_driver(**Scraper.DEFAULT_OPTIONS)


@pytest.fixture
def script(driver):
    return create_script('google/findpeople', driver)

class TestScript:
    def test_execute(self, script: Script):
        script.driver.get('http://example.com/')
        script.execute()

        assert script.driver.current_url == 'http://example.com/' \
            , 'It should do nothing with no query'

        script.execute(
            query = 'Donald Trump',
        )

        assert script.driver.current_url == '' \
            , 'It should do nothing with no user_pass'

        assert script.driver.current_url == '' \
            , 'It should do nothing with no user_pass'
