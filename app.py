import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask,jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return """
        Welcome to the Hawaii Weather API!<br/>
        Available Routes:<br/>
       <a href= '/api/v1.0/precipitation' target="_blank">Precipitation</a><br/>
       <a href= '/api/v1.0/stations'target="_blank">Stations</a><br/>
       <a href= '/api/v1.0/tobs'target="_blank">Temperature Observed</a><br/><br/>
       From Date:<input type='text' id='startdate' value='2016-01-01'><a href = "javascript:;" onclick = "this.href='/api/v1.0/' + document.getElementById('startdate').value"target="_blank">SummaryByStartDate</a><br/><br/>
       From Date:<input type='text' id='startenddate1' value='2016-01-01'> End Date:<input type='text' id='startenddate2' value='2017-01-01'><a href = "javascript:;" onclick = "this.href='/api/v1.0/' + document.getElementById('startenddate1').value+'/'+ document.getElementById('startenddate2').value"target="_blank">SummaryByStartDate_EndDate</a><br/>
   """

@app.route("/api/v1.0/<start>")
def summary_startdate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    data = session.query(*sel).filter(Measurement.date >= start)
    
    session.close()

    all_val = []
    for TMIN, TAVG,TMAX in data:
        temp_dict = {}
        temp_dict["TMIN"] = TMIN
        temp_dict["TAVG"] = TAVG
        temp_dict["TMAX"] = TMAX
        all_val.append(temp_dict)

    return jsonify(all_val)


@app.route("/api/v1.0/<start>/<end>")
def summary_startenddate(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    data = session.query(*sel).filter(Measurement.date >= start,Measurement.date <= end)
    
    session.close()

    all_val = []
    for TMIN, TAVG,TMAX in data:
        temp_dict = {}
        temp_dict["TMIN"] = TMIN
        temp_dict["TAVG"] = TAVG
        temp_dict["TMAX"] = TMAX
        all_val.append(temp_dict)

    return jsonify(all_val)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation

    data = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    all_prcp_val = []
    for date, prcp in data:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp_val.append(prcp_dict)

    return jsonify(all_prcp_val)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation

    station_data = session.query(Measurement.station).all()
    session.close()
    data = list(np.ravel(station_data))
    return jsonify(data)


@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation
    date_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latestdate = dt.datetime.strptime(date_recent[0], '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, 1, 1)
    
    sel = [Measurement.station,func.count(Measurement.id),Measurement.date,Measurement.tobs]
    act_station_temp = session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
    
    sel = [Measurement.tobs]
    temp_data = session.query(*sel).filter(Measurement.station==act_station_temp[0],Measurement.date >= querydate).all()
    
    session.close()
    

    data = list(np.ravel(temp_data))
    return jsonify(data)









if __name__ == "__main__":
    app.run(debug=True)