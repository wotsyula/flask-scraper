#!/usr/bin/env python3
"""
Defines functions and classes for managing `Scraper` object.
"""
import os
from typing import Generator
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Remote as WebDriver, DesiredCapabilities, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from .script import create_script

CHROME_URI = 'http://localhost:4444' \
    if not os.environ.get('SELENIUM_URI') else os.environ.get('SELENIUM_URI')
CHROME_CAPABILITIES = DesiredCapabilities.CHROME
CHROME_CAPABILITIES['prefs'] = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
}
CHROME_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
    + 'like Gecko) Chrome/91.0.4472.101 Safari/537.36 OPR/77.0.4054.90'


def generate_driver(timeout = 30, **kwargs) -> Generator[WebDriver, None, None]:
    """
    Creates selenium `Webdriver` instances.

    Args:
        timeout (int, optional): Value sent to `driver.implicitly_wait`. Defaults to 30.

    Yields:
        Generator[WebDriver, None, None]: instance to use for scrapping
    """

    while True:
        # generate user agent
        # user_agent = UserAgent(cache=False, fallback=CHROME_UA).random

        # create driver options
        options = ChromeOptions()

        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--headless')
        options.add_argument('--disable-notifications')
        # options.add_argument(f'--user-agent="{user_agent}"')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = WebDriver(options=options, **kwargs)

        # wait for elements
        driver.implicitly_wait(timeout)

        # change view port
        driver.set_window_size(1680, 990)

        yield driver

        # close browser when done
        driver.quit()


def create_driver(timeout = 30, **kwargs) -> WebDriver:
    """
    Creates a selenium `Webdriver` instance.

    Args:
        timeout (int, optional): Value sent to `driver.implicitly_wait`. Defaults to 30.

    Returns:
        WebDriver: instance to use for scrapping
    """
    return next(generate_driver(timeout=timeout, **kwargs))

class Scraper:
    """
    Class for managing scraping of scripts in `/scrapper` directory.
    """

    DEFAULT_OPTIONS = {
        'command_executor': CHROME_URI,
        'desired_capabilities': CHROME_CAPABILITIES,
    }


    def scrape (self, path: str, **kwargs) -> list[dict]:
        """
        Executes a script in the `/scrapper` directory.

        Args:
            path (str): path to script in `/scrapper` directory

        Returns:
            list[dict]: See `script.py:Script:execute`
        """
        options = {**self.options, **kwargs}
        driver = create_driver(**self.options)
        script = create_script(path, driver, **options)

        return script.execute(**options)


    def __init__(self, **kwargs) -> None:
        self.options = {**self.DEFAULT_OPTIONS, **kwargs}


def create_scraper(**kwargs) -> Scraper:
    """
    Factory function for `Scraper`.

    Returns:
        Scraper: an instance of `Scraper`
    """
    return Scraper(**kwargs)
