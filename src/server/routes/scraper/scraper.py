#!/usr/bin/env python3
"""
Defines functions and classes for managing `Scraper` object.
"""
import logging
import os
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
CHROME_OPTIONS = ChromeOptions()
# CHROME_OPTIONS.add_argument('--disable-extensions')
# CHROME_OPTIONS.add_argument('--disable-gpu')
# CHROME_OPTIONS.add_argument('--disable-notifications')
CHROME_OPTIONS.add_argument('--headless')


def create_driver(timeout: int = 10, **kwargs) -> WebDriver:
    """
    Creates a selenium `Webdriver` instance.

    Args:
        timeout (int, optional): Value sent to `driver.implicitly_wait`. Defaults to 10.

    Returns:
        selenium.webdriver.Remote: instance to use for scraping
    """
    if isinstance(create_driver.driver, WebDriver) is not True:
        create_driver.driver = WebDriver(**kwargs)

        create_driver.driver.implicitly_wait(timeout)

    return create_driver.driver

create_driver.driver = None


def delete_driver() -> None:
    """
    Destroys a selenium `Webdriver` instance.
    """
    if create_driver.driver is not None:
        create_driver.driver.quit()
        create_driver.driver = None


class Scraper:
    """
    Class for managing scraping of scripts in `/scrapper` directory.
    """

    DEFAULT_OPTIONS = {
        'command_executor': CHROME_URI,
        'desired_capabilities': CHROME_CAPABILITIES,
        'options': CHROME_OPTIONS,
        'timeout': 10,
    }


    def scrape (self, path: str, **kwargs) -> list[dict]:
        """
        Executes a script in the `/scrapper` directory.

        Args:
            path (str): path to script in `/scrapper` directory

        Returns:
            list[dict]: See `script.py:Script:execute`
        """
        options = dict(**self.options, **kwargs)

        logging.info(f'Scraping ({path})', extra=options)

        driver = create_driver(**options)
        script = create_script(path, driver, **options)

        return script.execute(**options)


    def __init__(self, **kwargs) -> None:
        self.options = dict(**self.DEFAULT_OPTIONS, **kwargs)


def create_scraper(**kwargs) -> Scraper:
    """
    Factory function for `Scraper`.

    Returns:
        Scraper: an instance of `Scraper`
    """
    return Scraper(**kwargs)
