#!/usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DefaultConfig

app = Flask(__name__)
cfg = DefaultConfig()    

app.config.from_object(cfg)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


import models
import routes


if __name__ == '__main__':
    app.run()