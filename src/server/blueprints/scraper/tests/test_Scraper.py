#!/usr/bin/env python3

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from ..Scraper import Scraper, createDriver, createScraper, deleteDriver
from .test_Script import MOCK_RESULT

def test_createDriver():
    assert isinstance(createDriver(**Scraper.DEFAULT_OPTIONS), WebDriver), 'Should return an instance of `Webdriver`'
    assert createDriver() == createDriver(), 'Should return the same instance (Singleton)'


class TestScraper:

    @pytest.fixture
    def scraper(self) -> Scraper:
        result = Scraper()
        yield result

        # scrape() calls createDriver() so we must do some cleanup
        deleteDriver()

    def test_scrape(self, scraper):
        result = scraper.scrape('tests/test_Script')

        assert isinstance(result, list), 'Should return a list object'
        assert result == MOCK_RESULT, 'Should call script->execute'

def test_createScraper():
    assert isinstance(createScraper(), Scraper), 'Should create a `Scrapper` object'

    scraper = createScraper(foo=1, bar='foo')

    assert scraper.options['foo'] == 1, 'Should forward `kwargs` -> `options`'
    assert scraper.options['bar'] == 'foo', 'Should forward `kwargs` -> `options`'
