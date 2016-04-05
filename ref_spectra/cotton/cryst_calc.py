import os
import sys
import gparse
import seaborn as sns
from matplotlib import pyplot as plt
from glob import glob
from scipy.interpolate import interp1d

cryst = []
temps = glob('*K.csv')
# loop over temperature directories
for temp in temps:

    with open(temp) as f:
        lines = f.readlines()
        lines = [l.split(',') for l in lines]

    freqs = [float(l[0]) for l in lines if float(l[0]) > 100]
    intens = [float(l[1]) for l in lines if float(l[0]) > 100]
    min_intens = min(intens)
    intens = [i - min_intens for i in intens]

    interp = interp1d(freqs, intens, kind='cubic')

    numerator = interp(380) - interp(357)
    denom = interp(1096) - interp(940)
    cryst.append(numerator/denom)

    
temps = [int(t[:3]) for t in temps]
plt.scatter(temps, cryst)
plt.ylabel('Crystallinity')
plt.xlabel('Temperature (K)')
plt.show()
