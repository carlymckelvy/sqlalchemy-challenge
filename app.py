import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).\
                      order_by(Measurement.date).all()

  
    session.close()

    # Convert list of tuples into normal list
    all_results = []
    for row in data:
        data_dict = {}
        data_dict["date"] = row[0]
        data_dict["precicipation"] = row[1]
        all_results.append(data_dict)

    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    sel = [Measurement.station, func.count(Measurement.id)]
    most_active = session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()


    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(most_active))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(Measurement.tobs).filter(Measurement.date > year_ago).\
                      filter(Measurement.station == 'USC00519281').all()

  
    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(data))

    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>")
def calc_temps_start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
  
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()


    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(start_results))

    return jsonify(all_results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    startend_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(startend_results))

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)