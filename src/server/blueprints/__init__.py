#!/usr/bin/env python3

from flask import Blueprint, jsonify

defaultBP = Blueprint('api', __name__)

@defaultBP.route('/')
def home():
    return jsonify({
        "status": 0,
        "error": None,
        "result": {},
    })
