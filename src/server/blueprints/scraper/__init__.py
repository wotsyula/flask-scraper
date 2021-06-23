#!/usr/bin/env python3
"""
Defines routes for `/scraper` subdirectory
"""
from .. import bp, empty

@bp.route('/scraper')
def status():
    """
    TODO
    """
    return empty()
