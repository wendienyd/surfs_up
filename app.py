# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

# Dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Dependency for Flask.
from flask import Flask, jsonify

# Setup a database engine.
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variable for each class to reference later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link.
session = Session(engine)

# Create and define a Flask application.
app = Flask(__name__)

# Define the welcome route.
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<Br>
    Available Routes:<Br>
    /api/v1.0/precipitation<Br>
    /api/v1.0/stations<Br>
    /api/v1.0/tobs<Br>
    /api/v1.0/temp/start/end<Br>
    ''')

# Create route.
@app.route("/api/v1.0/precipitation")

# Create precipitation() function.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Add route.
@app.route("/api/v1.0/stations")
def stations():
   results = session.query(Station.station).all()
   stations = list(np.ravel(results))
   return

# Create route.
@app.route("/api/v1.0/tobs")
def temp_monthly():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
   temps = list(np.ravel(results))
   return jsonify(temps=temps)

# Route start & end.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
   sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
   

   if not end:
      results = session.query(*sel).\
         filter(Measurement.date >= start).all()
      temps = list(np.ravel(results))
      return jsonify(temps=temps)

   results = session.query(*sel).\
      filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all()
   temps = list(np.ravel(results))
   return jsonify(temps)

if __name__=='__main__':
   app.run()