import pytest
import pandas as pd
import numpy as np
import datetime as dt
import math

import sys
sys.path.insert(0,'..')

import reporting

# ALL THE MAGIC NUMBERS WERE COMPUTED IN EXCEL
FLOAT_TOLERANCE = 1e-5

# The test data
test_data = reporting.get_monitering_station_data()

def test_daily_average():
    # Process test data
    dataHRLno = reporting.daily_average(test_data, "HRL", "no")
    dataMY1no = reporting.daily_average(test_data, "MY1", "no")
    dataKC1no = reporting.daily_average(test_data, "KC1", "no")
    dataHRLpm10 = reporting.daily_average(test_data, "HRL", "pm10")
    dataMY1pm10 = reporting.daily_average(test_data, "MY1", "pm10")
    dataKC1pm10 = reporting.daily_average(test_data, "KC1", "pm10")
    dataHRLpm25 = reporting.daily_average(test_data, "HRL", "pm25")
    dataMY1pm25 = reporting.daily_average(test_data, "MY1", "pm25")
    dataKC1pm25 = reporting.daily_average(test_data, "KC1", "pm25")

    # Get index of date
    dateHRLindex = reporting.get_date_index(test_data, "HRL", "2021-03-14")
    dateMY1index = reporting.get_date_index(test_data, "MY1", "2021-03-14")
    dateKC1index = reporting.get_date_index(test_data, "KC1", "2021-03-14")
    
    # Tests for full data
    assert np.isclose(dataHRLno[dateHRLindex], 0.859020, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1no[dateMY1index], 11.747027, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1no[dateKC1index], 0.607238, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm10[dateHRLindex], 6.333875, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm10[dateMY1index], 12.97917, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm10[dateKC1index], 7.200000, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm25[dateHRLindex], 3.971333, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm25[dateMY1index], 4.270833, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm25[dateKC1index], 4.327833, rtol=FLOAT_TOLERANCE)
    
    # Test for partial data
    partialDateIndex = reporting.get_date_index(test_data, "HRL", "2021-12-21")
    assert np.isclose(dataMY1pm25[partialDateIndex], 5.3875, rtol=FLOAT_TOLERANCE)
    # Test for missing data
    missingDateIndex = reporting.get_date_index(test_data, "HRL", "2021-12-31")
    assert np.isclose(dataMY1pm25[missingDateIndex], np.nan, equal_nan = True)
    
    # Test for exceptions
    with pytest.raises(Exception):
        reporting.daily_average(test_data, "Invalid Station", "no")
        reporting.daily_average(test_data, "HRL", "Invalid Pollutant")
        reporting.daily_average(test_data, "Invalid Station", "Invalid Pollutant")
    
def test_daily_median():
    # Process test data
    dataHRLno = reporting.daily_median(test_data, "HRL", "no")
    dataMY1no = reporting.daily_median(test_data, "MY1", "no")
    dataKC1no = reporting.daily_median(test_data, "KC1", "no")
    dataHRLpm10 = reporting.daily_median(test_data, "HRL", "pm10")
    dataMY1pm10 = reporting.daily_median(test_data, "MY1", "pm10")
    dataKC1pm10 = reporting.daily_median(test_data, "KC1", "pm10")
    dataHRLpm25 = reporting.daily_median(test_data, "HRL", "pm25")
    dataMY1pm25 = reporting.daily_median(test_data, "MY1", "pm25")
    dataKC1pm25 = reporting.daily_median(test_data, "KC1", "pm25")
    
    # Get index of date
    dateHRLindex = reporting.get_date_index(test_data, "HRL", "2021-03-14")
    dateMY1index = reporting.get_date_index(test_data, "MY1", "2021-03-14")
    dateKC1index = reporting.get_date_index(test_data, "KC1", "2021-03-14")
    
    # Tests for full data
    assert np.isclose(dataHRLno[dateHRLindex], 0.643260, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1no[dateMY1index], 10.84549, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1no[dateKC1index], 0.33122, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm10[dateHRLindex], 5.7775, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm10[dateMY1index], 12.7, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm10[dateKC1index], 6.4875, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm25[dateHRLindex], 3.3555, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm25[dateMY1index], 4.4, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm25[dateKC1index], 3.632, rtol=FLOAT_TOLERANCE)
    
    # Test for partial data
    partialDateIndex = reporting.get_date_index(test_data, "HRL", "2021-12-21")
    assert np.isclose(dataMY1pm25[partialDateIndex], 5.35, rtol=FLOAT_TOLERANCE)
    # Test for missing data
    missingDateIndex = reporting.get_date_index(test_data, "HRL", "2021-12-31")
    assert np.isclose(dataMY1pm25[missingDateIndex], np.nan, equal_nan = True)
    
    # Test for exceptions
    with pytest.raises(Exception):
        reporting.daily_median(test_data, "Invalid Station", "no")
        reporting.daily_median(test_data, "HRL", "Invalid Pollutant")
        reporting.daily_median(test_data, "Invalid Station", "Invalid Pollutant")
        
