#!/usr/bin/env python3
"""
Defines classes for managing configuration
"""

import os
# pylint: disable=too-few-public-methods

baseDir = os.path.abspath(os.path.dirname(__file__))

templateDir = os.path.join(baseDir, 'templates')

class Config:
    """
    Stores Flask configuration passed to `app.config.from_object()`.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET = os.environ.get('SERVER_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DefaultConfig(Config):
    """
    Default configuration. Takes values from enviroment variable `FLASK_ENV`.
    """
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    TESTING = os.environ.get('FLASK_ENV') == 'testing'

class ProductionConfig(Config):
    """
    Production environment configuration.
    """
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Testing environment configuration.
    """
    TESTING = True
