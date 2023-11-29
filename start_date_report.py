#!/usr/bin/env python3

import csv
import datetime
import requests
import operator


FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    # year = int("2020") # for testing purposes
    # month = int("06") # for testing purposes
    # day = int("13") # for testing purposes
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))

    return (datetime.datetime(year, month, day))

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def get_same_or_newer(start_date):
    """Returns the employees that started on the given date, or the closest one."""
    data = get_file_lines(FILE_URL)
    reader = csv.reader(data[1:])
    list = []
    min_date_employees = {}
    sorteddict = sorted(reader, key=operator.itemgetter(3))
    for row in sorteddict: 
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')
        row_without_time = row_date.date()
        if row_date < start_date:
            continue
        else:
            if row_without_time in min_date_employees:
                list = min_date_employees[row_without_time]
                list.append(row[0] + " " + row[1])
                min_date_employees[row_without_time] = list
            else:
                min_date_employees[row_without_time] = [row[0] + " " + row[1]]
    return min_date_employees

def list_newer(start_date): 
    """ Print newest employees """
    earliest_date = datetime.datetime(2018, 1, 1)
    if start_date <= datetime.datetime.today() and start_date >= earliest_date: # If date is between Jan 12st, 2018 and today, list hired all employees (data ends 2020/07)
        employees = get_same_or_newer(start_date)
        for key, employee in employees.items():
            print("Started on {}: {}".format(key.strftime("%b %d, %Y"), employees[key]))
    else:
        print("\nDate out of range. The date must be greater than Jan 1st, 2018 and before today")

def main():
    start_date = get_start_date()
    list_newer(start_date)

if __name__ == "__main__":
    main()
