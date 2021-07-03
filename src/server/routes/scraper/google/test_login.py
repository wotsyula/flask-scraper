#!/usr/bin/env python3
"""
Tests for `findpeople` script.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest
from fake_useragent.fake import UserAgent

from .login import BAD_REQUEST, Script
from ..scraper import create_driver, create_script, Scraper

@pytest.fixture
def driver():
    driver = create_driver(
        **Scraper.DEFAULT_OPTIONS,
        user_agent = UserAgent().chrome,
    )

    yield driver

    driver.close()
    driver.quit()


@pytest.fixture
def script(driver):
    return create_script('google/login', driver)

class TestScript:
    def test_execute(self, script: Script):
        script.driver.get('http://example.com/')

        assert next(script.execute()) == BAD_REQUEST \
            , 'Should yield bad request with no `user_name` option'

        assert next(script.execute(user_pass='foo')) == BAD_REQUEST \
            , 'Should yield bad request with no `user_name` option'

        assert next(script.execute(user_name='foo')) == BAD_REQUEST \
            , 'Should yield bad request with no `user_pass` option'

        result = next(script.execute(
            user_name = 'pokemon',
            user_pass = 'pokemon',
        ))

        assert result.status == 200 \
            , 'Should return a result with user_name and user_pass'

        assert result.error is None \
            , 'Should return a result with user_name and user_pass'

        assert isinstance(result.result, dict) \
            , 'Should return a result with user_name and user_pass'
