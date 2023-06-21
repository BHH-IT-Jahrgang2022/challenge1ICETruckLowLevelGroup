from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import sqlite3
import json
from dataclasses import dataclass



# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./test.db"
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


# Create database with its table and columns
@dataclass
class Temperature(db.Model):

    __tablename__ = "data"

    zeitpunkt:int = db.Column(db.BIGINT , primary_key=True)
    sensor_id:int = db.Column(db.INT)
    sensor_name:str = db.Column(db.VARCHAR(20))  
    temperatur:float = db.Column(db.FLOAT)

    @property
    def json(self):
        return to_json(self, self.__class__)

    def __init__(self, zeitpunkt, sensor_id, sensor_name, temperatur):
        self.zeitpunkt = zeitpunkt
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.temperatur = temperatur



with app.app_context():
    db.drop_all()
    db.create_all()


# Endpoint

@app.route("/", methods=['GET'])

def Hello():
    return "Help, I'm alive...", 200

# Request Send-JSON

@app.route('/json_input', methods=['POST'])
def handle_json():
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
    return_code = 200
    return_message = "Success!"
    try:
        all_posts = Temperature.query.all()
    
    except Exception as e:
        return_code = 400
        return_message = str(e)
        all_posts = []
    
    finally:
        return jsonify(all_posts), return_code

# Query all data of one sensor
@app.route("/get_sensor/<sensor_nr>", methods=['GET'])
def get_sensor(sensor_nr):
    return_code = 200
    return_message = "Success!"
    try:
        allposts_one_sensor = db.session.query(Temperature).filter(Temperature.sensor_id == sensor_nr)
    
    except Exception as e:
        return_code = 400
        return_message = str(e)
        allposts_one_sensor = []
    
    finally:
        return jsonify(allposts_one_sensor), return_code
    

# Query for a timeintervall
@app.route("/get_intervall")
def request_intervall():
    requestParam = request.json
    return_code = 200
    return_message = "Success!"
    try:
        if requestParam["SensorId"] == "":
            if requestParam["TimeBegin"] != "" and requestParam["TimeEnd"] != "":
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt >= requestParam["TimeBegin"], Temperature.zeitpunkt <= requestParam["TimeEnd"])
            elif requestParam["TimeBegin"] == "":
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt <= requestParam["TimeEnd"])
            else:
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt >= requestParam["TimeBegin"])

        else:
            if requestParam["TimeBegin"] != "" and requestParam["TimeEnd"] != "":
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt >= requestParam["TimeBegin"], Temperature.zeitpunkt <= requestParam["TimeEnd"], Temperature.sensor_id == requestParam["SensorId"])
            elif requestParam["TimeBegin"] == "":
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt <= requestParam["TimeEnd"], Temperature.sensor_id == requestParam["SensorId"])
            else:
                query_result = db.session.query(Temperature).filter(Temperature.zeitpunkt >= requestParam["TimeBegin"], Temperature.sensor_id == requestParam["SensorId"])
    except Exception as e:
        return_code = 400
        return_message = str(e)
        query_result = []
    finally:
        return jsonify(query_result), return_code

