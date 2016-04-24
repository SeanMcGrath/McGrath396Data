import os
import sys
import gparse
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

# Constants
ref_file = '/home/sean/Documents/thesis/ref_spectra/cotton/350K.csv'
sim_file = '/home/sean/Documents/thesis/gaussian/cellobiose/350K/8000ps/1/gdp/8000.log'

# plot setup
sns.set(context='poster', style='white', font_scale=1.3)

axis_range = [210, 1650, 0, 1.1]

with open(ref_file) as ref:
    lines = ref.readlines()
split_lines = [line.split(',') for line in lines]
freqs = [float(line[0]) for line in split_lines if float(line[0]) > 200]
intens = [float(line[1]) for line in split_lines if float(line[0]) > 200]
min_intens = min(intens)
intens = [i - min_intens for i in intens]
max_intens = max(intens)
plt.plot(freqs, [i/max_intens for i in intens], label='Experimental', color='r')

spectrum = gparse.Spectrum.from_log_file(sim_file)
max_x = max(freqs)
x_array = gparse.util.linspace(0, max_x, 10000)
y_array = [spectrum.fit_function(x) for x in x_array]
max_y = max(y_array)

plt.plot(x_array, [y/max_y for y in y_array], label='Simulated', color='k')

plt.text(0.1, 0.7, '300K', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
plt.gca().locator_params(axis='y', nbins=2)
plt.axis(axis_range)
plt.legend()
plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
plt.ylabel('Normalized Spectral Intensity')

plt.show()
