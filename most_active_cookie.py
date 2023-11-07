import argparse
import csv


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

def create_csv_file(data):
    filename = 'cookie_log.csv'
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in data:
            csv_writer.writerow(line)


def most_active_cookie(csv_file, date):
    freq = {}
    max_freq = 0

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for line in csv_reader:
            line = line[0]
            separated_contents = line.split(',')
            more_separated_contents = separated_contents[1].split('T')

            cookie_name = separated_contents[0]
            cookie_date = more_separated_contents[0]

            freq[(cookie_name, cookie_date)] = 1 + freq.get((cookie_name, cookie_date), 0)

            if date == cookie_date and freq[(cookie_name, cookie_date)] > max_freq:
                max_freq = freq[(cookie_name, cookie_date)]
    
            
    for k, v in freq.items():
        if k[1] == date and v == max_freq:
            print(k[0])


def most_active_cookie_binary_search(csv_file, date):
    date_int = int(''.join(date.split('-')))
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        csv_data = [line[0] for line in csv_reader]
        l, r = 0, len(csv_data) - 1

        while l <= r:
            # Can lead to integer overflow
            # mid = (r + l) // 2
            mid = l + (r - l) // 2

            separated_contents = csv_data[mid].split(',')
            more_separated_contents = separated_contents[1].split('T')
            cookie_date = more_separated_contents[0]
            cookie_date = int(''.join(cookie_date.split('-')))

            if date_int < cookie_date:
                l = mid + 1
            
            elif date_int > cookie_date:
                r = mid - 1
            
            else:
                l = r = mid
                break
    
    
    counter = {}
    max_freq = 0

    # Left pointer
    while l >= 0:
        separated_contents = csv_data[l].split(',')
        more_separated_contents = separated_contents[1].split('T')
        cookie_date = more_separated_contents[0]
        cookie_date = int(''.join(cookie_date.split('-')))

        if cookie_date == date_int:
            separated_contents = csv_data[l].split(',')
            cookie_name = separated_contents[0]

            counter[cookie_name] = 1 + counter.get(cookie_name, 0)

            if counter[cookie_name] > max_freq:
                max_freq = counter[cookie_name]

            l -= 1
        
        else:
            break

    # Right pointer
    r += 1
    while r < len(csv_data):
        separated_contents = csv_data[r].split(',')
        more_separated_contents = separated_contents[1].split('T')
        cookie_date = more_separated_contents[0]
        cookie_date = int(''.join(cookie_date.split('-')))

        if cookie_date == date_int:
            separated_contents = csv_data[r].split(',')
            cookie_name = separated_contents[0]

            counter[cookie_name] = 1 + counter.get(cookie_name, 0)

            if counter[cookie_name] > max_freq:
                max_freq = counter[cookie_name]

            r += 1
        
        else:
            break

    for k, v in counter.items():
        if v == max_freq:
            print(k)
    



        



def main():
    parser = argparse.ArgumentParser(description="Find the most active cookie on a certain day.")
    parser.add_argument('filename', help='Path to the CSV file containing the cookie data.')
    parser.add_argument('-d', '--date', help="Date for the most active cookie (YYYY-MM-DD)", required=True)

    args = parser.parse_args()

    filename = args.filename
    date = args.date

    # print(f"Filename: {filename}")
    # print(f"Date: {date}")

    most_active_cookie_binary_search(filename, date)


if __name__ == '__main__':
    # create_csv_file(data)
    main()


