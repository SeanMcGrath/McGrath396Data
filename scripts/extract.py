#!/bin/env/ python

import sys

args = sys.argv[1:]

for file in args:
    lines = []
    with open(file) as com_file:
        lines = com_file.readlines()
    lines.insert(1, '\n')
    lines.insert(3, '\n')
    lines[4] = '0 1\n'
    lines = lines[:5] + lines[32:61]
    lines.append('\n')

    new_file_name = file[:-3] + 'unit.com'
    with open(new_file_name, 'w') as new_file:
        [new_file.write(line) for line in lines]
