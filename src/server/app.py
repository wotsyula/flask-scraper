#!/usr/bin/env python3

import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DefaultConfig, baseDir
from blueprints import defaultBP

app = Flask(__name__)
cfg = DefaultConfig()

app.config.from_object(cfg)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.content_type = "application/json"
    response.data = json.dumps({
        "status": e.code,
        "error": e.name,
        "result": None
    })
    
    return response

app.register_blueprint(defaultBP, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()