#!/usr/bin/env python3

import os
import platform
import pytest

TEST_PATH = os.path.abspath(os.path.dirname(__file__))
CHROME_EXECUTABLE = 'chromedriver.exe' if platform.architecture() == 'Windows' else 'chromedriver'
CHROME_PATH = os.path.join(TEST_PATH, CHROME_EXECUTABLE)

@pytest.fixture()
def resource():
    # Setup...
    yield None
    # Teardown...

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = CHROME_PATH
