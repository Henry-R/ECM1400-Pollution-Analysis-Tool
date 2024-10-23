# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

from sys import exit
import datetime as dt

import pandas as pd
import numpy as np

import utils
import reporting
import intelligence
import monitoring
    
def get_valid_input(valid_inputs):
    """Loops until the user enter input that is specified in the valid_inputs list

    Args:
        valid_inputs ([str]): A list of possible valid inputs

    Returns:
        str: The user_input after being checked against valid_inputs
    """
    is_input_valid = False
    while not is_input_valid:
        user_input = input().lower()
        if not user_input in valid_inputs:
            print("Invalid input! Please use one of these options:")
            print(valid_inputs)
        else:
            return user_input

def main_menu():
    """Displays the main menu and allows the user to access the functionality of each module
    """

    user_input = ""
    program_running = True

    while program_running:
        # Display menu options
        print("Please choose an option:")
        print("R - Access the PR module")
        print("I - Access the MI module")
        print("M - Access the RM module")
        print("A - Print the About text")
        print("Q - Quit the application")

        # Get user input
        user_input = input().lower()

        utils.clear_screen()

        # Display correct menu
        if user_input == 'r':
            reporting_menu()
        elif user_input == 'i':
            intelligence_menu()
        elif user_input == 'm':
            monitoring_menu()
        elif user_input == 'a':
            about()
        elif user_input == 'q':
            quit()
        else:
            print("Please choose a valid option")      

def reporting_menu():
    """Displays the reporting menu and allows the user to interact with functions from the 'reporting' module
    """
    has_exited_menu = False
    
    print("Welcome to the reporting menu")
    print()
    
    data = reporting.get_monitering_station_data()

    while not has_exited_menu:
        print("Please choose an option: ")
        print("A - See the daily average")
        print("M - See the daily median")
        print("H - See the hourly average")
        print("O - See the monthly average")
        print("P - See the peek hour and date")
        print("C - See the missing data count")
        print("Q - To go back to the menu")
        user_input = get_valid_input(["a", "m", "h", "o", "p", "c", "q"])
        
        # Returning from the function returns to the menu as menu is the only function that calls 'reporting_menu()'
        if user_input == "q":
            return
        
        print("Please select a monitoring station by entering the 3-letter monitoring station code:")
        print("HRL - London Harlington")
        print("MY1 - London Marylebone Road")
        print("KC1 - London N Kensington")
        # Functions take monitoring station codes only in uppercase
        monitoring_station = get_valid_input(["hrl", "my1", "kc1"]).upper()
        
        print("Please select a pollutant:")
        print("'no', 'pm10', or 'pm25'")
        pollutant = get_valid_input(["no", "pm10", "pm25"])
        
        if user_input == "a":
            # Daily Average
            date = monitoring.get_valid_date()
            date_index = reporting.get_date_index(data, monitoring_station, date)
            
            # Calculate data and print it to user
            avg_pollution = reporting.daily_average(data, monitoring_station, pollutant)
            print(f"Average pollution on {date} was {avg_pollution[date_index]}")
            
        elif user_input == "m":
            # Daily Median
            date = monitoring.get_valid_date()
            date_index = reporting.get_date_index(data, monitoring_station, date)
            
            avg_pollution = reporting.daily_median(data, monitoring_station, pollutant)
            print(f"Average pollution on {date} was {avg_pollution[date_index]}")
            
        elif user_input == "h":
            # Hourly Average
            hourly_average = reporting.hourly_average(data, monitoring_station, pollutant)
            print(hourly_average)
            
        elif user_input == "o":
            # Monthly Average
            month_codes = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            print("Please enter a 3-letter month code, e.g. 'feb' or 'jul'")
            month = get_valid_input(month_codes)
            month_index = month_codes.index(month)
            
            avg_pollution = reporting.monthly_average(data, monitoring_station, pollutant)
            print(f"Average pollution for '{month}' was {avg_pollution[month_index]}")
            
        elif user_input == "p":
            # Peak Hour and Date
            date = monitoring.get_valid_date()
            peek_pollution = reporting.peak_hour_date(data, date, monitoring_station, pollutant)
            if peek_pollution == None:
                print("There was no pollution data for this date")
            else:
                print(f"Maximum value of {peek_pollution[1]} was achieved at {peek_pollution[0]}")
                
        elif user_input == "c":
            # Missing data count
            missing_data_count = reporting.count_missing_data(data, monitoring_station, pollutant)
            print(f"The there are {missing_data_count} missing data entries for the '{pollutant}' column in the '{monitoring_station}' data sheet")

