from typing import List, Tuple
import random
import csv
from datetime import datetime, timedelta


# Given data
data = [
    ["cookie,timestamp"],
    ["AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00"],
    ["SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00"],
    ["5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00"],
    ["AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00"],
    ["SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00"],
    ["4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00"],
    ["fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00"],
    ["4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00"],
]


##############################################################################
##################        CSV File Creation + Checker       ################## 
##############################################################################

def create_csv_file(data: List[List[str]], filename: str) -> None:
    """
        Helper function to create a csv file with the given data.
        The data should be of the form: [ [line1], [line2], ... ]

        Params: data     (a list of lists containing data for the cookies log).
                filename (the name of the csv file we want to create).
        Returns: Nothing (instead, it writes a csv file to the current directory).
    """

    # newline='' --> uses the default line ending: '\n'
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in data:
            # Write each line in the given data as a new row in the cookies log
            csv_writer.writerow(line)


def create_custom_csv_file(num_lines: int) -> None:
    """
        Function to create custom data, and turn this data into a CSV file.
        The data is randomly generated (with the same year as 2023), but depends on the create_csv_file function
        to turn the data into a csv file directly.

        Params: num_lines (an integer representing the number of lines we want to have in our csv file).
        Returns: None, but utilizes create_csv_file to create a brand new csv file of our cookie logs.
    """

    if num_lines < 1:
        raise ValueError("Invalid Number of Lines. Requires at least one line to create a CSV file.")
    
    header = ['cookie,timestamp']
    data = [header]

    for i in range(num_lines):
        # A cookie name consists of 16 characters with random alphanumeric characters
        cookie_name = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(16))

        # Datetime objects make it easier for us to extract date and time data
        # All months have 28 days so there should be no datetime object conflicts
        datetime_obj = (datetime(2023, random.randint(1, 12), random.randint(1, 28)))   # Keeping year the same is my personal design choice
        date = str(datetime_obj.date())

        # The extra time at the end of each row is fixed
        extra_time = "00+00:00"
        hour, minutes = random.randint(0, 23), random.randint(0, 59)

        # Time is in the form xx:xx
        time = f"{hour:02d}:{minutes:02d}"
        
        # {cookie_name},{date}T{time}:{extra_time}
        data.append([cookie_name + ',' + date + 'T' + time + ':' + extra_time])

        # Extra cases so not all cookies are unique for each date
        if i % 2 == 0:
            data.append([cookie_name + ',' + date + 'T' + time + ':' + extra_time])

            # Make sure to have at most num_lines + 1 lines of data (including the header)
            if len(data) - 1 == num_lines: break
            
        if i % 4 == 0:
            data.append([cookie_name + ',' + date + 'T' + time + ':' + extra_time])

            # Make sure to have at most num_lines + 1 lines of data (including the header)
            if len(data) - 1 == num_lines: break
        
        if i % 6 == 0:
            data.append([cookie_name + ',' + date + 'T' + time + ':' + extra_time])

            # Make sure to have at most num_lines + 1 lines of data (including the header)
            if len(data) - 1 == num_lines: break

    rows = data[1:]

    # We need to sort by timestamp
    sorted_rows = sorted(rows, key = lambda row: row[0].split(',')[1], reverse=True)
    sorted_data = [header] + sorted_rows
    create_csv_file(sorted_data, 'more_cookie_log.csv')



def main():
    # create_csv_file(data, 'cookie_log.csv')       # Create cookie logs from manual data
    create_custom_csv_file(1000)                  # Create cookie logs from auto-generated data


if __name__ == '__main__':
    """
        Run the main function to create our cookie log datasets.
    """
    
    main()