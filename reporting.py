# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

import pandas as pd
import numpy as np

import datetime as dt

VALID_MONITORING_STATIONS = ["HRL", "MY1", "KC1"]
VALID_POLLUTANT_TYPES = ["no", "pm10", "pm25"]

def get_data_from_csv(file_name):
    """Returns a numpy array containing the data from the csv file"""
    # Uses pandas library to read the csv file into a pandas DataFrame
    data = pd.read_csv(file_name)
    
    # Convert date format to a better format for pandas
    data["date"] = pd.to_datetime(data["date"], format='%Y-%m-%d')
    
    return data

def get_monitering_station_data():
    """Returns a pandas DataFrame containing all the data from all 3 monitering stations"""
    HRLdata = get_data_from_csv("data/Pollution-London Harlington.csv")
    MY1data = get_data_from_csv("data/Pollution-London Marylebone Road.csv")
    KC1data = get_data_from_csv("data/Pollution-London N Kensington.csv")

    stations_data = {"HRL":HRLdata, "MY1":MY1data, "KC1":KC1data}
    return stations_data

def get_inital_date(data, monitoring_station):
    """Returns the first date for the specific monitoring station as a DateTime object"""
    data = data[monitoring_station]
    return data["date"].at[0]

def get_date_index(data, monitoring_station, date):
    """Returns the numerical position of the date in the monitoring station data sheet in days (integer)"""
    return (dt.datetime.strptime(date, "%Y-%m-%d") - get_inital_date(data, monitoring_station)).days

def daily_average(data, monitoring_station, pollutant):
    """Returns the mean pollutant concentration for each day for the specified monitoring station.
    If there is no data avaliable, the mean will be 'nan'"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    # Remove missing data, so it does not alter the mean (pandas.groupby automatically removes 'nan' values)
    data = fill_missing_data(data, np.nan, monitoring_station, pollutant)
    data = data[monitoring_station]
    
    # Convert data from string to float to calculate mean
    data[pollutant] = data[pollutant].astype(float)
    
    # Group the data by date
    data = data.groupby(["date"])[pollutant]
    # Use pandas for mean
    mean = data.mean()
    return mean.to_numpy()

def daily_median(data, monitoring_station, pollutant):
    """Returns the median pollutant concentration for each day for the specified monitoring station.
    If there is no data avaliable, the mean will be 'nan'"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    # Remove missing data, so it does not alter the mean (pandas.groupby automatically removes 'nan' values)
    data = fill_missing_data(data, np.nan, monitoring_station, pollutant)
    data = data[monitoring_station]
    
    # Convert data from string to float to calculate mean
    data[pollutant] = data[pollutant].astype(float)
    
    # Group the data by date
    data = data.groupby(["date"])[pollutant]
    # Use pandas for median
    median = data.median()
    return median.to_numpy()

def hourly_average(data, monitoring_station, pollutant):
    """Returns the mean value for pollutant concentration for each hour (24 hours) for the specified monitoring station.
    If there is no data avaliable, the mean will be 'nan'"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    # Remove missing data, so it does not alter the mean (pandas.groupby automatically removes 'nan' values)
    data = fill_missing_data(data, np.nan, monitoring_station, pollutant)
    data = data[monitoring_station]
    
    # Convert data from string to float to calculate mean
    data[pollutant] = data[pollutant].astype(float)
    
    # Group the data by hour
    data = data.groupby(["time"])[pollutant]
    # Use pandas for mean
    mean = data.mean()
    return mean.to_numpy()

def monthly_average(data, monitoring_station, pollutant):
    """Returns the mean value for pollutant concentration for each month for the specified monitoring station.
    If there is no data avaliable, the mean will be 'nan'"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    # Remove missing data, so it does not alter the mean (pandas.groupby automatically removes 'nan' values)
    data = fill_missing_data(data, np.nan, monitoring_station, pollutant)
    data = data[monitoring_station]
    
    # Convert data from string to float to calculate mean
    data[pollutant] = data[pollutant].astype(float)
    
    # Group the data by month
    data = data.groupby(pd.Grouper(key="date", freq="M"))[pollutant]
    # Use pandas for mean
    mean = data.mean()
    return mean.to_numpy()

def peak_hour_date(data, date, monitoring_station,pollutant):
    """Returns the peak pollution and the hour that pollution was reached for a specific date, monitoring station and pollutant.
    If all the data for the specific date and pollutant are missing, this function will return None
    """
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    date = dt.datetime.strptime(date, "%Y-%m-%d")
    
    # Remove missing data, so data can safely be converted to a float
    data = fill_missing_data(data, -1, monitoring_station, pollutant)
    # Shadow data with data from relavent monitering station
    data = data[monitoring_station]
    # Filter data by the specific date
    data = data.loc[data["date"] == date]
    
    # First convert type from string to float, so max gives the numerical maximum
    max_index = data[pollutant].astype(float).idxmax()
    max_value = data[pollutant].at[max_index]
    max_time = data["time"].at[max_index]
    # Cut off the last 2 digits as the specification requires (removes the ':00' at the end of the hour)
    max_time = max_time[:-3]
    
    # Check if all the value is missing
    if max_value == -1:
        return None
    
    return (max_time, max_value)

def count_missing_data(data, monitoring_station, pollutant):
    """Returns the count of 'No data' items for a specific station and pollutant"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    data = data[monitoring_station]
    # Find all occourences of "No data" for the specific pollutant
    data = data.loc[data[pollutant] == "No data", pollutant]
    return data.count()

def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """Takes the monitoring station datasheet, the monitoring station code, the pollutant code and a replacement value and returns the datasheet
    with the missing data replaced by the new value"""
    # Check that monitoring stations and pollutants are valid
    if not monitoring_station in VALID_MONITORING_STATIONS:
        raise Exception("Monitoring station type is not valid!")
    if not pollutant in VALID_POLLUTANT_TYPES:
        raise Exception("Pollutant type is not valid!")
    
    sdata = data[monitoring_station]
    sdata.loc[sdata[pollutant] == "No data", pollutant] = new_value
    return data