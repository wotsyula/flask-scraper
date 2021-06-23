#!/usr/bin/env python3
"""
Defines root blueprint for all flask routes
"""
from flask import Blueprint, jsonify

bp = Blueprint('api', __name__)

@bp.route('/')
def empty():
    """
    Desplays empty JSON response.
    """
    return jsonify({
        "status": 0,
        "error": None,
        "result": {},
    })
