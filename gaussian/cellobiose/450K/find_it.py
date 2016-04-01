import gparse
import seaborn
from glob import glob
from matplotlib import pyplot as plt

ax = plt.gca()
for f in glob('**/1/2dp/*.log'):
 	print(f)
 	spectrum = gparse.Spectrum.from_log_file(f)
 	spectrum.plot(ax, label=f)

plt.legend()
plt.show()
