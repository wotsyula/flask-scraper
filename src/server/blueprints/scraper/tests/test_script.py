#!/usr/bin/env python3

import pytest

from ..script import validate_script, sanitize_script, load_script, Script as BaseScript, create_script
from ..scraper import Scraper, create_driver

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

class Script (BaseScript):

    def execute(self, **kwargs) -> list[dict]:
        return MOCK_RESULT


def test_validate_script():

    for path in INVALID_PATHS:
        assert validate_script(path) is False \
            , 'Should return false if path not a string'

    for path in VALID_PATHS:
        assert validate_script(path) is True \
            , 'Return true for if path is valid'


def test_sanitize_script():
    for path in INVALID_PATHS:
        """Should raise an error if path is not a string"""
        with pytest.raises(TypeError):
            sanitize_script("abc.def")

    """Should raise an error if path contains full stop (.)"""
    with pytest.raises(TypeError):
        sanitize_script("abc.def")

    for number in range(0-9):
        """Should raise an error if path contains a number (0-9)"""
        with pytest.raises(TypeError):
            sanitize_script(f'abc{number}def')

    for path in VALID_PATHS:
        assert isinstance(sanitize_script(path), str) \
            , 'Should return string'


def test_load_script():
    """Should raise an error for non existent modules"""
    with pytest.raises(Exception):
        load_script('__non_existent_module__')

    mod = load_script('tests/test_Script')
    assert hasattr(mod, 'Script') \
        , 'Should return a Script module'


class TestScript:
    pass

def test_create_script():
    driver = create_driver(**Scraper.DEFAULT_OPTIONS)

    """Should throw an error if module does not have 'Script' property"""
    with pytest.raises(Exception):
        create_script('tests/test_scraper', driver)

    assert isinstance(create_script('tests/test_script', driver), BaseScript) \
        , 'Should create a `Script` object'
