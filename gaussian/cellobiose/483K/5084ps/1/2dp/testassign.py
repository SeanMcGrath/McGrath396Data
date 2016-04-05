import gparse
from glob import glob
from matplotlib import pyplot as plt
import seaborn as sns

ax = plt.gca()
reporter = gparse.PeakReporter(glob('*.log')[0])
reporter.report(plt=plt)
