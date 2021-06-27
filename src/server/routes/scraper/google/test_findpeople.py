#!/usr/bin/env python3
"""
Tests for `findpeople` script.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
from selenium.webdriver.common.keys import Keys

from .findpeople import Script
from ..scraper import create_driver, create_script, Scraper

@pytest.fixture
def driver():
    return create_driver(**Scraper.DEFAULT_OPTIONS)


@pytest.fixture
def script(driver):
    return create_script('google/findpeople', driver)

class TestScript:
    def test_go_to_next(self, script: Script):
        """
        Test if `go_to_next()` controls page navigation
        """

        # go to google.com website
        if 'google.com/search' not in script.driver.current_url:
            script.driver.get('https://google.com')

        # enter search term
        script.send_keys('//*[@name="q"]', 'web development' + Keys.ENTER)

        # go to 1st page
        script.current_page = 0

        assert script.go_to_next() is False \
            , 'Should do nothing if current page is 0 or lower'

        # go to 2nd page
        script.current_page = 1

        assert script.go_to_next() is True \
            , 'Should return True'

        assert ' 2 ' in script.xpath('//*[@id="result-stats"]').text \
            , 'Should navigate to second page'

        assert script.current_page == 2 \
            , 'Should update page pointer'

        # go to next page
        script.go_to_next()

        assert ' 3 ' in script.xpath('//*[@id="result-stats"]').text \
            , 'Should navigate to second page'

        assert script.current_page == 3 \
            , 'Should update page pointer'

        # go to page 100
        script.current_page = 99

        assert script.go_to_next() is False \
            , 'Should do nothing if current page is 99 or higher'

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