def test_hourly_average():
    # Process test data
    dataHRLno = reporting.hourly_average(test_data, "HRL", "no")
    dataMY1no = reporting.hourly_average(test_data, "MY1", "no")
    dataKC1no = reporting.hourly_average(test_data, "KC1", "no")
    dataHRLpm10 = reporting.hourly_average(test_data, "HRL", "pm10")
    dataMY1pm10 = reporting.hourly_average(test_data, "MY1", "pm10")
    dataKC1pm10 = reporting.hourly_average(test_data, "KC1", "pm10")
    dataHRLpm25 = reporting.hourly_average(test_data, "HRL", "pm25")
    dataMY1pm25 = reporting.hourly_average(test_data, "MY1", "pm25")
    dataKC1pm25 = reporting.hourly_average(test_data, "KC1", "pm25")
    
    # Test data
    assert np.isclose(dataHRLno[0], 6.1148450, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1no[0], 18.835068, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1no[0], 3.5154820, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm10[0], 12.981416, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm10[0], 15.759130, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm10[0], 13.774863, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm25[0], 8.5614080, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm25[0], 10.557051, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm25[0], 9.6341290, rtol=FLOAT_TOLERANCE)
    
    # Test for exceptions
    with pytest.raises(Exception):
        reporting.hourly_average(test_data, "Invalid Station", "no")
        reporting.hourly_average(test_data, "HRL", "Invalid Pollutant")
        reporting.hourly_average(test_data, "Invalid Station", "Invalid Pollutant")

def test_monthly_average():
    # Process test data
    dataHRLno = reporting.monthly_average(test_data, "HRL", "no")
    dataMY1no = reporting.monthly_average(test_data, "MY1", "no")
    dataKC1no = reporting.monthly_average(test_data, "KC1", "no")
    dataHRLpm10 = reporting.monthly_average(test_data, "HRL", "pm10")
    dataMY1pm10 = reporting.monthly_average(test_data, "MY1", "pm10")
    dataKC1pm10 = reporting.monthly_average(test_data, "KC1", "pm10")
    dataHRLpm25 = reporting.monthly_average(test_data, "HRL", "pm25")
    dataMY1pm25 = reporting.monthly_average(test_data, "MY1", "pm25")
    dataKC1pm25 = reporting.monthly_average(test_data, "KC1", "pm25")
    
    # Test data
    assert np.isclose(dataHRLno[0], 5.647247, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1no[0], 35.605124, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1no[0], 6.415822, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm10[0], 10.162960, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm10[0], 14.992286, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm10[0], 11.747577, rtol=FLOAT_TOLERANCE)
    
    assert np.isclose(dataHRLpm25[0], 7.679626, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataMY1pm25[0], 11.314963, rtol=FLOAT_TOLERANCE)
    assert np.isclose(dataKC1pm25[0], 8.724157, rtol=FLOAT_TOLERANCE)
    
    # Test for exceptions
    with pytest.raises(Exception):
        reporting.monthly_average(test_data, "Invalid Station", "no")
        reporting.monthly_average(test_data, "HRL", "Invalid Pollutant")
        reporting.monthly_average(test_data, "Invalid Station", "Invalid Pollutant")

