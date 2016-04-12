import gparse
from glob import glob
from matplotlib import pyplot as plt
import seaborn as sns

#ax = plt.gca()
#reporter = gparse.PeakReporter(glob('*.log')[0], heavy_only=True, most_sig=True)
#reporter.report(plt=plt)

assigner = gparse.PeakAssigner(glob('*.log')[0])

print(assigner.closest_freq(600).most_significant_atoms())
