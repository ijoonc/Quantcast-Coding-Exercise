import unittest
import sys
import subprocess
from most_active_cookie import Cookie_Finder
from most_active_cookie import main

class TestMostActiveCookie(unittest.TestCase):
    """
        Test Suite for the Most Active Cookie.
        Although there are two methods defined to find the most active cookie (Full Traversal & Binary Search),
        we will be testing on the Binary Search Method as this will be the algorithm that we will choose throughout
        this problem.

        Testing Method: Python's Unittests.
    """

    def test_valid_csv_file(self):
        """
            Test whether the given filename is a valid CSV file.
        """

        # Valid CSV file
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-09']
        self.assertIsNone(main())

        # Another valid CSV file
        sys.argv = ['most_active_cookie.py', 'more_cookie_log.csv', '-d', '2018-12-09']
        self.assertIsNone(main())


    def test_invalid_csv_file(self):
        """
            Test whether the given filename is an invalid CSV file.
        """

        # The 'v' is removed from '.csv
        sys.argv = sys.argv = ['most_active_cookie.py', 'cookie_log.cs', '-d', '2018-12-09']
        with self.assertRaises(ValueError):
            main()
        
        # This file does not exist
        sys.argv = sys.argv = ['most_active_cookie.py', 'no_file.csv', '-d', '2018-12-09']
        with self.assertRaises(FileNotFoundError):
            main()

        # This is not a CSV file
        sys.argv = sys.argv = ['most_active_cookie.py', 'most_active_cookie.py', '-d', '2018-12-09']
        with self.assertRaises(ValueError):
            main()
    
    
    def test_valid_date(self):
        """
            Test whether the given date is a valid date (as a string).
        """

        # Valid date
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-09']
        self.assertIsNone(main())

        # Another valid date
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-09']
        self.assertIsNone(main())

        # Valid date but doesn't exist in CSV file
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2023-01-01']
        self.assertIsNone(main())

        
    def test_invalid_date(self):
        """
            Test whether the given date is invalid.
        """

        # Invalid date 1
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-0']
        with self.assertRaises(ValueError):
            main()

        # Invalid date 2
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-']
        with self.assertRaises(ValueError):
            main()

        # Invalid date 3
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '201-12-09']
        with self.assertRaises(ValueError):
            main()

        # Invalid date 4
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '2018-1-09']
        with self.assertRaises(ValueError):
            main()

        # Invalid date 5
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d', '--']
        with self.assertRaises(SystemExit):
            main()

        # No date input
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv', '-d']
        with self.assertRaises(SystemExit):
            main()

        # No date command
        sys.argv = ['most_active_cookie.py', 'cookie_log.csv']
        with self.assertRaises(SystemExit):
            main()
    

    def test_cookie_finder_initialization(self):
        """
            Tests the initial conditions of a Cookie Finder object upon creation.
        """

        cookie_finder = Cookie_Finder('cookie_log.csv', '2018-12-09')
        expected_freq_map = {}
        expected_max_freq = 0
        expected_filename = 'cookie_log.csv'
        expected_date = '2018-12-09'

        self.assertEqual(cookie_finder.freq_map, expected_freq_map)
        self.assertEqual(cookie_finder.max_freq, expected_max_freq)
        self.assertEqual(cookie_finder.filename, expected_filename)
        self.assertEqual(cookie_finder.date, expected_date)

        cookie_finder2 = Cookie_Finder('cookie_log.csv', '2018-12-08')
        expected_freq_map2 = {}
        expected_max_freq2 = 0
        expected_filename2 = 'cookie_log.csv'
        expected_date2 = '2018-12-08'

        self.assertEqual(cookie_finder2.freq_map, expected_freq_map2)
        self.assertEqual(cookie_finder2.max_freq, expected_max_freq2)
        self.assertEqual(cookie_finder2.filename, expected_filename2)
        self.assertEqual(cookie_finder2.date, expected_date2)


    def test_frequency_update(self):
        """
            Tests whether the Cookie Finder's member variables are updated with 
            each call of the frequency_update() function.
        """

        cookie_finder = Cookie_Finder('cookie_log.csv', '2018-12-09')

        # Assume that this cookie appears within the given date
        cookie_finder.frequency_update('PG5h4u7zpHtq3Omy')              # Example of Cookie Name

        checker = {'PG5h4u7zpHtq3Omy': 1}
        self.assertEqual(cookie_finder.freq_map, checker)
        self.assertEqual(cookie_finder.max_freq, 1)

        # Same Cookie
        cookie_finder.frequency_update('PG5h4u7zpHtq3Omy') 
        checker = {'PG5h4u7zpHtq3Omy': 2}
        self.assertEqual(cookie_finder.freq_map, checker)
        self.assertEqual(cookie_finder.max_freq, 2)

        # New Cookie
        cookie_finder.frequency_update('Lzg3P1WfuU4fth9g') 
        checker = {'PG5h4u7zpHtq3Omy': 2, 'Lzg3P1WfuU4fth9g': 1}
        self.assertEqual(cookie_finder.freq_map, checker)
        self.assertEqual(cookie_finder.max_freq, 2)
        

    def test_find_cookie_name_and_date(self):
        """
            Tests whether the function find_cookie_name_and_date() returns the correct cookie name and date
            for a given line in the cookie logs.
        """

        # First example
        cookie_finder = Cookie_Finder('cookie_log.csv', '2018-12-09')
        cookie_name, cookie_date = cookie_finder.find_cookie_name_and_date("AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00")
        self.assertEqual(cookie_name, "AtY0laUfhglK3lC7")
        self.assertEqual(cookie_date, "2018-12-09")

        # Second example
        cookie_name, cookie_date = cookie_finder.find_cookie_name_and_date("SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00")
        self.assertEqual(cookie_name, "SAZuXPGUrfbcn5UA")
        self.assertEqual(cookie_date, "2018-12-09")

        # Third example with different cookie and CSV file
        cookie_finder2 = Cookie_Finder('more_cookie_log.csv', '2023-12-26')
        cookie_name2, cookie_date2 = cookie_finder2.find_cookie_name_and_date("QIRTZYrZcfijihAr,2023-12-26T02:29:00+00:00"
)
        self.assertEqual(cookie_name2, "QIRTZYrZcfijihAr")
        self.assertEqual(cookie_date2, "2023-12-26")
    
    def test_full_traversal_search(self):
        """
            Tests the FULL TRAVERSAL method of finding the most active cookie.
            We will use the subprocess method instead of StringIO since the testing code is much cleaner.

            Make sure the main() function in most_active_cookie.py utilizes the full_traversal_search method only.
        """


        # First given test case
        output = ['python', './most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-09']
        processed_result = subprocess.check_output(output, text=True)
        self.assertEqual(processed_result, "AtY0laUfhglK3lC7\n")

        # Second given test case
        output2 = ['python', './most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-08']
        processed_result = subprocess.check_output(output2, text=True)

        expected_output_set = {"SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"}
        actual_output_set = set(processed_result.strip().split('\n'))

        self.assertEqual(expected_output_set, actual_output_set)        # Assume that order of cookies do not matter

        # Third test case using custom generated dataset
        output2 = ['python', './most_active_cookie.py', 'more_cookie_log.csv', '-d', '2023-10-05']
        processed_result = subprocess.check_output(output2, text=True)
        self.assertEqual(processed_result, "fBsaJfYNabwaiSSu\n")


    def test_binary_search(self):
        """
            Tests the binary search method, which serves as a helper method to the binary search algorithm
            to find the most active cookie.
        """

        # Given data
        csv_data = [
            "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00",
            "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00",
            "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00",
            "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00",
            "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00",
            "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00",
            "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00",
            "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00",
        ]

        cookie_finder = Cookie_Finder('cookie_log.csv', '2018-12-09')

        # Look for the date '2018-12-09'
        left, right = cookie_finder.binary_search(csv_data, 0, len(csv_data) - 1)
        self.assertEqual(left, 3)
        self.assertEqual(right, 4)

        # Look for the date '2018-12-08'
        cookie_finder2 = Cookie_Finder('cookie_log.csv', '2018-12-08')
        left, right = cookie_finder2.binary_search(csv_data, 0, len(csv_data) - 1)
        self.assertEqual(left, 5)
        self.assertEqual(right, 6)

        # Look for the date '2023-01-01' which doesn't exist in the data
        cookie_finder3 = Cookie_Finder('cookie_log.csv', '2023-01-01')
        left, right = cookie_finder3.binary_search(csv_data, 0, len(csv_data) - 1)
        self.assertEqual(left, -1)
        self.assertEqual(right, -1)
    

    def test_active_cookie_binary_search(self):
        """
            Tests the BINARY SEARCH method of finding the most active cookie.
            We will use the subprocess method instead of StringIO since the testing code is much cleaner.

            Make sure the main() function in most_active_cookie.py utilizes the active_cookie_binary_search method only.
        """

        # First given test case
        output = ['python', './most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-09']
        processed_result = subprocess.check_output(output, text=True)
        self.assertEqual(processed_result, "AtY0laUfhglK3lC7\n")

        # Second given test case
        output2 = ['python', './most_active_cookie.py', 'cookie_log.csv', '-d', '2018-12-08']
        processed_result = subprocess.check_output(output2, text=True)

        expected_output_set = {"SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"}
        actual_output_set = set(processed_result.strip().split('\n'))

        self.assertEqual(expected_output_set, actual_output_set)            # Assume that order of cookies do not matter

        # Third test case using custom generated dataset
        output2 = ['python', './most_active_cookie.py', 'more_cookie_log.csv', '-d', '2023-10-05']
        processed_result = subprocess.check_output(output2, text=True)
        self.assertEqual(processed_result, "fBsaJfYNabwaiSSu\n")


if __name__ == '__main__':
    unittest.main()

