#!/usr/bin/env python3
"""
Defines routes for `/status` subdirectory
"""
from .. import bp, empty

@bp.route('/status')
def status():
    """
    TODO
    """
    return empty()
