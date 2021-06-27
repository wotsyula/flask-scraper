#!/usr/bin/env python3
"""
Describes functions and classes for managing `Script` objects.
"""
import importlib
import os
import random
import re
import time
from abc import ABC, abstractmethod
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import wait, expected_conditions as EC

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SCRIPTS = []

for directory in os.listdir(SCRIPT_DIR):
    abs_directory = os.path.join(SCRIPT_DIR, directory)

    if os.path.isdir(abs_directory):
        for script in os.listdir(abs_directory):
            if re.match('^[a-z]+.py$', script) is not None:
                SCRIPTS.append(directory + '/' + script[:-3])


def validate_script(path: str) -> bool:
    """
    Validates a script path from scraper directory.

    Args:
        path (str): path to validate

    Returns:
        bool: `True` if valid and `False` otherwise.
    """
    return isinstance(path, str) and len(path) > 0


def sanitize_script(path: str) -> str:
    """
    Validates and sanitizes a script path from scraper directory
    and returns it's python module name.

    Args:
        path (str): path to sanitize

    Raises:
        TypeError: If path is not an non-empty string
        TypeError: If path does not match regex `^([A-Za-z_]+/?)+$`

    Returns:
        str: module or `None` if unavailable
    """

    if validate_script(path) is not True:
        raise TypeError(f'path must be a non empty string ({path})')

    module = re.search(r'^([A-Za-z_]+/?)+$', path)

    if isinstance(module, re.Match) is not True:
        raise TypeError(f'invalid path {path})')

    module = '..' + module.group().rstrip('/').replace('/', '.')

    return module


def load_script(path) -> any:
    """
    Validates and sanitizes a script path from scraper directory
    and returns it's python module.

    Args:
        path ([type]): path to script

    Returns:
        any: module if successfull and `None` if not
    """
    module = sanitize_script(path)

    if module:
        module = importlib.import_module(module, __name__)

    return module


class Script (ABC):
    # pylint: disable=too-few-public-methods
    """
    Abstract class that all scripts inherit from.

    Args:
        driver (selenium.webdriver.remote.webdriver.Webdriver): driver to use for script

    Raises:
        TypeError: if driver is not an instance of Webdriver
    """
    DEFAULT_OPTIONS = {}

    @staticmethod
    def sleep(multiplier = 1):
        """
        Sleeps a random ammount of milliseconds (100-2,000) * `multiplier`

        Args:
            multiplier (int, optional): Multiplier of random milliseconds. Defaults to 1.

        Raises:
            TypeError: if not multiplier > 1
        """
        if not isinstance(multiplier, int) or multiplier < 1:
            raise TypeError('multiplier should be an number larger than 0')

        # Get duration to wait in milliseconds
        duration = multiplier * random.randint(300, 1000) / 1000

        time.sleep(duration)


    def click(self, xpath: str) -> WebElement:
        """
        Clicks an element

        Args:
            xpath (str): XPath of element to click

        Returns:
            WebElement: returns element found by `find_element_by_xpath()`
        """
        element_clickable = EC.element_to_be_clickable((By.XPATH, xpath))

        self.action.move_to_element(self.wait.until(element_clickable)).perform()
        self.wait.until(element_clickable).click()
        self.sleep(4)

        return self.wait.until(element_clickable)

    def send_keys(self, xpath: str, keys: str, click = False) -> WebElement:
        """
        Sends keystrokes to an element

        Args:
            xpath (str): XPath of element to click
            click (bool, optional): If `True` will click on element before sending keys. Defaults to False.

        Returns:
            WebElement: returns element found by `find_element_by_xpath()`
        """
        element_exists = EC.presence_of_element_located((By.XPATH, xpath))

        if click:
            self.wait.until(element_exists).click()
            self.sleep(2)

        for char in keys:
            self.wait.until(element_exists).send_keys(char)
            self.sleep(1)

        return self.wait.until(element_exists)

    @abstractmethod
    def execute(self, **kwargs) -> list[dict]:
        """
        Executes the script using `driver`.

        Returns:
            list[dict]: Returns a list of `dict` values
        """

    def __init__(self, driver: WebDriver, **kwargs) -> None:

        if isinstance(driver, WebDriver) is not True:
            raise TypeError('driver should be an instance of Webdriver')

        super().__init__()

        self.options = dict(**self.DEFAULT_OPTIONS, **kwargs)
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.wait = wait.WebDriverWait(self.driver, 10)

def create_script(path: str, driver: WebDriver, **kwargs) -> Script:
    """
    Creates a `Script` from scraper directory from module in path.

    Args:
        path (str): Relative position of script in scrapper directory
        driver (WebDriver): Selenium `Webdriver` instance

    Raises:
        Exception: [description]

    Returns:
        Script: [description]
    """
    mod = load_script(path)

    if hasattr(mod, "Script") is not True or isinstance(mod.Script, type) is not True:
        raise Exception(f'invalid module ({path})')

    return mod.Script(driver, **kwargs)
