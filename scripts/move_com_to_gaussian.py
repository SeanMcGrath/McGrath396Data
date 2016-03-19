#!/bin/env/ python
# pass in "find -name *.com"

import sys
import os

destination = '/home/sean/Documents/thesis/gaussian/cellobiose'
args = sys.argv[1:]

for file in args:
    temp_time = os.path.dirname(file)[2:]
    com_file = os.path.basename(file)

    lines = []
    with open(file) as f:
        lines = f.readlines()
    lines = lines[:5] + lines[32:61]
    lines.append('\n')

    new_path = '{}/{}/1/2dp'.format(destination, temp_time)
    print('making ' + new_path)
    os.makedirs(new_path, exist_ok=True)
    new_file = new_path + '/' + com_file
    print('writing ' + new_file)
    with open(new_file, 'w') as f:
        [f.write(line) for line in lines]
