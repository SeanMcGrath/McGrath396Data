import os
import sys
import gparse
import functools
import seaborn as sns
from matplotlib import pyplot as plt
from glob import glob

# Constants
x_scale = 1.017
y_scale = 17

# loop constants / vars
log_glob1 = '**/1/2dp/*.log'
log_glob2 = '**/1/2dfp/*.log'
top_dir = os.path.abspath('.')
temp_dirs = [d for d in os.listdir() if d.endswith('K')]
temps = [int(f[:-1]) for f in temp_dirs]

cryst = []

# loop over temperature directories
for dir in temp_dirs:
    os.chdir(dir)

    spectra = []
    for f in glob(log_glob1) + glob(log_glob2):
        with open(f) as file:
            lines = file.readlines()
        if 'inished' in lines[-1]:
            spectra.append(gparse.Spectrum.from_log_file(f))
    try:
        avg_function = gparse.Spectrum.average_function(spectra)

        numerator = avg_function(380/x_scale) - avg_function(357/x_scale)
        denom = avg_function(1096/x_scale) - avg_function(940/x_scale)
        cryst.append(numerator/denom)

    except Exception as e:
        print(e)
    finally:
        os.chdir(top_dir)
    
plt.scatter(temps, cryst)
plt.ylabel('Crystallinity')
plt.xlabel('Temperature (K)')
plt.show()
