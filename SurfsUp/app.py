# Import the dependencies for Flask
from flask import Flask, jsonify, request, render_template_string

# import dependencies for SQLAcademy, Counter, Pandas, and Datetime to calculate data
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func
from datetime import datetime, timedelta
import json
from collections import Counter
import pandas as pd
import statistics

#################################################
# Database Setup
#################################################

#  Create engine using the `hawaii.sqlite` database file from the Resources folder
engine = create_engine("sqlite:///C:/Users/thegr/Documents/UT Boot Camp/Assignments/Module 10 Assignment - SQLAlchemy/SurfsUp/Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create the session (link) from Python to the database
session = Session(engine)

# Query to get the most recent date in the dataset
most_recent_date = session.query(func.max(Measurement.date)).scalar()

# Convert the date from string format to datetime object (if it's in string format)
most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')

# Calculate the date 12 months prior to most recent date
twelve_months_ago = most_recent_date - timedelta(days=365)

# set the precipitation data database object
# return only the most recent 12 months of data
precipitation_data = (
    session.query(Measurement.date, Measurement.prcp)
    .filter(Measurement.date >= twelve_months_ago)
    .order_by(Measurement.date)
    .all()
)

# returns jsonified data of all the stations in the database
stations_data = session.query(Measurement.station).all()
unique_stations_data = session.query(Measurement.station).distinct().all()

# Convert the query results to a dictionary with date as the key and precipitation as the value
precipitation_dict = {date: prcp for date, prcp in precipitation_data}

# use list comprehension to store only the unique names of the stations
unique_stations_list = [station[0] for station in unique_stations_data]

# capture the total number of rows of measurements for each station
station_counts = Counter([station[0] for station in stations_data]).most_common()

# capture the most active station ID from the previous query into a variable
most_active_station_id = station_counts[0][0]

# Using this most active station ID, run another query to capture the last 12
# months of data for this station only
most_active_station_data = (
    session.query(Measurement.date, Measurement.tobs)
    .filter(Measurement.station == most_active_station_id)
    .filter(Measurement.date >= twelve_months_ago)
    .order_by(Measurement.date)
    .all()
)

# also capture all-time temperature data to be used later for user date input
most_active_station_data_all = (
    session.query(Measurement.date, Measurement.tobs)
    .filter(Measurement.station == most_active_station_id)
    .order_by(Measurement.date)
    .all()
)

# turn the above query results into a dictionary for properly displaying it in flask
most_active_station_data_dict = {date: tobs for date, tobs in most_active_station_data}
most_active_station_data_all_dict = {date: tobs for date, tobs in most_active_station_data_all}

# Close the session after the query
session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# welcome message on the home page of the API
@app.route("/")
def welcome():
    return (
        f"<html>"
        f"<head>"
        f"<style>"
        f"  h1 {{ font-family: Arial, sans-serif; }}" 
        f"  table {{ width: 100%; border-collapse: collapse; }}"  
        f"  th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}"  
        f"  tr:nth-child(even) {{ background-color: #f2f2f2; }}" 
        f"  tr:nth-child(odd) {{ background-color: #ffffff; }}" 
        f"  .button {{ display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #4CAF50; border: none; border-radius: 5px; text-align: center; text-decoration: none; margin: 5px; cursor: pointer; }}"
        f"</style>"
        f"</head>"
        f"<body>"

        # Main title and image of Hawaii
        f"<h1 style='font-size: 25px; color: green;'>Hawaii Precipitation and Temperature Measurement API</h1><br/>"
        f"<img src='https://statesymbolsusa.org/sites/default/files/primary-images/stateofHawaiimap.jpg' alt='Hawaii' style='width:300px;height:auto;'/><br/>"
        f"<h1 style='font-size: 18px'><u>Available Routes:</u></h1>"

        # Table with buttons to navigate to each route
        f"<table>"
        
        # Table header
        f"<tr style='background-color: #d3d3d3;'><th style='font-size: 18px;'>Route</th><th style='font-size: 18px;'>Description</th><th style='font-size: 18px;'>Direct Links to Route</th></tr>"
        
        # Rows to show each route name, a description of of each route, and a button linked directly to each route
        # precipitation route
        f"<tr><td style='font-size: 18px;'>/precipitation</td>"
        f"<td style='font-size: 18px;'>The last 12 months of recorded precipitation values organized in ascending order by date</td>"
        f"<td><a href='/precipitation' class='button'>Go to route</a></td></tr>"

        # stations route
        f"<tr><td style='font-size: 18px;'>/stations</td>"
        f"<td style='font-size: 18px;'>The list of stations in the dataset and how many readings each station has in descending order</td>"
        f"<td><a href='/stations' class='button'>Go to route</a></td></tr>"

        # tobs (temperature) route
        f"<tr><td style='font-size: 18px;'>/tobs</td>"
        f"<td style='font-size: 18px;'>The temperature measurement data for the most active station for the last 12 months</td>"
        f"<td><a href='/tobs' class='button'>Go to route</a></td></tr>"
    
        # start route taking a user input for a start date 
        f"<tr><td style='font-size: 18px;'>/start/YYYY-MM-DD</td>"
        f"<td style='font-size: 18px;'>Returns the minimum, maximum, and average temperatures from that inputted date at the end of the API route URL to present</td>"
        f"<td>Type a start date on the end of the route URL in your browser URL bar in the format:  YYYY-MM-DD"
        #f"<td><a href='/tobs' class='button'>Go to route</a></td></tr>"

        # tobs (temperature) route
        f"<tr><td style='font-size: 18px;'>/start/end/YYYY-MM-DD/YYYY-MM-DD</td>"
        f"<td style='font-size: 18px;'>Returns the minimum, maximum, and average temperatures from that inputted start date to the inputted end date at the end of the API URL to present</td>"
        f"<td>Type a start date/end date on the end of the API route URL in your browser URL bar in the format:  YYYY-MM-DD/YYYY-MM-DD"
        #f"<td><a href='/tobs' class='button'>Go to route</a></td></tr>"
        f"</table>"
        
        f"</body>"
        f"</html>"
    )

@app.route("/precipitation")
def precipitation():    
    return jsonify(precipitation_dict)

@app.route("/stations")
def stations():
    return jsonify(station_counts)

@app.route("/tobs")
def tobs():
    return jsonify(most_active_station_data_dict)

@app.route("/start/<start_date>", methods=["GET"])
def start(start_date):
    try:
        # Convert the `start_date` from string to a datetime object
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        # Call the tobs_start_date to handle the data from the start_date type in by the user
        return tobs_start_date(start_date)
    except ValueError:
        # If the date format is incorrect, return an error message
        return "Invalid date format. Please use YYYY-MM-DD."

# create a method to use user-inputted start date at the end of the URL to capture tobs date from that inputted date
# to present
def tobs_start_date(start_date):
    tobs_start_date_dict = {date: tobs for date, tobs in most_active_station_data_all_dict.items() 
                            if datetime.strptime(date, '%Y-%m-%d') >= start_date}
    tobs_results = list(tobs_start_date_dict.values())
    tobs_min = min(tobs_results)
    tobs_max = max(tobs_results)
    tobs_avg = statistics.mean(tobs_results)

    tobs_results_dict = {
        "total_data": tobs_start_date_dict,
        "min_temp": tobs_min,
        "max_temp": tobs_max,
        "avg_temp": tobs_avg
    }

    return jsonify(tobs_results_dict)


@app.route("/start/end/<start_date>/<end_date>", methods=["GET"])
def start_end(start_date, end_date):
    try:
        # Convert the `start_date` and `end_date` from strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Call a function to handle data between the specified dates
        return tobs_start_end_dates(start_date, end_date)
    except ValueError:
        # If the date format is incorrect, return an error message
        return "Invalid date format. Please use YYYY-MM-DD/YYYY-MM-DD."

# Method to handle the filtered data between start and end dates
def tobs_start_end_dates(start_date, end_date):
    tobs_start_end_dict = {
        date: tobs for date, tobs in most_active_station_data_all_dict.items()
        if start_date <= datetime.strptime(date, '%Y-%m-%d') <= end_date
    }

    tobs_results = list(tobs_start_end_dict.values())
    tobs_min = min(tobs_results)
    tobs_max = max(tobs_results)
    tobs_avg = statistics.mean(tobs_results)

    tobs_results_dict = {
        "total_data": tobs_start_end_dict,
        "min_temp": tobs_min,
        "max_temp": tobs_max,
        "avg_temp": tobs_avg
    }    

    return jsonify(tobs_results_dict)

if __name__ == "__main__":
    app.run(debug=False)