import argparse
from datetime import datetime
from termcolor import colored
import utils


def by_year(year, city):
    selected_columns = [0, 1, 3, 7]  # Example: Selecting columns at index 1, 3

    highest_temp = float('-inf')  # Initialize highest temperature with negative infinity
    lowest_temp = float('inf')  # Initialize lowest temperature with positive infinity
    highest_humidity = float('-inf')  # Initialize highest humidity with negative infinity
    lowest_date = ''
    highest_date = ''
    humid_date = ''

    try:
        for line, date_str in utils.file(city):
            data_year = utils.extract_year(date_str)  # Extract the year from the date column

            if data_year == year:
                selected_data = utils.selected_data(line, selected_columns)

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

        output = f"Highest: {highest_temp}C on {highest_date}\nLowest: {lowest_temp}C on {lowest_date}\nHumid: {highest_humidity}% on {humid_date}"
        return output
    except FileNotFoundError:
        return "Invalid city. Please provide a valid city name."

def by_month(year_month, city):
    selected_columns = [0, 2, 8]  # Example: Selecting columns at index 1, 3, 7

    year, month = year_month.split('/')
    avg_highest_temperature = 0
    avg_lowest_temperature = float('inf')
    avg_humidity = 0

    count = 0
    sum_temps = 0
    sum_humidity = 0

    try:
        for line, date_str in utils.file(city):
            data_year_month = utils.extract_year_month(date_str)  # Extract the year and month from the date column

            if data_year_month == f"{year}-{month}":
                selected_data = utils.selected_data(line, selected_columns)

                if selected_data[1]:  # Check if the value is not empty
                    temp_value = int(selected_data[1])  # Assuming column 2 contains numeric values

                    if temp_value > avg_highest_temperature:
                        avg_highest_temperature = temp_value

                    if temp_value < avg_lowest_temperature:
                        avg_lowest_temperature = temp_value
                        # print(avg_lowest_temperature)

                    sum_temps += temp_value
                    count += 1

                if selected_data[2]:  # Check if the value is not empty
                    humidity_value = int(selected_data[2])  # Assuming column 8 contains numeric values
                    sum_humidity += humidity_value

        if count > 0:
            avg_humidity = int(sum_humidity / count)

        output = f"Highest Average: {avg_highest_temperature}C \nLowest Average: {avg_lowest_temperature}C \nAverage_Humidity: {avg_humidity}%"
        return output
    except FileNotFoundError:
        return "Invalid city. Please provide a valid city name."

def draw_chart(year_month, city):
    selected_columns = [0, 1, 3]  # Example: Selecting columns at index 1, 3

    year, month = year_month.split('/')
    data = {}

    try:
        for line, date_str in utils.file(city):
            data_year_month = utils.extract_year_month(date_str)

            if data_year_month == f"{year}-{month}":
                day = utils.extract_day(date_str)
                selected_data = utils.selected_data(line, selected_columns)

                if selected_data[1] and selected_data[2]:  # Check if the values are not empty
                    highest_temp = int(selected_data[1])  # Assuming column 1 contains numeric values
                    lowest_temp = int(selected_data[2])  # Assuming column 3 contains numeric values
                    data[day] = (highest_temp, lowest_temp)

        month_name = datetime.strptime(f"{year}-{month}", "%Y-%m").strftime("%B %Y")
        print(month_name)

        if len(data) == 0:
            print("No data available for the specified month and city.")
            return

        for day, temps in sorted(data.items()):
            highest_temp, lowest_temp = temps
            highest_bar = '+' * int(highest_temp)
            lowest_bar = '+' * int(lowest_temp)

            highest_colored_bar = colored(highest_bar, 'red')
            lowest_colored_bar = colored(lowest_bar, 'blue')

            print(f"{day:02d}  {lowest_colored_bar}{highest_colored_bar}  {int(lowest_temp)}C - {int(highest_temp)}C")
    except FileNotFoundError:
        print("Invalid city. Please provide a valid city name.")


def main():
    args = utils.parse_arguments()

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


if __name__ == "__main__":
    main()
