# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#

import datetime as dt
import re
import calendar

import pandas as pd
import numpy as np

import utils

def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date if end_date is None else end_date
    end_date += datetime.timedelta(days=1)
    
    period = None
    units = None
    step = None

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()



def get_valid_date():
    """Uses ReGex to prompt the user to enter a date in YYYY-MM-DD format and loops until they enter a date in this format

    Returns:
        str: a string date in the form YYYY-MM-DD
    """
    is_input_valid = False
    
    while not is_input_valid:
        print("Please enter a date (YYYY-MM-DD):")
        user_date = input()
        # Check if date is in the YYYY-MM-DD format
        if re.match("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", user_date):
            date = dt.datetime.strptime(user_date, "%Y-%m-%d")
            if date > dt.datetime.today():
                print("Date is in the future! Please choose an earlier date")
            else:
                is_input_valid = True
        else:
            print("Date format is invalid. Please enter a date in the (YYYY-MM-DD) format")
    # Return the string date as that is what the specification requires for the functions
    return user_date

def convert_response_to_dataframe(response_data) -> pd.DataFrame:
    """Converts data from the requests library into a pandas datasheet

    Args:
        response_data (response): the raw response data as json

    Returns:
        pd.DataFrame: A dataframe containing a datetime column and a pollution column
    """
    data_frame = pd.DataFrame(response_data["RawAQData"]["Data"])
    
    # Rename the columns so they are less verbose
    data_frame.rename(columns = {"@MeasurementDateGMT" : "date", "@Value" : "value"}, inplace=True)
    
    # Convert the types for easy processing
    data_frame["date"] = pd.to_datetime(data_frame["date"])
    data_frame["value"] = pd.to_numeric(data_frame["value"])
    
    return data_frame

def group_data(data: pd.DataFrame, data_grouping):
    """Groups the data according to the data_grouping

    Args:
        data (pd.DataFrame): The input dataframe which should consist of two colums: 'date' and 'values'
        data_grouping (str): How the data will be grouped. Can be 'none', 'day', 'time', 'month', or 'year'

    Returns:
        Pandas Group Object: The grouped data
    """
    freq_dict = {"none" : None, "day": "D", "time" : "H", "month" : "M", "year" : "Y"}
    freq = freq_dict[data_grouping]

    if data_grouping == "none":
        # Do not group data
        data_group = data.groupby(data["date"])
    elif data_grouping == "day":
        data_group = data.groupby(data["date"].dt.day)
    elif data_grouping == "time":
        data_group = data.groupby(data["date"].dt.day_of_week)
    elif data_grouping == "month":
        data_group = data.groupby(data["date"].dt.month)
    elif data_grouping == "year":
        data_group = data.groupby(data["date"].dt.year)

    data = data_group["value"]
    return data

def display_monitoring_data(raw_data, data_grouping, monitoring_station, pollutant, start_date, end_date, scale_max, display_settings):
    """Displays all the currently active data displays using the supplied data

    Args:
        raw_data (reponse): The raw json data fetched from the API
        data_grouping (str): A enum like string which describes how the data will be grouped
        monitoring_station (str): The  monitoring station code
        pollutant (str): The pollutant code
        start_date (datetime): The earliest date in the data
        end_date (datetime): The latest date in the data
        scale_max (int): The maximum value shown in barcharts
        display_settings ([str]): Specifies which data displays will be shown
    """
    utils.clear_screen()
    
    print(f"Monitoring station: {monitoring_station}. Pollutant: {pollutant}. Date: {start_date} - {end_date}")
    
    data = convert_response_to_dataframe(raw_data)
    data_group = group_data(data, data_grouping)
    
    # Data for ranges
    if "mean_range" in display_settings:
        show_data_mean(data)
    if "median_range" in display_settings:
        show_data_median(data)
    if "max_range" in display_settings:
        show_data_max(data)
    if "min_range" in display_settings:
        show_data_min(data)
    # Data for groups
    if "mean_group" in display_settings:
        show_data_mean(data_group)
    if "median_group" in display_settings:
        show_data_median(data_group)
    # Visulisations
    if "barchart" in display_settings:
        show_data_as_barchart(data_group.mean(), data_grouping, scale_max)
    if "table" in display_settings:
        show_data_as_table(data_group, data_grouping)

