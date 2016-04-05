import os
import sys
import gparse
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

# Constants
x_scale = 1.017
y_scale = 10.9167

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
    offset_val = 80
    text_offset = 2
    if stacked:
        axis_range = [900, 1250, 0, 90]
    else:
        axis_range = [900, 1400, 0, 210]

# loop constants / vars
y_offset = 0
log_glob = sys.argv[-1]
top_dir = os.path.abspath('.')
#temp_dirs = sorted([dir for dir in os.listdir('.') if dir.endswith('K')])
temp_dirs = ['400K', '423K', '473K', '483K'] #['300K', '350K', '400K', '423K', '450K', '473K', '483K', '493K', '500K']

# loop over temperature directories
for dir in temp_dirs:
    print('entering ' + dir)
    os.chdir(dir)
    try:
        if infrared:
            spectra = [gparse.Spectrum.from_log_file(f, type='ir') for f in glob(log_glob)]
        else:
           spectra = [gparse.Spectrum.from_log_file(f) for f in glob(log_glob)]
        avg_function = lambda x: sum([s.fit_function(x)/len(spectra) for s in spectra])
        max_x = max([s.x_array()[-1] for s in spectra]) 
        x_array = gparse.util.linspace(0, max_x, 10000)

        if not stacked:
            plt.plot(x_array, [avg_function(x)*y_scale for x in x_array], label=dir)
            plt.legend()
        else:
            plt.plot(x_array, [avg_function(x)*y_scale + y_offset for x in x_array], label=dir)
            plt.annotate(dir + 'K', xy = (1200, text_offset +  y_offset))
            y_offset += offset_val

    except ValueError:
        pass
    finally:
        os.chdir(top_dir)

# finish plot
plt.axis(axis_range)
plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
plt.ylabel(y_axis_title + ' Activity (arb. units)', fontsize=20)
plt.gca().tick_params(axis='both', which='major', labelsize='16')

plt.show()

