from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from server.config import DefaultConfig

import os


app = Flask(__name__)
cfg = DefaultConfig()    

app.config.from_object(cfg)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


import server.models
import server.routes


if __name__ == '__main__':
    app.run()