#!/usr/bin/env python3

import logging
import os
import platform
from selenium.webdriver import Remote as WebDriver, DesiredCapabilities, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from .Script import createScript

CHROME_URI = 'http://localhost:4444' if not os.environ.get('SELENIUM_URI') else os.environ.get('SELENIUM_URI')
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


def createDriver(**kwargs) -> WebDriver:

    if isinstance(createDriver.driver, WebDriver) != True:
        createDriver.driver = WebDriver(**kwargs)        

    return createDriver.driver

createDriver.driver = None


def deleteDriver() -> None:
    if createDriver.driver != None:
        createDriver.driver.quit()
        createDriver.driver = None


class Scraper:

    DEFAULT_OPTIONS = {
        'command_executor': CHROME_URI,
        'desired_capabilities': CHROME_CAPABILITIES,
        'options': CHROME_OPTIONS,
    }


    def scrape (self, path: str, **kwargs) -> list[dict]:

        options = dict(**self.options, **kwargs)
        
        logging.info(f'Scraping ({path})', extra=options)

        driver = createDriver(**options)
        script = createScript(path, driver, **options)

        return script.execute(**options)


    def __init__(self, **kwargs) -> None:
        self.options = dict(**self.DEFAULT_OPTIONS, **kwargs) 


def createScraper(**kwargs) -> Scraper:
    return Scraper(**kwargs)
