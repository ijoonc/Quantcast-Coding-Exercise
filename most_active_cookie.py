import argparse
import csv
from typing import List, Tuple
import random
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

    
    # We need to sort the timestamps
    rows = data[1:]
    sorted_rows = sorted(rows, key = lambda row: row[0].split(',')[1], reverse=True)
    sorted_data = [header] + sorted_rows
    create_csv_file(sorted_data, 'more_cookie_log.csv')


##############################################################################
###################           Validation Checks           ####################
##############################################################################

'''
    We are assuming that the cookie,timestamp format is consistent in the data given.
    Hence, the cookie name should already be valid as well as the timestamp. 
    For now, we do not want to pay attention to the time (in UTC), but rather the date.
'''


def valid_csv(filename: str) -> None:
    """
        Raises an error depending on whether the given file is a valid csv file or not.

        Params: filename (a string representing the name of a file of data).
        Returns: None, but raises an error if the file is not of the .csv format.
    """

    if filename[-4:] != '.csv':
        raise ValueError("Invalid file format. Requires CSV file.")


def valid_date(date: str) -> None:
    """
        Raises an error if there is an valid date given in the cookie logs.

        Params: date (a string representing a particular date in the cookie logs).
        Returns: None, but raises an error if the year, month, day, or the entire date is invalid.
    """

    if len(date.split('-')) != 3:
        raise ValueError("Invalid date format. Requires xxxx-xx-xx format.")

    year, month, day = date.split('-')

    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        raise ValueError("Invalid date format. Requires xxxx-xx-xx format.")
    
    # Year can be any four digit value wheras month and day cannot
    year, month, day = int(year), int(month), int(day)

    if month < 1 or month > 12:
        raise ValueError("Invalid Month Provided.")

    if day < 1 or day > 31:
        raise ValueError("Invalid Day Provided.")


##############################################################################
############              Find Most Frequent Cookie              ############# 
##############################################################################

def frequency_update(freq_map: dict, max_freq: int, cookie_name: str):
    """
        This function updates the hashmap containing the frequency of cookie names in the given date.
        It also updates the maximum frequency if we reached a new maximum.

        Params: freq_map    (the hashmap containing the frequency of cookie names).
                max_freq    (the maximum frequency of any apparent cookie).
                cookie_name (the name of the cookie of interest).
        Returns: the newly updated frequency hashmap and the current maximum frequency of any cookie.

        Runtime Complexity: O(1) since we are simply utilizing hashing functions.
        Space Complexity: O(n) where n is the number of unique cookies in the hashmap so far.
    """

    # Only consider cookie names that occur in our date of interest
    freq_map[cookie_name] = 1 + freq_map.get(cookie_name, 0)

    if freq_map[cookie_name] > max_freq:
        # Update the maximum frequency of all cookies
        max_freq = freq_map[cookie_name]

    return freq_map, max_freq

def find_cookie_name_and_date(line: str) -> Tuple[str, str]:
    """
        Helper function to all functions defined below.
        For a given line of the cookies log, this function returns the cookie name and date
        by splitting the line contents into segments of interest.
        
        Params: line (a line of a cookies log (csv file)).
        Returns: the cookie name and date of the given line (in the form of strings).

        Runtime Complexity: O(m) where m is the number of characters in the given line.
        Space Complexity: O(1), assuming that the given line does not play a role.
    """

    separated_contents = line.split(',')
    cookie_name = separated_contents[0]         # Cookie name is separated by a ','

    more_separated_contents = separated_contents[1].split('T')
    cookie_date = more_separated_contents[0]    # Cookie date is separated by ',' and 'T'

    valid_date(cookie_date)

    return cookie_name, cookie_date


def most_active_cookie(csv_file: str, input_date: str) -> None:
    """
        This function prints out the cookie that occurs the most within the given input date.

        Params: csv_file (a csv file containing the cookies log).
                input_date (a string that represents the date of interest).
        Returns: Nothing. Instead, this function prints out the names of cookies that occur most often.

        Runtime Complexity: O(nm + n) where n is the number of rows in the cookies log and m is the number 
                            of chars in each row.
        Space Complexity: O(n) where n is the number of rows. This is because each row can contain a unique 
                          cookie with the given input date.
    """

    # Before anything, make sure the given file is a CSV file
    valid_csv(csv_file)

    # These two variables will hold cookie data within the given input_date
    freq = {}                   # Key: cookie name, Value: frequency of pair
    max_freq = 0                # Frequency of the most occurring cookie

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)        # Skip the header (i.e. "cookie,timestamp")

        for line in csv_reader:
            # line is in the form of [line contents: string]
            line = line[0]
            
            cookie_name, cookie_date = find_cookie_name_and_date(line)

            # Only obtain frequency of cookie if we have found our date of interest
            if cookie_date == input_date:
                freq, max_freq = frequency_update(freq, max_freq, cookie_name)
    
    # No cookie found with the given date
    if len(freq.items()) == 0:
        print("No cookie(s) found.")

    else:
        # Print out all the cookie names with the maximum frequency
        for k, v in freq.items():
            if v == max_freq:
                print(k)


