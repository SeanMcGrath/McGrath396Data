import os
import sys
import raman
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

# Choose stacked or normal plot
if '-s' in sys.argv or '--stacked' in sys.argv:
    stacked = True
else:
    stacked = False

sns.set_context('poster')

y_offset = 0
top_dir = os.path.abspath('.')
#temp_dirs = sorted([dir for dir in os.listdir('.') if len(dir) is 3])
temp_dirs = ['280']
for dir in temp_dirs:
    print('entering ' + dir)
    os.chdir(dir)

    spectra = [raman.Configuration.from_log_file(f).spectrum for f in glob('**/**/*.log')]
    avg_function = lambda x: sum([s.fit_function(x)/len(spectra) for s in spectra])
    max_x = max([s.x_array()[-1] for s in spectra]) 
    x_array = raman.util.linspace(0, max_x, 10000)

    if not stacked:
        plt.plot(x_array, [avg_function(x) for x in x_array], label=dir + 'K')
        plt.legend()
        plt.axis([900, 1250, 0, 35])
    else:
        plt.plot(x_array, [avg_function(x) + y_offset for x in x_array], label=dir + 'K')
        plt.annotate(dir + 'K', xy = (1000, 2 +  y_offset))
        y_offset += 8
        plt.axis([900, 1250, 0, 95])

    os.chdir(top_dir)

plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
plt.ylabel('Raman Activity (arb. units)', fontsize=20)
plt.gca().tick_params(axis='both', which='major', labelsize='16')

plt.show()

