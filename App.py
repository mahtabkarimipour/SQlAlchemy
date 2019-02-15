from flask import Flask
from flask import jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import text

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def index():
    res = {}
    myapp_urls = str(app.url_map).split('\n')
    for i, u in enumerate(myapp_urls):
        print(i, u)    
    return jsonify(res)
    
@app.route('/api/v1.0/precipitation',)
def get_precipitation():
    res = {}
    records = session.query(Measurement)
    for r in records:
        res[r.date] = r.prcp
    return jsonify(res)

@app.route('/api/v1.0/stations')
def get_stations():
    res = []
    records = session.query(Station)
    for r in records:
        tmp = {}
        tmp['station'] = r.station
        tmp['name'] = r.name
        tmp['latitude'] = r.latitude
        tmp['longitude'] = r.longitude
        tmp['elevation'] = r.elevation
        res.append(tmp)
    return jsonify(res)

@app.route('/api/v1.0/tobs')
def get_tobs():
    res = {}
    records = session.query(Measurement).filter(text("date > '2016-08-23'")).all()
    res['Temparature'] = []
    for r in records:
        res['Temparature'].append(r.tobs)
    return jsonify(res)

@app.route('/api/v1.0/<start>')
def get_temp_data_day(start):
    res = {}
    print(start)
    t = "'" + start + "'"
    t = "date = " + t
    res['Start'] = start
    records = session.query(func.min(Measurement.tobs).label('min'), func.max(Measurement.tobs).label('max'), func.avg(Measurement.tobs).label('avg')).filter(text(t)).all()
    for r in records:
        res['TMIN'] = r.min
        res['TMAX'] = r.max
        res['TAVG'] = r.avg
    return jsonify(res)

@app.route('/api/v1.0/<start>/<end>')
def get_temp_data_interval(start, end):
    res = {}
    print(start)
    t1 = "'" + start + "'"
    t1 = "date > " + t1
    t2 = "'" + end + "'"
    t2 = "date < " + t2
    res['Start'] = start
    res['End'] = end
    records = session.query(func.min(Measurement.tobs).label('min'), func.max(Measurement.tobs).label('max'), func.avg(Measurement.tobs).label('avg')).filter(text(t1)).filter(text(t2)).all()
    for r in records:
        res['TMIN'] = r.min
        res['TMAX'] = r.max
        res['TAVG'] = r.avg
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)