def show_data_as_table(data: pd.DataFrame, data_grouping):
    """Displays the data in a table format

    Args:
        data (pd.DataFrame): The data that will be displayed
        data_grouping (_type_): How the data will be grouped
    """
    MAX_DATA = 16
    
    # Make dates more readable
    if data_grouping == "none":
        date_converter = lambda date: date.hour + 1
    elif data_grouping == "day":
        date_converter = lambda date: date
    elif data_grouping == "time":
        date_converter = lambda date: calendar.day_abbr[date % 7]
    elif data_grouping == "month":
        date_converter = lambda date: calendar.month_abbr[date % 13]
    elif data_grouping == "year":
        date_converter = lambda date: date
    
    for group in data:
        date = group[0]
        pollution_data = group[1].values
        
        date = date_converter(date)
        
        # Display the date with padding
        print(str(date).ljust(21), end="")
        
        # Get all the data, until the console runs out of column space
        for value in pollution_data[:MAX_DATA]:
            value = round(value, 1)
            # Print value with spacing so values are aligned
            print(str(value).ljust(7), end="")
        # If there is too much data to show, show ellipses
        if len(pollution_data) > MAX_DATA:
            print("...", end="")
        print()

def show_data_as_barchart(data: pd.DataFrame, data_grouping, scale_max):  
    """Displays the data in a barchart format

    Args:
        data (pd.DataFrame): The data that will be displayed
        data_grouping (_type_): How the data will be grouped
        scale_max (_type_): The maximum value that will be displayed on the chart
    """
    step = scale_max // 20
    MAX_DATA = 48
    
    # Console will only show around 48 columns of data
    data_count = data.shape[0]
    if data_count > MAX_DATA:
        print("Too much data to show! Only showing the first 48 values!")
        data_count = MAX_DATA
    width = data_count * 3
    
    print("   ^")
    for i in range(scale_max, 0, -step):
        # Print index
        print(str(i).rjust(3) + "|", end="")
        # Print bar if data is high enough
        j = 0
        # Only print values upto the maximum width
        for value in data[:MAX_DATA]:
            if np.isnan(value) and i == step:
                print("NaN", end="")
            elif value > scale_max and i == scale_max:
                # Value is off the scale
                print("!#!", end="")
            elif value - i > 0:
                print(" # ", end="")
            else:
                print("   ", end="")
        print()
     
    # Print hours   
    print("---+" + "".rjust(width - 1, "-"), end="")
    print(">")
    print("   |", end="")
    for i in range(min(data_count, MAX_DATA)):
        print(str(i % data_count).ljust(3), end="")
    print()
    print(("Grouping: " + data_grouping).rjust(width // 2))

def show_data_mean(data: pd.DataFrame):
    """Computes the mean of the data for a dataframe

    Args:
        data (pd.DataFrame or Group): The data which will be used for computation
    """
    if type(data) == pd.DataFrame:
        mean = data.mean(numeric_only=True).value
    else:
        mean = data.mean().mean()
    if np.isnan(mean):
        print("There is no mean    value as there is no data")
    else:
        mean = round(mean, 2)
        print(f"The mean   for the date range is: {mean}")

def show_data_median(data: pd.DataFrame):
    """Computes the median of the data for a dataframe

    Args:
        data (pd.DataFrame or Group): The data which will be used for computation
    """
    if type(data) == pd.DataFrame:
        median = data.median(numeric_only=True).value
    else:
        median = data.median().median()
    if np.isnan(median):
        print("There is no median  value as there is no data")
    else:
        median = round(median, 2)
        print(f"The median for the date range is: {median}")

def show_data_max(data: pd.DataFrame):
    """Computes the maximum of the data for a dataframe

    Args:
        data (pd.DataFrame or Group): The data which will be used for computation
    """
    idxmax = data["value"].idxmax()
    if np.isnan(idxmax):
        print("There is no maximum value as there is no data")
    else:
        max = data["value"].at[idxmax]
        date = data["date"].at[idxmax]
        max = round(max, 2)
        print(f"The max    for the date range is: {max} ".ljust(40) + f"which was achieved at {date}")

def show_data_min(data: pd.DataFrame):
    """Computes the minimum of the data for a dataframe

    Args:
        data (pd.DataFrame or Group): The data which will be used for computation
    """
    idxmin = data["value"].idxmin()
    if np.isnan(idxmin):
        print("There is no minimum value as there is no data")
    else:
        min = data["value"].at[idxmin]
        date = data["date"].at[idxmin]
        min = round(min, 2)
        print(f"The min    for the date range is: {min} ".ljust(40) + f"which was achieved at {date}")