##############################################################################
##########      Find Most Frequent Cookie Using Binary Search      ########### 
##############################################################################

def binary_search(csv_data: List[str], date: str, left: int, right: int) -> Tuple[int, int]:
    """
        This is a helper function to most_active_cookie_binary_search(csv_file, date).
        We perform binary search on the rows of the cookies data to find the FIRST
        row with the given date.

        Params: csv_data (a list of strings containing the cookies log data).
                date     (the cookie date of interest).
                left     (the left pointer).
                right    (the right pointer).
        Returns: the left and right pointers, starting at the index that contains the date of interest.

        Runtime Complexity: O(m * logn) where m is the number of chars in each line and n is the number of rows in csv_data.
        Space Complexity: O(1), assuming that the parameters do not contribute to the total space complexity.
    """

    while left <= right:
        # mid = (r + l) // 2 --> can lead to integer overflow
        mid = left + (right - left) // 2

        # Find the cookie date of the current row of interest
        _, cookie_date = find_cookie_name_and_date(csv_data[mid])

        # Perform binary search to find the first date that is the same as the input date
        if date < cookie_date:
            left = mid + 1
        
        elif date > cookie_date:
            right = mid - 1
        
        else:
            left = right = mid
            
            # Return the first and second indices (so that we don't check the same index twice) 
            # of the given date
            return left, right + 1


    # No cookie found with the given date
    return -1, -1


def most_active_cookie_binary_search(csv_file: str, date: str) -> None:
    """
        This function is the overarching function that finds the most active cookie(s) using binary search.
        It serves as an alternative/better solution to the most_active_cookie function, which searches through all the rows
        of the given cookie log per function call.
        This function also depends on helper functions such as binary_search, find_cookie_name_and_date, and frequency_update.
        
        Params: csv_file (the cookie logs in the form of a CSV file).
                date (the date of interest in the form of a string).
        Returns: None, but prints out the most active cookie(s) in the given log.

        Runtime Complexity: O(mn + n) where m is the number of characters in each row and n is the number of rows in the log file.
                            In the worst case, all rows contain a unique cookie that appears in the given date. That means we stop the
                            binary search on the first iteration, and then iterate through the entire file to find all the cookie names.
        Space Complexity: O(n) where n is the number of rows. This is because each row can contain a unique cookie with the given input date.
    """

    # Before anything, make sure the given file is a CSV file
    valid_csv(csv_file)

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        # Store each line of the cookies log into a list for easier access to cookies content
        csv_data = [line[0] for line in csv_reader]
        left, right = binary_search(csv_data, date, 0, len(csv_data) - 1)

        # At least one cookie exists with the given input date
        if left != -1:
            counter = {}
            max_freq = 0

            # Check left
            while left >= 0:
                # Obtain the cookie name and date of current row
                cookie_name, cookie_date = find_cookie_name_and_date(csv_data[left])

                if cookie_date == date:
                    counter, max_freq = frequency_update(counter, max_freq, cookie_name)
                    left -= 1

                else:
                    break

            # Check right
            while right < len(csv_data):
                # Obtain the cookie name and date of current row
                cookie_name, cookie_date = find_cookie_name_and_date(csv_data[right])

                if cookie_date == date:
                    counter, max_freq = frequency_update(counter, max_freq, cookie_name)
                    right += 1
                
                else:
                    break
            
            # Print out all the cookie names with the highest frequency
            for k, v in counter.items():
                if v == max_freq:
                    print(k)
        
        # No cookie found with the given input date
        else:
            print("No cookie(s) found.")

        
##############################################################################
##########               End of Function Declarations              ########### 
##############################################################################

def main():
    """
        Runs the functions of interest implemented above.
        A filename (for the cookie logs) and -d (for date) are both required for a valid run.
    """

    parser = argparse.ArgumentParser(description="Find the most active cookie on a certain day.")
    parser.add_argument('filename', help='Path to the CSV file containing the cookie data.')
    parser.add_argument('-d', '--date', help="Date for the most active cookie (YYYY-MM-DD)", required=True)

    args = parser.parse_args()

    filename = args.filename
    date = args.date

    # Validate the csv filename and given date first
    valid_csv(filename)
    valid_date(date)

    # Two functions that find the most active cookie
    most_active_cookie(filename, date)
    print()
    most_active_cookie_binary_search(filename, date)


if __name__ == '__main__':
    """
        It's best to run one of these functions at a time.
    """

    # create_csv_file(data, 'cookie_log.csv')
    create_custom_csv_file(1000)
    # main()


