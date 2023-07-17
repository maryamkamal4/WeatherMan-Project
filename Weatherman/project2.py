import argparse
from datetime import datetime
import os
from termcolor import colored


def extract_year(date):
    return date.split('-')[0]  # Extract the year from the date string


def extract_day(date):
    return int(date.split('-')[2])


def extract_year_month(date):
    return '-'.join(date.split('-')[:2])  # Extract the year and month from the date string


def by_year(year, city):
    folder_path = f'C:\\Users\\hamxa\\Desktop\\Weatherman_Project\\Weatherman\\{city}_weather'
    selected_columns = [0, 1, 3, 7]  # Example: Selecting columns at index 1, 3, 7

    highest_temp = 0  # Initialize highest temperature with negative infinity
    lowest_temp = 0  # Initialize lowest temperature with positive infinity
    highest_humidity = 0  # Initialize highest humidity with negative infinity
    lowest_date = ''
    highest_date = ''

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        date_str = line.split(',')[0]  # Assuming the date is the first column
                        date = datetime.strptime(date_str, '%Y-%m-%d')  # Specify the expected date format
                    except ValueError:
                        continue  # Skip the line if the date format is not valid

                    data_year = extract_year(date_str)  # Extract the year from the date column

                    if data_year == year:
                        columns = line.strip().split(',')  # Assuming columns are separated by commas
                        selected_data = [columns[i] for i in selected_columns]

                        if selected_data[1]:  # Check if the value is not empty
                            col1_value = int(selected_data[1])  # Assuming column 1 contains numeric values
                            if col1_value > highest_temp:
                                highest_temp = col1_value
                                highest_date = date_str

                        if selected_data[2]:  # Check if the value is not empty
                            col3_value = int(selected_data[2])  # Assuming column 3 contains numeric values
                            if col3_value < lowest_temp:
                                lowest_temp = col3_value
                                lowest_date = date_str

                        if selected_data[3]:  # Check if the value is not empty
                            col7_value = int(selected_data[3])  # Assuming column 7 contains numeric values
                            if col7_value > highest_humidity:
                                highest_humidity = col7_value
                                humid_date = date_str

        except IOError:
            print("Error: could not read file " + file_name)

    output = f"Highest: {highest_temp}C on {highest_date}\nLowest: {lowest_temp}C on {lowest_date}\nHumid: {highest_humidity}% on {humid_date}"
    return output


def by_month(year_month, city):
    folder_path = f'C:\\Users\\hamxa\\Desktop\\Weatherman_Project\\Weatherman\\{city}_weather'
    selected_columns = [0, 2, 8]  # Example: Selecting columns at index 1, 3, 7

    year, month = year_month.split('/')
    avg_highest_temperature = 0  # Initialize the maximum value with negative infinity
    avg_lowest_temperature = 0  # Initialize the minimum value with positive infinity

    count = 0
    sum_values = 0

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        date_str = line.split(',')[0]  # Assuming the date is the first column
                        date = datetime.strptime(date_str, '%Y-%m-%d')  # Specify the expected date format
                    except ValueError:
                        continue  # Skip the line if the date format is not valid

                    data_year_month = extract_year_month(date_str)  # Extract the year and month from the date column

                    if data_year_month == f"{year}-{month}":
                        columns = line.strip().split(',')  # Assuming columns are separated by commas
                        selected_data = [columns[i] for i in selected_columns]

                        if selected_data[1]:  # Check if the value is not empty
                            value = int(selected_data[1])  # Assuming column 2 contains numeric values

                            if value > avg_highest_temperature:
                                avg_highest_temperature = value

                            if value < avg_lowest_temperature:
                                avg_lowest_temperature = value

                        if selected_data[2]:  # Check if the value is not empty
                            value = int(selected_data[2])  # Assuming column 2 contains numeric values
                            sum_values += value
                            count += 1
                            avg_humidity = int(sum_values / count)

        except IOError:
            print("Error: could not read file " + file_name)

    output = f"Highest Average: {avg_highest_temperature}C \nLowest Average: {avg_lowest_temperature}C \nAverage_Humidity: {avg_humidity}%"
    return output


def draw_chart(year_month, city):
    folder_path = f'C:\\Users\\hamxa\\Desktop\\Weatherman_Project\\Weatherman\\{city}_weather'
    selected_columns = [0, 1, 3]  # Example: Selecting columns at index 1, 3

    year, month = year_month.split('/')
    data = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        date_str = line.split(',')[0]  # Assuming the date is the first column
                        date = datetime.strptime(date_str, '%Y-%m-%d')  # Specify the expected date format
                    except ValueError:
                        continue  # Skip the line if the date format is not valid

                    data_year_month = extract_year_month(date_str)  # Extract the year and month from the date column

                    if data_year_month == f"{year}-{month}":
                        day = extract_day(date_str)
                        columns = line.strip().split(',')  # Assuming columns are separated by commas
                        selected_data = [columns[i] for i in selected_columns]

                        if selected_data[1] and selected_data[2]:  # Check if the values are not empty
                            highest_temp = int(selected_data[1])  # Assuming column 1 contains numeric values
                            lowest_temp = int(selected_data[2])  # Assuming column 3 contains numeric values
                            data[day] = (highest_temp, lowest_temp)

        except IOError:
            print("Error: could not read file " + file_name)

    month_name = datetime.strptime(f"{year}-{month}", "%Y-%m").strftime("%B %Y")
    print(month_name)

    for day, temps in sorted(data.items()):
        highest_temp, lowest_temp = temps
        highest_bar = '+' * int(highest_temp)
        lowest_bar = '+' * int(lowest_temp)

        highest_colored_bar = colored(highest_bar, 'red')
        lowest_colored_bar = colored(lowest_bar, 'blue')

        print(f"{day:02d}  {lowest_colored_bar}{highest_colored_bar}  {int(lowest_temp)}C - {int(highest_temp)}C")


# Parse the command line arguments
parser = argparse.ArgumentParser(description='Weatherman Data Analysis')
parser.add_argument('-e', '--year', type=str, help='Year for data analysis')
parser.add_argument('-a', '--month', type=str, help='Year/Month for data analysis')
parser.add_argument('-c', '--chart', type=str, help='Draw chart for a given month')
parser.add_argument('city', type=str, help='City name for data analysis')

args = parser.parse_args()

if args.year:
    result = by_year(args.year, args.city)
    print(result)
elif args.month:
    result = by_month(args.month, args.city)
    print(result)
elif args.chart:
    draw_chart(args.chart, args.city)
else:
    print("Please provide valid arguments for data analysis.")
