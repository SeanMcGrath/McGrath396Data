from glob import glob
from matplotlib import pyplot as plt

for f in sorted(glob('*K.csv')):
    with open(f) as csv:
        lines = csv.readlines()
    lines = [line.split(',') for line in lines]
    freqs = [float(line[0]) for line in lines if float(line[0]) < 1200]
    intens = [float(line[1]) for line in lines if float(line[0]) < 1200]
    max_index = intens.index(max(intens))
    max_freq = freqs[max_index]
    temp = float(f[:3])
    print('{},{}'.format(temp, max_freq))
