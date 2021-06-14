from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig, StagingConfig

import os


if os.environ.get('ENVIRONMENT') == 'production':
    cfg = ProductionConfig()
    
elif os.environ.get('ENVIRONMENT') == 'staging':
    cfg = StagingConfig()

else:
    cfg = DevelopmentConfig()

    
app = Flask(__name__)

app.config.from_object(cfg)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import Result
from routes import *


if __name__ == '__main__':
    app.run()