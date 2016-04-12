import sys
from glob import glob
from matplotlib import pyplot as plt

min_freq = float(sys.argv[1])
max_freq = float(sys.argv[2])

for f in sorted(glob('*K.csv')):
    with open(f) as csv:
        lines = csv.readlines()
    lines = [line.split(',') for line in lines]
    freqs = [float(line[0]) for line in lines if float(line[0]) > min_freq and float(line[0]) < max_freq]
    intens = [float(line[1]) for line in lines if float(line[0]) > min_freq and float(line[0]) < max_freq]
    max_index = intens.index(max(intens))
    max_freq = freqs[max_index]
    temp = float(f[:3])
    if temp < 484:
        print('{},{}'.format(temp, max_freq))
