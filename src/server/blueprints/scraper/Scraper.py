#!/usr/bin/env python3

import logging
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from . import CHROME_PATH
from .Script import createScript


def createDriver(**kwargs) -> WebDriver:

    if createDriver.driver == None:
        createDriver.driver = Chrome(**kwargs)        

    return createDriver.driver

createDriver.driver = None


def deleteDriver() -> None:
    if createDriver.driver != None:
        createDriver.driver.quit()
        createDriver.driver = None


class Scraper:

    DEFAULT_OPTIONS = {
        'executable_path': CHROME_PATH,
        'options': ChromeOptions(),
    }


    def scrape (self, path: str, **kwargs) -> list[dict]:

        options = dict(**self.options, **kwargs)
        
        logging.info(f'Scraping ({path})', extra=options)

        driver = createDriver(**options)
        script = createScript(path, driver, **options)

        return script.execute(**options)


    def __init__(self, **kwargs) -> None:
        self.options = dict(**self.DEFAULT_OPTIONS, **kwargs) 


# Scraper.DEFAULT_OPTIONS['options'].add_argument("--disable-extensions")
Scraper.DEFAULT_OPTIONS['options'].add_argument("--disable-gpu")
Scraper.DEFAULT_OPTIONS['options'].add_argument("--headless")


def createScraper(**kwargs) -> Scraper:
    return Scraper(**kwargs)
