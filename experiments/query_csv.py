#!/usr/bin/env python3

# Very loosely based on https://github.com/RobustPerception/python_examples/blob/master/csv/query_csv.py

import csv
import requests
import sys

if len(sys.argv) != 7:
    print('Usage: {0} http://prometheus:9090 name query start end step'.format(sys.argv[0]))
    sys.exit(1)

response = requests.get('{0}/api/v1/query_range'.format(sys.argv[1]),
        params={'query': sys.argv[3], 'start': sys.argv[4], 'end': sys.argv[5], 'step': sys.argv[6]})
results = response.json()['data']['result'][0]

writer = csv.writer(sys.stdout)

# Header line
writer.writerow(['timestamp', sys.argv[2]])

# Write the samples.
for value in results['values']:
    writer.writerow([value[0], value[1]])
