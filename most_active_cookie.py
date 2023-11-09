import argparse
import csv
from typing import List, Tuple


##############################################################################
##################           Cookie Finder Object           ################## 
##############################################################################

class Cookie_Finder:

    def __init__(self, filename: str, date: str) -> None:
        """
            The constructor of the "Most Active" Cookie Finder, which contains the necessary attributes for each object.
            Note: the name is Cookie Finder instead of "Most_Active_Cookie_Finder" (or anything of the sort), just in case we 
                  decide to expand upon this problem.

            Params: filename (a valid CSV filename that this object will be associated with).
                    date     (a valid date that we will consider to find the most active cookie).
            Returns: Nothing, but creates a Cookie_Finder object that is designated to the given cookie logs.
        """

        self.filename = filename            # Store the filename for future uses
        self.date = date                    # Date of interest
        self.freq_map = {}                  # Frequency of each cookie given the date of interest; (Key: cookie name, Value: frequency of pair)
        self.max_freq = 0                   # Frequency of the most occurring cookie in a given date


    ##############################################################################
    ###################           Validation Checks           ####################
    ##############################################################################

    '''
        We are assuming that the cookie,timestamp format is consistent in the data given.
        Hence, the cookie name should already be valid as well as the timestamp. 
        For now, we do not want to pay attention to the time (in UTC), but rather the date.
    '''

    @staticmethod
    def valid_csv(filename: str) -> None:
        """
            Raises an error depending on whether the given file is a valid csv file or not.

            Params: filename (a string representing the name of a file of data).
            Returns: None, but raises an error if the file is not of the .csv format.
        """

        if filename[-4:] != '.csv':
            raise ValueError("Invalid file format. Requires CSV file.")


    @staticmethod
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

    def frequency_update(self, cookie_name: str):
        """
            This function updates the hashmap containing the frequency of cookie names in the given date.
            It also updates the maximum frequency if we reached a new maximum.

            Params:  cookie_name (the name of the cookie of interest).
            Returns: Nothing, but updates the frequency hashmap and maximum frequency of cookies up to this point.

            Runtime Complexity: O(1) since we are simply utilizing hashing functions.
            Space Complexity: O(n) where n is the number of unique cookies in the hashmap so far.
        """

        # Only consider cookie names that occur in our date of interest
        self.freq_map[cookie_name] = 1 + self.freq_map.get(cookie_name, 0)

        if self.freq_map[cookie_name] > self.max_freq:
            # Update the maximum frequency of all cookies
            self.max_freq = self.freq_map[cookie_name]


    def find_cookie_name_and_date(self, line: str) -> Tuple[str, str]:
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

        Cookie_Finder.valid_date(cookie_date)

        return cookie_name, cookie_date


    def full_traversal_search(self) -> None:
        """
            This function prints out the cookie that occurs the most within the given input date.

            Params: None
            Returns: Nothing. Instead, this function prints out the names of cookies that occur most often.

            Runtime Complexity: O(nm + n) where n is the number of rows in the cookies log and m is the number 
                                of chars in each row.
            Space Complexity: O(n) where n is the number of rows. This is because each row can contain a unique 
                            cookie with the given input date.
        """

        # Before anything, make sure the given file is a CSV file
        Cookie_Finder.valid_csv(self.filename)

        # Reset the member variables 
        self.freq_map = {}
        self.max_freq = 0

        with open(self.filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)        # Skip the header (i.e. "cookie,timestamp")

            for line in csv_reader:
                # line is in the form of [line contents: string]
                line = line[0]
                
                cookie_name, cookie_date = self.find_cookie_name_and_date(line)

                # Only obtain frequency of cookie if we have found our date of interest
                if cookie_date == self.date:
                    self.frequency_update(cookie_name)
        
        # No cookie found with the given date
        if len(self.freq_map.items()) == 0:
            print("No cookie(s) found.")

        else:
            # Print out all the cookie names with the maximum frequency
            for k, v in self.freq_map.items():
                if v == self.max_freq:
                    print(k)


    ##############################################################################
    ##########      Find Most Frequent Cookie Using Binary Search      ########### 
    ##############################################################################

    def binary_search(self, csv_data: List[str], left: int, right: int) -> Tuple[int, int]:
        """
            This is a helper function to most_active_cookie_binary_search(csv_file, date).
            We perform binary search on the rows of the cookies data to find the FIRST
            row with the given date.

            Params: csv_data (a list of strings containing the cookies log data).
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
            _, cookie_date = self.find_cookie_name_and_date(csv_data[mid])

            # Perform binary search to find the first date that is the same as the input date
            if self.date < cookie_date:
                left = mid + 1
            
            elif self.date > cookie_date:
                right = mid - 1
            
            else:
                left = right = mid
                
                # Return the first and second indices (so that we don't check the same index twice) 
                # of the given date
                return left, right + 1


        # No cookie found with the given date
        return -1, -1


    def most_active_cookie_binary_search(self) -> None:
        """
            This function is the overarching function that finds the most active cookie(s) using binary search.
            It serves as an alternative/better solution to the most_active_cookie function, which searches through all the rows
            of the given cookie log per function call.
            This function also depends on helper functions such as binary_search, find_cookie_name_and_date, and frequency_update.
            
            Params: None
            Returns: None, but prints out the most active cookie(s) in the given log.

            Runtime Complexity: O(mn + n) where m is the number of characters in each row and n is the number of rows in the log file.
                                In the worst case, all rows contain a unique cookie that appears in the given date. That means we stop the
                                binary search on the first iteration, and then iterate through the entire file to find all the cookie names.
            Space Complexity: O(n) where n is the number of rows. This is because each row can contain a unique cookie with the given input date.
        """

        # Before anything, make sure the given file is a CSV file
        Cookie_Finder.valid_csv(self.filename)

        # Reset the member variables 
        self.freq_map = {}
        self.max_freq = 0

        with open(self.filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)

            # Store each line of the cookies log into a list for easier access to cookies content
            csv_data = [line[0] for line in csv_reader]
            left, right = self.binary_search(csv_data, 0, len(csv_data) - 1)

            # At least one cookie exists with the given input date
            if left != -1:
                # Check left
                while left >= 0:
                    # Obtain the cookie name and date of current row
                    cookie_name, cookie_date = self.find_cookie_name_and_date(csv_data[left])

                    if cookie_date == self.date:
                        self.frequency_update(cookie_name)
                        left -= 1
                    else:
                        break

                # Check right
                while right < len(csv_data):
                    # Obtain the cookie name and date of current row
                    cookie_name, cookie_date = self.find_cookie_name_and_date(csv_data[right])

                    if cookie_date == self.date:
                        self.frequency_update(cookie_name)
                        right += 1
                    else:
                        break
                
                # Print out all the cookie names with the highest frequency
                for k, v in self.freq_map.items():
                    if v == self.max_freq:
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
    Cookie_Finder.valid_csv(filename)
    Cookie_Finder.valid_date(date)

    # Create a Cookie Finder object
    cookie_finder = Cookie_Finder(filename, date)

    # Two functions that find the most active cookie
    cookie_finder.full_traversal_search()                   # Full Traversal Method
    # print()
    # cookie_finder.most_active_cookie_binary_search()        # Binary Search Method


if __name__ == '__main__':
    """
        It's best to run one of these functions at a time.
    """

    # create_csv_file(data, 'cookie_log.csv')       # Create cookie logs from manual data
    # create_custom_csv_file(1000)                  # Create cookie logs from auto-generated data
    main()                                          # Run the functions to find most active cookie


