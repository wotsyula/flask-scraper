#!/usr/bin/env python3
"""
Mock script for testing.
"""
from typing import Generator
from ..script import Script as BaseScript

MOCK_RESULT = {
    'foo': 1,
    'bar': 'foo',
}

class Script (BaseScript):
    def execute(self, **kwargs) -> Generator[dict, None, None]:
        yield MOCK_RESULT

