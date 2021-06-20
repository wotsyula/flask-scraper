#!/usr/bin/env python3

import os
import platform

CHROME_EXECUTABLE = 'chromedriver.exe' if platform.system() == 'Windows' else 'chromedriver'
CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), CHROME_EXECUTABLE))

from .Script import *
from .Scraper import *
