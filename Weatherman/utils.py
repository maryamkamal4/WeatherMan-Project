
import argparse
from datetime import datetime
import os
import re


def extract_year(date):
    return date.split('-')[0]  # Extract the year from the date string


def extract_day(date):
    return int(date.split('-')[2])


def extract_year_month(date):
    return '-'.join(date.split('-')[:2])  # Extract the year and month from the date string


def data_year_month(date_str):
    data_year_month = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m')  # Extract the year and month from the date column
    return data_year_month


def selected_data(line, selected_columns):
    columns = line.strip().split(',')  # Assuming columns are separated by commas
    selected_data = [columns[i] for i in selected_columns]
    return selected_data


def file(city):
    folder_path = f'C:\\Users\\hamxa\\Desktop\\Weatherman_Project\\Weatherman\\{city}_weather'

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

                    yield line, date_str

        except IOError:
            print("Error: could not read file " + file_name)
            
            
def parse_arguments():
    parser = argparse.ArgumentParser(description='Weatherman Data Analysis')
    parser.add_argument('-e', '--year', type=str, help='Year for data analysis')
    parser.add_argument('-a', '--month', type=str, help='Year/Month for data analysis (YYYY/MM)')
    parser.add_argument('-c', '--chart', type=str, help='Draw chart for a given month')
    parser.add_argument('city', type=str, help='City name for data analysis')

    args = parser.parse_args()

    if args.year:
        if not re.match(r"^\d{4}$", args.year):
            raise ValueError("Invalid year format. Please provide a valid year (YYYY).")

    if args.month:
        if not re.match(r"^\d{4}/\d{1,2}$", args.month):
            raise ValueError("Invalid month format. Please provide a valid month (YYYY/MM).")

    return args
