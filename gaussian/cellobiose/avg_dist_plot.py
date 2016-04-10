import gparse
import os
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from glob import glob

sns.set_context('talk')
sns.set_style('white')

temp_dirs = sorted([dir for dir in os.listdir() if dir.endswith('K')])
temps = [int(t[:-1]) for t in temp_dirs]
top_dir = os.getcwd()

avgs = []
stds = []

for dir in temp_dirs:
    os.chdir(dir)
    logs = glob('**/1/**/*.log')
    matrices = [gparse.DistanceMatrix.from_log_file(log) for log in logs]
    avg = sum([m.average for m in matrices]) / len(matrices)
    avgs.append(avg)
    std = np.std([m.average for m in matrices]) / len(matrices)
    stds.append(std)
    print(dir, avg, std)
    os.chdir(top_dir)
    
f, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.plot(temps, avgs)
ax1.set_ylabel('Average interatomic distance (nm)')
ax2.plot(temps, stds)
ax2.set_ylabel('Interatomic distance standard deviation (nm)')
ax2.set_xlabel('Temperature(K)')
plt.show()
plt.show()
