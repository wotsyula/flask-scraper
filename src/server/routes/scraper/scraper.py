#!/usr/bin/env python3
"""
Defines functions and classes for managing `Scraper` object.
"""
import os
import random
from typing import Generator
from selenium.webdriver import Remote as WebDriver, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from .script import create_script

CHROME_URI = 'http://localhost:4444' \
    if not os.environ.get('SELENIUM_URI') else os.environ.get('SELENIUM_URI')
CHROME_USER_AGENT   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                    + 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    + 'Chrome/91.0.4472.101 ' \
                    + 'Safari/537.36 OPR/77.0.4054.90'


def generate_driver(timeout = 30, **kwargs) -> Generator[WebDriver, None, None]:
    """
    Creates selenium `Webdriver` instances.

    Args:
        timeout (int, optional): Value sent to `driver.implicitly_wait`. Defaults to 30.

    Yields:
        Generator[WebDriver, None, None]: instance to use for scrapping
    """
    timeout = kwargs.pop('timeout', 30)
    user_agent = kwargs.pop('user_agent', CHROME_USER_AGENT)

    while True:
        # create driver options
        options = ChromeOptions()

        # change user agent
        options.add_argument(f'--user-agent="{user_agent}"')

        # disable features not compatible with docker
        options.add_argument('--no-sandbox')

        # disable automation extension
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # configure browser settings
        options.add_experimental_option('prefs',  {
            'enable_do_not_track': True,                        # tell servers not to track us
            'webkit.webprefs.encrypted_media_enabled': False,   # disable protected content
        })

        driver = WebDriver(options=options, **kwargs)

        # set timeout for driver operations
        driver.implicitly_wait(timeout)

        # change view port
        driver.set_window_size(
            1300 + random.randint(1, 10) * 10,
            900 + random.randint(2, 9) * 10,
        )

        yield driver

        # close browser when done
        driver.close()
        driver.quit()


def create_driver(**kwargs) -> WebDriver:
    """
    Creates a selenium `Webdriver` instance.

    Args:
        **timeout (int): Value sent to `driver.implicitly_wait`. Defaults to 30.
        **user_agent (str): User Agent header. Defaults to latest version of Chrome.
        **kwargs (any): All extra arguments are forwarded to seleniums `Webdriver()` constructor

    Returns:
        WebDriver: instance to use for scrapping
    """
    return next(generate_driver(**kwargs))

class Scraper:
    """
    Class for managing scraping of scripts in `/scrapper` directory.
    """

    DEFAULT_OPTIONS = {
        'command_executor': CHROME_URI,
    }


    def scrape (self, path: str, **kwargs) -> Generator[dict, None, None]:
        """
        Executes a script in the `/scrapper` directory.

        Args:
            path (str): path to script in `/scrapper` directory

        Returns:
            Generator[dict, None, None]: See `script.py:Script:execute`
        """
        driver = create_driver(**self.options)
        script = create_script(path, driver, **self.options)

        return script.execute(**kwargs)


    def __init__(self, **kwargs) -> None:
        self.options = {**self.DEFAULT_OPTIONS, **kwargs}


def create_scraper(**kwargs) -> Scraper:
    """
    Factory function for `Scraper`.

    Returns:
        Scraper: an instance of `Scraper`
    """
    return Scraper(**kwargs)
