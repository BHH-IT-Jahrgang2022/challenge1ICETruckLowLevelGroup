from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json
import jsonify
from dataclasses import dataclass

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home//lazaro/test.db"
# initialize the app with the extension
db.init_app(app)

# Create database with its table and columns
@dataclass
class Temperature(db.Model):

    __tablename__ = "data"

    zeitpunkt:int = db.Column(db.INTEGER , primary_key=True)
    sensor:str = db.Column(db.VARCHAR(20))  
    temperatur:float = db.Column(db.FLOAT)

    def __init__(self, zeitpunkt, sensor, temperatur):
        self.zeitpunkt = zeitpunkt
        self.sensor = sensor
        self.temperatur = temperatur

with app.app_context():
    db.drop_all()
    db.create_all()

# Endpoint

@app.route("/test")

def Hello():
    return "Hello World"

# Request JSON

@app.route('/json_test', methods=['POST'])
def handle_json():
    #data = json.loads(request.json)
    data = request.json
    print(data)
    return_code = 200
    return_message = "Saved succesfully"
    try:
        post = Temperature(**data)
        db.session.add(post)
        db.session.commit()

    except Exception as e:
        return_code = 400
        return_message = str(e)

    finally:
        return return_message, return_code   

@app.route("/get_json", methods=['GET'])
def get_json():
    all_posts = Temperature.query().all()
    print(all_posts)
    if all_posts == None:
        return jsonify({}), 404
    return jsonify(all_posts)