from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from . import routes, models

# Set up logging
routes.init_logging(app)
app.logger.info("Product Service running...")
