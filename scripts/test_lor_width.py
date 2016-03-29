import gparse
import os
import sys
import gparse
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import quad
from glob import glob
from matplotlib import pyplot as plt

def spec_diff(spec1, spec2, x_min, x_max):
    diff_func = lambda x: np.abs(spec1(x) - spec2(x))
    return quad(diff_func, x_min, x_max)

sns.set_style('white')
sns.set_context('poster')

ref_file = sys.argv[1]

with open(ref_file) as ref:
    lines = ref.readlines()
split_lines = [line.split(',') for line in lines]
freqs = [float(line[0]) for line in split_lines if float(line[0]) >= 890 and float(line[0]) <= 1260]
intens = [float(line[1]) for line in split_lines if float(line[0]) >= 890 and float(line[0]) <= 1260]

x_array = np.linspace(925, 1200, 1000)
ref_x_array = np.linspace(900, 1250, 1000)

logs = glob('**/*.log', recursive=True)

diff_integrals = []

for width in [3.3]:#np.arange(3, 5, .1):
    spectra = [gparse.Spectrum.from_log_file(log, width=width) for log in logs if '2dfp' in log]
    avg = gparse.Spectrum.average_function(spectra)
    y_array = np.array([avg(x) for x in ref_x_array])
    y_scaling_factor = (max(intens)-min(intens))/(max(y_array)-min(y_array))
    scaled_y = y_scaling_factor*y_array
    min_y = min(intens) - min(scaled_y)
    scaled_intensities = [i - min_y for i in intens]
    x_scaling_factor = freqs[np.argmax(scaled_intensities)]/ref_x_array[np.argmax(scaled_y)]
    scaled_x = ref_x_array*x_scaling_factor

    ref_func = interp1d(freqs, scaled_intensities, kind='cubic')
    computed_func = interp1d(scaled_x, scaled_y, kind='cubic')
#    integral = spec_diff(ref_func, computed_func, 1064, 1121)[0]
#    print(width, integral)
#    diff_integrals.append((width, integral))

#print(sorted(diff_integrals, key=lambda x: x[1]))
#print(x_scaling_factor, y_scaling_factor)
plt.plot(x_array, ref_func(x_array), label='experimental')
plt.plot(x_array, computed_func(x_array), label='computed')
plt.legend()
plt.show()
