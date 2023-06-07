from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home//void/test.db"
# initialize the app with the extension
db.init_app(app)

class Temperature(db.Model):

    __tablename__ = "data"

    zeitpunkt = db.Column(db.TIMESTAMP , primary_key=True)
    sensor = db.Column(db.VARCHAR(20))  
    temperatur = db.Column(db.FLOAT)

    def __init__(self, sensor, temperatur):
        self.zeitpunkt = db.time.time()
        self.sensor = sensor
        self.temperatur = temperatur

with app.app_context():
    db.create_all()