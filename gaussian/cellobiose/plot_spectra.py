import os
import raman
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

plt.axis([900, 1250, 0, 35])
sns.set_context('poster')

y_offset = 0
temp_dirs = sorted([dir for dir in os.listdir('.') if len(dir) is 3])
for dir in temp_dirs:
    print('entering ' + dir)
    os.chdir(dir)

    spectra = [raman.Configuration.from_log_file(f).spectrum for f in glob('**/*.log')]
    avg_function = lambda x: sum([s.fit_function(x)/len(spectra) for s in spectra])
    max_x = max([s.x_array()[-1] for s in spectra]) 
    x_array = raman.util.linspace(0, max_x, 10000)

    plt.plot(x_array, [avg_function(x) for x in x_array], label=dir + 'K')
    plt.legend()

    os.chdir('..')

plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
plt.ylabel('Raman Intensity (arb. units)', fontsize=20)
plt.gca().tick_params(axis='both', which='major', labelsize='16')

plt.show()

