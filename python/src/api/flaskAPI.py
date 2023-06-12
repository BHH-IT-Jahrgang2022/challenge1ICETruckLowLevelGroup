from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import sqlite3
import json
import jsonify
from dataclasses import dataclass
from marshmallow import Schema, fields, post_load


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home//lazaro/test.db"
# initialize the app with the extension
db.init_app(app)

#to_json Methode: 
def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to convert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

class postSchema(Schema):
    zeitpunkt = fields.Int()
    sensor = fields.Str()
    temperatur = fields.Float()

    @post_load
    def make_post(self, data, **kwargs):
        return Temperature(**data)

# Create database with its table and columns
@dataclass
class Temperature(db.Model):

    __tablename__ = "data"

    zeitpunkt:int = db.Column(db.INTEGER , primary_key=True)
    sensor:str = db.Column(db.VARCHAR(20))  
    temperatur:float = db.Column(db.FLOAT)

    @property
    def json(self):
        return to_json(self, self.__class__)

    def __init__(self, zeitpunkt, sensor, temperatur):
        self.zeitpunkt = zeitpunkt
        self.sensor = sensor
        self.temperatur = temperatur

#class temperatureSchema(ma.Schema):
 #   class Meta:
    #Fields to expose
  #      fields = ("zeitpunkt", "sensor", "temperatur")

with app.app_context():
    db.drop_all()
    db.create_all()

# Endpoint

@app.route("/test")

def Hello():
    return "Hello World"

# Request Send-JSON

@app.route('/json_test', methods=['POST'])
def handle_json():
    #data = json.loads(request.json)
    data = request.json
    #print(data)
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

# Request Get-JSON
@app.route("/get_json", methods=['GET'])
def get_json():
    all_posts = Temperature.query.all()
    #all_posts = db.session.execute(select(Temperature)).first()[0]
    
    result = {}
    index = 0
    for temp in all_posts:
        result[index] = temp.json
        index += 1
    print(result)
    #all_posts = db.session.execute(select(Temperature).order_by(Temperature.zeitpunkt)).scalars()
    print(all_posts)
    #schema = postSchema(many=True)
    #result = schema.dump(all_posts)
    if all_posts == None:
        return jsonify({}), 404
    return json.dumps(result)
