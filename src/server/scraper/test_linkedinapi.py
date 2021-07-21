#!/usr/bin/env python3
"""
Tests for `script` module.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import time
import pytest

from .linkedinapi import (
    LinkedInAPI,
    create_linkedinapi,
)

class TestLinkedInAPI:
    @pytest.fixture
    def linkedinapi(self, session_driver):
        session_driver.get('https://www.linkedin.com/home')
        time.sleep(5)

        return LinkedInAPI(session_driver)

    def test_is_logged_in(self, driver, session_driver):
        assert not LinkedInAPI.is_logged_in(driver) \
            , 'Should return `False` if `driver` session is not logged in'

        assert LinkedInAPI.is_logged_in(session_driver) \
            , 'Should return `True` if `driver` session is not logged in'

    def test_get_headers(self, session_driver):
        headers = LinkedInAPI.get_headers(session_driver)

        assert isinstance(headers, dict) \
            , 'Should return a dict'

        assert 'csrf-token' in headers \
            , 'Should have CSRF-Token header'

    def test_get_cookies(self, session_driver):
        cookies = LinkedInAPI.get_cookies(session_driver)

        assert 'JSESSIONID' in cookies \
            , 'Should return `JSESSIONID` cookie'

    def test_sanitize_path(self):

        assert LinkedInAPI.sanitize_path('/foo') == 'foo' \
            , 'Should remove starting slash'

    def test_call(self, linkedinapi: LinkedInAPI):
        result = linkedinapi.call('/identity/profiles/williamhgates/profileView')

        assert result.status_code == 200 \
            , 'Should return a result'

        assert 'included' in result.json() \
            , 'Should return a result'

    def test_get_profile(self, linkedinapi: LinkedInAPI):
        result = linkedinapi.get_profile('jcrossman')

        assert isinstance(result, dict) \
            , 'Should return a JSON response'

    def test__init__(self, driver, session_driver):
        # Should throw an error if driver is not an instance of `WebDriver`
        with pytest.raises(TypeError):
            LinkedInAPI(None)

        # Should throw an error if session is not logged in
        with pytest.raises(TypeError):
            LinkedInAPI(driver)

        assert LinkedInAPI(session_driver) \
            , 'Should not throw an error'


def test_create_linkedinapi(session_driver):
    assert isinstance(create_linkedinapi(session_driver), LinkedInAPI) \
        , 'Should create a `LinkedInAPI` instance'
