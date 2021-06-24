#!/usr/bin/env python3
"""
Defines fixtures for `server` module
"""
# pylint: disable=missing-function-docstring
import pytest
from .app import create_app as base_create_app

@pytest.fixture(scope='session')
def create_app():
    return base_create_app
