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
from .index import index

def create_app(name):
    """Factory for Flask libraries `Flask`.

    Args:
        name (string): Module name to attach to app (`__name__`).

    Returns:
        flask.Flask: Flask `app` instance
    """
    application = Flask(name)
    cfg = DefaultConfig()

    application.config.from_object(cfg)

    application.db = SQLAlchemy(application)
    application.migrate = Migrate(application, application.db)

    return application

app = create_app(__name__)
app.register_blueprint(index, url_prefix='/api/v1')

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

if __name__ == '__main__':
    app.run()
