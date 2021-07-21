#!/usr/bin/env python3
"""
Tests for `scraper` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from .scraper import Scraper, create_driver, create_scraper
from .script import create_script

from .scripts.mock import MOCK_RESULT, Script as MockScript

def test_create_driver():
    driver = create_driver(**Scraper.DEFAULT_OPTIONS)

    assert isinstance(driver, WebDriver) \
        , 'Should return an instance of `Webdriver`'

    driver.close()
    driver.quit()

class TestScraper:

    @pytest.fixture
    def scraper(self) -> Scraper:
        return Scraper()

    def test_is_script(self, scraper: Scraper):
        assert not scraper.is_script('mock') \
            , 'Should return false'

    def test_run_script(self, scraper: Scraper):
        pass

    def test_add_script(self, scraper: Scraper):
        scraper.add_script('mock', None, None, [])

        assert scraper.is_script('mock') \
            , 'Should add a new script'

    def test_get_script(self, scraper: Scraper):
        assert scraper.get_script('mock') is None \
            , 'Should return None for non existant scripts'

        scraper.scrape('mock')

        assert isinstance(scraper.get_script('mock'), MockScript) \
            , 'Should return an instance of `Script`'

    def test_delete_script(self, scraper: Scraper, driver: WebDriver):
        script = create_script('mock', driver)
        generator = script.execute()

        scraper.add_script('mock', driver, script, generator)
        scraper.delete_script('mock')

        assert not scraper.is_script('mock') \
            , 'Should delete a script'

    def test_scrape(self, scraper: Scraper):
        assert scraper.scrape('mock') == 'done' \
            , 'Should return a string'

        assert scraper.is_script('mock') \
            , 'Should add a new script'

    def test_get_results(self, scraper: Scraper):
        scraper.scrape('mock')

        assert scraper.get_results('mock') == [MOCK_RESULT] \
            , 'Should return results from script'

def test_create_scraper():
    assert isinstance(create_scraper(), Scraper) \
        , 'Should create a `Scrapper` object'

    scraper = create_scraper(foo=1, bar='foo')

    assert scraper.options['foo'] == 1 \
        , 'Should forward `kwargs` -> `options`'
    assert scraper.options['bar'] == 'foo' \
        , 'Should forward `kwargs` -> `options`'
