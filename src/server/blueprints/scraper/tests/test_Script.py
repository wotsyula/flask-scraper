#!/usr/bin/env python3

import pytest
from selenium import webdriver

from .. import CHROME_PATH, validateScript, sanitizeScript, loadScript, Script as BaseScript, createScript

from ..Script import *

INVALID_PATHS = [
    None,
    '',
    [],
    {},
]

VALID_PATHS = [
    'google',
    'google/search',
    'facebook',
    'facebook/user',
    'facebook/page',
]

MOCK_RESULT = [{
    'foo': 1,
    'bar': 'foo',
}]

class Script (Script):

    def execute(self, **kwargs) -> list[dict]:
        return MOCK_RESULT


def test_validateScript():

    for path in INVALID_PATHS:
        assert validateScript(path) == False, 'Should return false if path not a string'

    for path in VALID_PATHS:
        assert validateScript(path) == True, 'Return true for if path is valid'


def test_sanitizeScript(mocker):
    for path in INVALID_PATHS:
        """Should raise an error if path is not a string"""
        with pytest.raises(TypeError) as err:
            sanitizeScript("abc.def")

    """Should raise an error if path contains full stop (.)"""
    with pytest.raises(TypeError) as err:
        sanitizeScript("abc.def")

    for number in range(0-9):
        """Should raise an error if path contains a number (0-9)"""
        with pytest.raises(TypeError) as err:
            sanitizeScript(f'abc{number}def')

    for path in VALID_PATHS:
        assert isinstance(sanitizeScript(path), str), 'Should return string'


def test_loadScriptModule():
    """Should raise an error for non existent modules"""
    with pytest.raises(Exception) as err:
        loadScript('__non_existent_module__')

    mod = loadScript('tests/test_Script')
    assert hasattr(mod, 'Script'), 'Should return a Script module'


class TestScript:
    pass

def test_createScript():
    driver = webdriver.Chrome(executable_path=CHROME_PATH)

    """Should throw an error if module does not have 'Script' property"""
    with pytest.raises(Exception) as err:
        createScript('tests/test_Scraper', driver)

    assert isinstance(createScript('tests/test_Script', driver), BaseScript), 'Should create a `Script` object'

    driver.quit()
