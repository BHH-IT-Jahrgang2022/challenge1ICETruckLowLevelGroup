from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, TIMESTAMP, FLOAT, VARCHAR
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text
import sqlite3
import time

engine = create_engine('sqlite:////home//void/test.db', pool_pre_ping= True)

class Base(DeclarativeBase):
    pass


class Temperature(Base):

    __tablename__ = "data"

    zeitpunkt = Column(TIMESTAMP , primary_key=True)
    sensor = Column(VARCHAR(20))  
    temperatur = Column(FLOAT)

    def __init__(self, sensor, temperatur):
        self.zeitpunkt = time.time()
        self.sensor = sensor
        self.temperatur = temperatur    


Base.metadata.create_all(engine)
'''
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)

username = 'root'
password = 'root'

# change string to the name of your database; add path if necessary
db_name = 'test.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

"""
    test a SQLite database connection locally
    assumes the database file is in same location
    as this .py file
"""



# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# change string to the name of your database; add path if necessary
db_name = 'sockmarket.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)


# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection - and nothing more
@app.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)
'''