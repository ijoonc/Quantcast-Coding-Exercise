# Quantcast-Coding-Exercise

QuantCast Software Engineering Internship Coding Task 1

### Instructions

The cookie logs can be directly downloaded onto your computer as a CSV file. `cookie_log.csv` contains the data given to us in the problem statement. `more_cookie_log.csv` contains 1000 lines of auto-generated cookie data that is in sorted order by timestamp. 

There is a Python file called `cookie_log_generator.py` that can be used to generate cookie log files in CSV format. There are two functions.

The first is called `create_csv_file`, which requires manually created data in the form of `List[List[str]]` to be inputted as a parameter to the function. It will then convert each line in this data as a separate line in the CSV file.

The second is called `create_custom_csv_file`, which generates random cookie names, dates, and timestamps with valid values. There are also additional conditions near the end of the function to allow duplicate cookie names to exist. This makes it easier to test scenarios where there are more than one occurances of a cookie for a specified date (as opposed to a unique cookie per date).

The file with our main program is called `most_active_cookie.py`. This is our file of interest.

To run the program, we can give a command-line prompt in the form of `python ./most_active_cookie.py {csv file name such as cookie_log.csv} -d {date such as 2018-12-09}`.

To run the unit tests, we can use the command `python3 -m unittest most_active_cookie_test.py` where `most_active_cookie_test.py` is the Python file that contains all of our unit tests for each function in `most_active_cookie.py`.

### Assumptions

The main assumption I made when implementing this program is that the order of the printed cookies do not matter. For instance, when there are multiple cookies that are most active in a given date, the order of the printed cookies may differ from the expected output, but the cookie names themselves are the same. 

`Note:` the order of the cookie names are preserved in the `full_traversal_search` method, but not the main `most_active_cookie_binary_search` method within our `most_active_cookie.py` file.

If the order of the printed cookie names do matter, I have thought of a strategy that can account for this. In our binary search, we will first find the index of the row in our CSV data that contains the date of interest. Then, we will continue to move our left pointer to the left (or up the CSV file) until we have reached its end or the date of the row does not match the date of interest. We will do the same on the right side for the right pointer. As we move the left and right pointers in this manner, we will keep track of the cookie names and their occurrances in a hashmap through each iteration. We will also keep track of the maximum frequency of a cookie at each point in a variable.

These two pointers will now cover the range of rows that contain our date of interest. Our maximum frequency variable will contain the number of occurances of the cookie(s) that occur the most in the given date.

We will start from the left pointer and iterate through until we reach the right pointer. In each iteration, we will check the occurrance of each cookie (using our hashmap), and if it equals the maximum frequency, we will print out the cookie name.

At the end of the iteration, we will have printed out all the cookie names with the most occurances on each separate line. 

This method ensures that the order of the cookie names are preserved while also utilizing binary search so that we do not have process every line of the data for each function call.

### My Intuition on Tackling this Problem

I have initially approached this problem using the brute force solution. Specifically, I have iterated through each row of the CSV file and obtained the cookie name, the date, and its frequency. However, this method requires us to iterate through the entire CSV file for each function call. This idea didn't rest comfortably for me, so I tried to think of a more efficient solution.

I noticed that the instructions mentioned that the timestamps of the cookie data were in order. This made me think of implementing a potential binary search solution. Now, instead of iterating through the entire file each time the function is called, we instead search for the date of interest. Then, extract the cookie name, date, and frequency for only the cookies that appear in our date of interest. This reduces a lot of the unnececssary computation! 

Of course, we must note that in the worst case, all cookies will appear in the date of interest. That means our binary search algorithm will halt on the first line it encounters, and we must traverse through the entire file to obtain the cookie names and frequency. However, the worst case scenario for our binary search algorithm has identical or very similar performance to our `full_traversal_search` algorithm. The worst case scenario is very unlikely, indicating that the binary search algorithm should be more efficient most of the time!

`Note: the Runtime and Space Complexities of each function is presented in the most_active_cookie.py file`. 

Now, after implementing these functions, I still felt somewhat unsatisfied with my code. After re-reading through the instructions, I have found a few key words that stood out to me: `maintainable`, `extendable`, and `clean abstractions`. Hence, I have decided to combine all of my implementations into a class. Classes make it so that users can create objects and easily call functions of their interest. Additionally, I was able to abstract most of the higher-level implementation details since this makes it easier for the users to utilize my functions. All helper/main functions can be maintained within the class for specific object-usage. To further extend this implementation, we can provide more helper functions to abstract away more complicated details from complex algorithms such as the binary search algorithm (`most_active_cookie_binary_search`).

To further extend my implementations, I have created custom cookie log data generators. These generators can be found in `cookie_log_generator.py` as mentioned above. The `data` presented in that file is the exact same data as shown in the problem statement. Again, I have also implemented another function `create_custom_csv_file` that can create auto-generated cookie data with as many rows as the user desires. This makes it easier to test my functions with unseen, large amounts of data. 

### Summary

Overall, this coding question really pushed me to utilize and combine the core skills I have developed throughout my programming experiences, including algorithmic thinking, unit testing, and generating large amounts of data. This was a very fun and exciting problem to tackle, and it really reinforced my fundamentals as a programmer. Through this experience, I really believe that I have enhanced my skills to develop production-grade code. I really appreciate your time for looking over my implementation and for giving me this opportunity to solve an immersive, challenging problem!

