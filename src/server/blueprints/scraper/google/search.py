#!/usr/bin/env python3
"""
Defines the script for `/scrapper/google/search` subdirectory
"""

from ..script import Script as BaseClass

class Script (BaseClass):
    """
    Script that is imported by `Scraper` object.
    See `Scraper.scrape()` function.
    """
    def execute(self, **kwargs) -> list[dict]:
        return []
