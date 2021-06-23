#!/usr/bin/env python3

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from ..scraper import Scraper, create_driver, create_scraper
from .test_script import MOCK_RESULT

def test_create_driver():
    assert isinstance(create_driver(**Scraper.DEFAULT_OPTIONS), WebDriver) \
        , 'Should return an instance of `Webdriver`'
    assert create_driver() == create_driver() \
        , 'Should return the same instance (Singleton)'


class TestScraper:

    @pytest.fixture
    def scraper(self) -> Scraper:
        return Scraper()

    def test_scrape(self, scraper):
        result = scraper.scrape('tests/test_script')

        assert isinstance(result, list) \
            , 'Should return a list object'
        assert result == MOCK_RESULT \
            , 'Should call script->execute'

def test_create_scraper():
    assert isinstance(create_scraper(), Scraper) \
        , 'Should create a `Scrapper` object'

    scraper = create_scraper(foo=1, bar='foo')

    assert scraper.options['foo'] == 1 \
        , 'Should forward `kwargs` -> `options`'
    assert scraper.options['bar'] == 'foo' \
        , 'Should forward `kwargs` -> `options`'
