#!/usr/bin/env python3
"""
Fask application
"""

import logging
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from .config import DefaultConfig
from .blueprints import bp

app = Flask(__name__)
cfg = DefaultConfig()

app.config.from_object(cfg)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.errorhandler(HTTPException)
def handle_exception(err):
    """
    Return JSON instead of HTML for HTTP errors.
    """
    logging.exception(err.name, exc_info=err)

    # start with the correct headers and status code from the error
    response = err.get_response()
    # replace the body with JSON
    response.content_type = "application/json"
    response.data = json.dumps({
        "status": err.code,
        "error": err.name,
        "result": None
    })

    return response

app.register_blueprint(bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()
