import csv
from datetime import datetime
import os


def write_to_csv(data, filename = None):
    filename = 'result.csv'
    rows = read_from_csv(filename)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        row = [datetime.now().date()] + data
        rows.append(row)
        for row in rows:
            writer.writerow(row)

def read_from_csv(filename='result.csv'):
    rows = []
    if not os.path.exists(filename):
        # Create the file and immediately close it, making it empty if it didn't exist
        open(filename, 'a').close()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return rows[-49:]
# Example usage
read_from_csv()