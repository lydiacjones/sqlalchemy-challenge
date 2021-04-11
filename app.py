#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
#Use Flask to create your routes.

import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Init flask
app = Flask(__name__)


#ROUTES:

#/
#Make home page.
#List all routes that are available.
@app.route("/")
def welcome():
    return (
        f"Welcome to the SQL-Alchemy Hawaiian Climate API!<br/>"
        f"<br/>"
        f"Add the following to the end of the URL in order to view datasets.<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"Precipitation:      /api/v1.0/precipitation<br/>"
        f"Stations:           /api/v1.0/stations<br/>"
        f"Temperatures:       /api/v1.0/tobs<br/>"
        f"Date:               /api/v1.0/[yyyy-mm-dd]<br/>"
        f"Date Range ([start]/[end]):   /api/v1.0/[yyyy-mm-dd]/[yyyy-mm-dd]<br/>"
    )


#/api/v1.0/precipitation
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()

    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp    
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


#/api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


#/api/v1.0/tobs
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


#/api/v1.0/<start> 
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def get_t_start(start):
    session = Session(engine)

    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)



#/api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def get_t_start_stop(start,end):
    session = Session(engine)

    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


if __name__ == "__main__":
    app.run(debug=True)