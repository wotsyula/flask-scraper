#!/usr/bin/env python3
"""
Fask application
"""

from flask import Flask, json, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import DefaultConfig, STATIC_DIR
from .routes import index

def create_app(name):
    """Factory for Flask libraries `Flask`.

    Args:
        name (string): Module name to attach to app (`__name__`).

    Returns:
        flask.Flask: Flask `app` instance
    """
    application = Flask(
        name,
        static_url_path='',
        static_folder=STATIC_DIR,
        
    )
    cfg = DefaultConfig()

    application.config.from_object(cfg)

    application.db = SQLAlchemy(application)
    application.migrate = Migrate(application, application.db)
    application.wsgi_app = ProxyFix(application.wsgi_app)

    return application

app = create_app(__name__)
app.register_blueprint(index, url_prefix='/api/v1')

@app.route('/', methods=['GET'])
def get_index():
    """
    Home page

    Returns:
        str: HTML
    """
    return current_app.send_static_file('index.htm')

@app.before_request
def handle_wsgi_input_terminated():
    """
    Werkzeug required environ 'wsgi.input_terminated' to be set
    otherwise it empties the input request stream.
    """
    if request.environ.get('HTTP_TRANSFER_ENCODING', '').lower() == 'chunked':
        if 'wsgi.input_terminated' not in request.environ:
            request.environ['wsgi.input_terminated'] = 1


@app.after_request
def set_headers(response):
    """
    Sets nice CORS for our server.

    Original source: https://github.com/postmanlabs/httpbin/blob/master/httpbin/core.py
    """
    response.headers['Server'] = 'Apache/2.4.6 (CentOS) PHP/5.4.16'
    response.headers['X-Powered-By'] = 'PHP / 5.4.16'
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    if request.method == 'OPTIONS':
        # Both of these headers are only used for the 'preflight request'
        # http://www.w3.org/TR/cors/#access-control-allow-methods-response-header
        response.headers[
            'Access-Control-Allow-Methods'
        ] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Max-Age'] = '3600'  # 1 hour cache

        if request.headers.get('Access-Control-Request-Headers') is not None:
            response.headers['Access-Control-Allow-Headers'] = request.headers[
                'Access-Control-Request-Headers'
            ]

    return response


if __name__ == '__main__':
    app.run()