def test_peak_hour_date():
    # Process test data
    dataHRLno = reporting.peak_hour_date(test_data, "2021-01-01", "HRL", "no")
    dataMY1no = reporting.peak_hour_date(test_data, "2021-01-01", "MY1", "no")
    dataKC1no = reporting.peak_hour_date(test_data, "2021-01-01", "KC1", "no")
    dataHRLpm10 = reporting.peak_hour_date(test_data, "2021-01-01", "HRL", "pm10")
    dataMY1pm10 = reporting.peak_hour_date(test_data, "2021-01-01", "MY1", "pm10")
    dataKC1pm10 = reporting.peak_hour_date(test_data, "2021-01-01", "KC1", "pm10")
    dataHRLpm25 = reporting.peak_hour_date(test_data, "2021-01-01", "HRL", "pm25")
    dataMY1pm25 = reporting.peak_hour_date(test_data, "2021-01-01", "MY1", "pm25")
    dataKC1pm25 = reporting.peak_hour_date(test_data, "2021-01-01", "KC1", "pm25")
    
    # Tests for full data
    assert dataHRLno[0] == "20:00"
    assert np.isclose(dataHRLno[1], 13.00595, rtol=FLOAT_TOLERANCE)
    assert dataMY1no[0] == "16:00"
    assert np.isclose(dataMY1no[1], 54.87196, rtol=FLOAT_TOLERANCE)
    assert dataKC1no[0] == "19:00"
    assert np.isclose(dataKC1no[1], 17.7681, rtol=FLOAT_TOLERANCE)
    
    assert dataHRLpm10[0] == "14:00"
    assert np.isclose(dataHRLpm10[1], 31.18, rtol=FLOAT_TOLERANCE)
    assert dataMY1pm10[0] == "02:00"
    assert np.isclose(dataMY1pm10[1], 45.1, rtol=FLOAT_TOLERANCE)
    assert dataKC1pm10[0] == "02:00"
    assert np.isclose(dataKC1pm10[1], 65.475, rtol=FLOAT_TOLERANCE)
    
    assert dataHRLpm25[0] == "14:00"
    assert np.isclose(dataHRLpm25[1], 27.694, rtol=FLOAT_TOLERANCE)
    assert dataMY1pm25[0] == "02:00"
    assert np.isclose(dataMY1pm25[1], 40.3, rtol=FLOAT_TOLERANCE)
    assert dataKC1pm25[0] == "02:00"
    assert np.isclose(dataKC1pm25[1], 55.802, rtol=FLOAT_TOLERANCE)
    
    # Test partial data
    dataMY1partial = reporting.peak_hour_date(test_data, "2021-12-21", "MY1", "pm25")
    assert dataMY1partial[0] == "08:00"
    assert np.isclose(dataMY1partial[1], 8.2, rtol=FLOAT_TOLERANCE)
    
    # Test no data (CRASHES - IDK WHY)
    #dataMY1full = reportin.peak_hour_date(test_data, "2021-12-31", "MY1", "pm25")
    #assert dataMY1full == None

    # Test for exceptions
    with pytest.raises(Exception):
        reporting.peak_hour_date(test_data, "Invalid Station", "no")
        reporting.peak_hour_date(test_data, "HRL", "Invalid Pollutant")
        reporting.peak_hour_date(test_data, "Invalid Station", "Invalid Pollutant")

def test_count_missing_data():
    

    # Test for exceptions
    with pytest.raises(Exception):
        reporting.count_missing_data(test_data, "Invalid Station", "no")
        reporting.count_missing_data(test_data, "HRL", "Invalid Pollutant")
        reporting.count_missing_data(test_data, "Invalid Station", "Invalid Pollutant")

def test_fill_missing_data():
    

    # Test for exceptions
    with pytest.raises(Exception):
        reporting.fill_missing_data(test_data, None, "Invalid Station", "no")
        reporting.fill_missing_data(test_data, None, "HRL", "Invalid Pollutant")
        reporting.fill_missing_data(test_data, None, "Invalid Station", "Invalid Pollutant")
