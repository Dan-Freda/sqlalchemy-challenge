# Import Dependencies 

import numpy as np 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert and query the results to a dictionary using 'date as the key and 'prcp' as the value.
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_prior).all()
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of most active station for last year of data.
    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date >= one_year_prior).\
                    filter(Measurement.station == 'USC00519281').all()
    tobs_list = list(np.ravel(tobs_results))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    group_by(Measurement.date).all()
    start_date_list = list(start_date)
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start_end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).\
                        group_by(Measurement.date).all()
    start_end_date_list = list(start_end_date)
    return jsonify(start_end_date_list)
    
    
if __name__ == '__main__':
    app.run(debug=True)