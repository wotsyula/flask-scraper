#!/usr/bin/env python3
"""
Tests for `findpeople` script.
"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import os
import pytest

from .login_linkedin import BAD_REQUEST, SUCCESS, Script
from ..scraper import create_script


@pytest.fixture
def script(session_driver):
    yield create_script('login_linkedin', session_driver)

@pytest.mark.skip(reason="must be tested manually")
class TestScript:
    def test_execute(self, script: Script):
        assert next(script.execute(), None) == BAD_REQUEST \
            , 'Should yield bad request with no `user_name` option'

        assert next(script.execute(user_pass='foo'), None) == BAD_REQUEST \
            , 'Should yield bad request with no `user_name` option'

        assert next(script.execute(user_name='foo'), None) == BAD_REQUEST \
            , 'Should yield bad request with no `user_pass` option'

        result = next(script.execute(
            user_name=os.environ.get('SERVER_EMAIL'),
            user_pass=os.environ.get('SERVER_SECRET'),
        ), None)

        assert result == SUCCESS \
            , 'Should yield success with `user_name` and `user_pass option'
