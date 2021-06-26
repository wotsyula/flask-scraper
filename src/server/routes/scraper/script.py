#!/usr/bin/env python3
"""
Describes functions and classes for managing `Script` objects.
"""
import importlib
import re
import os
from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver

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