def monitoring_menu():
    """Allows the user to explore real-time data from the London Air API. 
    """
    
    start_date = dt.date.today()
    end_date = dt.date.today()
    
    has_exited_menu = False
    # Default options for fetching data
    pollutant = "NO"
    monitoring_station = "MY1"
    # Default options for displaying data
    data_grouping = "none"
    scale_max = 200
    display_options = ["mean_group", "median_group", "max_range", "min_range", "barchart"]
    
    # Fetch inital live data, additional data will only be fetched as needed
    raw_data = monitoring.get_live_data_from_api(monitoring_station, pollutant, start_date, end_date)
    
    while not has_exited_menu:
        monitoring.display_monitoring_data(raw_data, data_grouping, monitoring_station, pollutant, start_date, end_date, scale_max, display_options)
        
        print("Please choose the data types and range to display. When you are finished, press L to load and display the data")
        print("M - Select monitoring station")
        print("P - Select pollutant type")
        print("D - Select date")
        print("R - Select date range")
        print("G - Choose how the data is grouped")
        print("V - Choose how the data is visualised")
        print("L - Save changes and reload data")
        print("Q - Return to menu")
        
        user_input = get_valid_input(["m", "p", "d", "r", "g", "v", "l", "q"])
        
        # Return to menu
        if user_input == "q":
            return
        # Select Monitoring Station
        elif user_input == "m":
            print("Select a monitoring station:")
            print("(1) - London Harlington")
            print("(2) - London Marylebone Road")
            print("(3) - London N Kensington")
            user_input = get_valid_input(["1", "2", "3"])
            monitoring_station = ["HRL", "MY1", "KC1"][int(user_input) - 1]
        # Select Pollutant Type
        elif user_input == "p":
            print("Select a pollutant type:")
            print("(1) - NO")
            print("(2) - PM10")
            print("(3) - PM25")
            user_input = get_valid_input(["1", "2", "3"])
            pollutant = ["NO", "PM10", "PM25"][int(user_input) - 1]
        # Select Date
        elif user_input == "d":
            user_input = monitoring.get_valid_date()
            # Date will be in a valid form, so strptime will not raise exceptions
            date = dt.datetime.strptime(user_input, "%Y-%m-%d")
            start_date = date.date()
            end_date = start_date
        # Select Date Range
        elif user_input == "r":
            print("Enter a start date and a end date:")
            # Get dates as strings
            new_start_str = monitoring.get_valid_date()
            new_end_str = monitoring.get_valid_date()
            # Convert string dates to datetime dates
            new_start_date = dt.datetime.strptime(new_start_str, "%Y-%m-%d").date()
            new_end_date = dt.datetime.strptime(new_end_str, "%Y-%m-%d").date()
            # Check dates are not in the wrong order
            if new_start_date >= new_end_date:
                print("Start date must be before end date")
                return
            start_date, end_date = new_start_date, new_end_date
        # Choose How Data is Grouped
        elif user_input == "g":
            print("Select a data group size:")
            print("(1) - No Group")
            print("(2) - Days of the month")
            print("(3) - Weekdays")
            print("(4) - Month")
            print("(5) - Year")
            user_input = get_valid_input(["1", "2", "3", "4", "5"])
            data_grouping = ["none", "day", "time", "month", "year"][int(user_input) - 1]
        # Choose How Data is Visulised
        elif user_input == "v":
            print("(1) - Change data scale")
            print("(2) - Change active data displays")
            print("(3) - Back to menu")
            
            user_input = get_valid_input(["1", "2", "3"])
            
            # Change Data Scale
            if user_input == "1":
                is_valid_scale = False
                print("Select a new maximum value as a whole number at least 20")
                while not is_valid_scale:
                    new_scale_max = input()
                    # Check new scale is an integer
                    if not new_scale_max.isdigit():
                        print("Value must be a whole number!")
                    else:
                        new_scale_max = int(new_scale_max)
                        # Check if scale is below 20, which is too small to display on the console
                        if new_scale_max < 20:
                            print("New scale is too small! Scale must be at least 20")
                        else:
                            scale_max = new_scale_max
                            is_valid_scale = True
            # Change active data displays
            elif user_input == "2":
                toggleable_values = ["mean_range", "median_range", "max_range", "min_range", 
                                     "mean_group", "median_group", "barchart", "table"]
                exited_options_menu = False
                
                while not exited_options_menu:
                    # As this menu is quite large, redisplay options every time
                    monitoring.display_monitoring_data(raw_data, data_grouping, monitoring_station, pollutant, start_date, end_date, scale_max, display_options)
                    
                    print("(1)  - Toggle mean   (range)")
                    print("(2)  - Toggle median (range)")
                    print("(3)  - Toggle max    (range)")
                    print("(4)  - Toggle min    (range)")
                    print("(5)  - Toggle mean   (group)")
                    print("(6)  - Toggle median (group)")
                    print("(7)  - Toggle bar-chart")
                    print("(8) - Toggle table")
                    print("(9) - Back to menu")
                    print(f"Active options: {display_options}")
                    user_input = get_valid_input(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
                    
                    # Check if user wants to exit menu
                    if user_input == "9":
                        exited_options_menu = True
                    else:
                        toggled_value = toggleable_values[int(user_input) - 1]
                        # Toggle option
                        if toggled_value in display_options:
                            display_options.remove(toggled_value)
                        else:
                            display_options.append(toggled_value)
            elif user_input == "3":
                # Returns to menu
                pass
        # Load new data from API
        elif user_input == "l":
            print("Loading data...")
            raw_data = monitoring.get_live_data_from_api(monitoring_station, pollutant, start_date, end_date)
            
def intelligence_menu():
    """Displays the intelligence menu which allows the user to access the intelligence modules functions
    """
    MAP_INPUT = "data/map.png"
    has_exited_menu = False
    
    print()
    print("Welcome to the Intelligence Menu")
    
    while not has_exited_menu:
        print("Please choose an option:")
        print("R - Analyze red pixles")
        print("C - Analyze cyan pixles")
        print("Q - Return to main menu")
        
        user_input = get_valid_input(["r", "c", "q"])
        
        if user_input == "q":
            return
        else:
            colour_option = user_input
            
            print("Please select an option:")
            print("C - Get connected components")
            print("S - Get sorted connected components (Also outputs unsorted connected components)")
            
            user_input = get_valid_input(["c", "s"])
            
            # Get connected components
            if colour_option == "r":
                input_image = intelligence.find_red_pixels(MAP_INPUT)
            else:
                input_image = intelligence.find_cyan_pixels(MAP_INPUT)
            mark = intelligence.detect_connected_components(input_image)
  
            if user_input == "s":
                intelligence.detect_connected_components_sorted(mark)
            
    
    data = intelligence.find_red_pixels("data/map.png")
    #data = intelligence.find_cyan_pixels("data/map.png")
    mark = intelligence.detect_connected_components(data)
    intelligence.detect_connected_components_sorted(mark)

def about():
    """Displays the 'about' information
    """
    utils.clear_screen()

    print("Module code:     ECM1400")
    print("Candiate Number: 256396")
    print("Press [enter] to return to menu")

    input()
    utils.clear_screen()

def quit():
    """Exits the program in a controled way, using the exit function with a normal exit code
    """
    exit(0)

if __name__ == '__main__':
    main_menu()