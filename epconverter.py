#!/usr/bin/env python
# -*- coding: utf-8 -*- 

""" 

    Takes all E-Prime raw data files in the script directory and
    converts them to csv files.

    Author: Gunnar Norrman

"""
import sys
import os
import csv
import glob

def epconverter(src, dest):

    # Initiate some variables
    raw = []
    data = []
    max_level = 0

    # Import raw data to list by row
    with open(src, 'r') as source:
        for line in source.readlines():
            line_values = line.replace('\00', '').strip()

            # Find max level in experiment for use later
            if 'Level:' in line_values:
                value = line_values.split()
                max_level = int(value[1]) if int(value[1])>int(max_level) else int(max_level)

            # Add stripped line to a datalist
            raw.append(line_values) 

    # Get index for the end of the header section and save headers for Subject and Session.
    header_end_i = [i for i, v, in enumerate(raw) if "*** Header End ***" in v]
    header_data = [r for r in raw[1:header_end_i[0]] if r.split(': ')[0] in ['Subject', 'Session']]
    header_data = [r.split(': ') for r in raw[1:header_end_i[0]]]

    # Identify trial start and end
    start_i = [i+3 for i, v, in enumerate(raw) if ' '.join(['Level:', str(max_level)]) in v]
    end_i = [i for i, v, in enumerate(raw) if "*** LogFrame End ***" in v]

    # Prepare headers and data dictionary
    headers = [a.split(':')[0] for a in raw[start_i[0]:end_i[0]] if a!='']
    dct = {key:[] for key in headers} 

    # Create data dictionary
    for i in range(0, len(start_i)):
        trial = [r.split(':') for r in raw[start_i[i]:end_i[i]] if len(r)>1]
        [dct[t[0]].append(t[1].strip()) for t in trial if len(t)>1]

    # Convert to ordered data
    # header_data = [row.split(':') for row in header_data]
    header_data_keys = [row[0] for row in header_data]
    header_data_values = [row[1].strip() for row in header_data]


    # Create data frame with headers
    data.append(header_data_keys + headers)

    # Append rows to data frame
    for i in range(0, len(dct[headers[0]])):
        data.append(header_data_values + [dct[k][i] for k in headers])

    # Export data frame as CSV
    with open(dest, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        for trial in data:
            a.writerow(trial)


if len(sys.argv) > 1:
	arg = sys.argv[1]

else:
	sys.exit('No arguments supplied.')


if os.path.isfile(arg):

	files = [arg]

elif os.path.isdir(arg):

	files = glob.glob(''.join([files, '*.txt']))

else:

	sys.exit('Please select a file or a directory.')

for file in files:

	name, ext = os.path.splitext(file)
	print(name)
	epconverter(file, name + '.csv')
