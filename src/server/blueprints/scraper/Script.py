#!/usr/bin/env python3

from abc import ABC, abstractmethod
import importlib
import re

from selenium.webdriver.remote.webdriver import WebDriver

def validateScript(path: str) -> bool:
    return isinstance(path, str) and len(path) > 0


def sanitizeScript(path: str) -> str:
    
    if validateScript(path) != True:
        raise TypeError(f'path must be a non empty string ({path})')

    module = re.search(r'^([A-Za-z_]+/?)+$', path)

    if isinstance(module, re.Match) != True:
        raise TypeError(f'invalid path {path})')

    module = '..' + module.group().rstrip('/').replace('/', '.')
    
    return module         


def loadScript(path) -> any:
    module = sanitizeScript(path)
    
    if module:
        module = importlib.import_module(module, __name__)

    return module


class Script (ABC):
    DEFAULT_OPTIONS = {}

    @abstractmethod
    def execute (self, **kwargs) -> list[dict]:
        pass

    def __init__(self, driver: WebDriver, **kwargs) -> None:

        if isinstance(driver, WebDriver) != True:
            raise TypeError('driver should be an instance of Webdriver')

        super().__init__()

        self.options = dict(**self.DEFAULT_OPTIONS, **kwargs)
        self.driver = driver


def createScript(path: str, driver: WebDriver, **kwargs) -> Script:
    mod = loadScript(path)

    if hasattr(mod, "Script") != True or isinstance(mod.Script, type) != True:
        raise Exception(f'invalid module ({path})')

    return mod.Script(driver, **kwargs)
