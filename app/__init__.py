from flask import Flask
from config import Config, PopulateDBConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if app.config["ENV"] == "populate":
    from app.populate_db import populate
    app.config.from_object(PopulateDBConfig)
    populate()


# from app import routes, models
from app import models