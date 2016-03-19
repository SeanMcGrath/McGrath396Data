import os
import sys
import gparse
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

# plot setup
sns.set_context('poster')
sns.set_style('white')

# get options
stacked = '-s' in sys.argv or '--stacked' in sys.argv
infrared = '-i' in sys.argv or '--infrared' in sys.argv

# do config based on options
if infrared:
    y_axis_title = 'IR'
    offset_val = 120
    text_offset = 70
    if stacked:
        axis_range = [900, 1250, 0, 1600]
    else:
        axis_range = [900, 1250, 0, 600]
else:
    y_axis_title = 'Raman'
    offset_val = 8
    text_offset = 2
    if stacked:
        axis_range = [900, 1250, 0, 90]
    else:
        axis_range = [900, 1250, 0, 40]

# loop constants / vars
y_offset = 0
log_glob = sys.argv[-1]
top_dir = os.path.abspath('.')
temp_dirs = sorted([dir for dir in os.listdir('.') if len(dir) is 3 and dir is not '500'])

# loop over temperature directories
for dir in temp_dirs:
    print('entering ' + dir)
    os.chdir(dir)
    if infrared:
        spectra = [gparse.Spectrum.from_log_file(f, type='ir') for f in glob(log_glob)]
    else:
        spectra = [gparse.Spectrum.from_log_file(f) for f in glob(log_glob)]

    avg_function = lambda x: sum([s.fit_function(x)/len(spectra) for s in spectra])
    max_x = max([s.x_array()[-1] for s in spectra]) 
    x_array = gparse.util.linspace(0, max_x, 10000)

    if not stacked:
        plt.plot(x_array, [avg_function(x) for x in x_array], label=dir + 'K')
        plt.legend()
    else:
        plt.plot(x_array, [avg_function(x) + y_offset for x in x_array], label=dir + 'K')
        plt.annotate(dir + 'K', xy = (1200, text_offset +  y_offset))
        y_offset += offset_val

    os.chdir(top_dir)

# finish plot
plt.axis(axis_range)
plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
plt.ylabel(y_axis_title + ' Activity (arb. units)', fontsize=20)
plt.gca().tick_params(axis='both', which='major', labelsize='16')

plt.show()

