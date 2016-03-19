import gparse
from matplotlib import pyplot as plt
from glob import glob

logs = glob('**/1/2dfp/*.log')

for log in logs:
    ax = plt.gca()
    spec = gparse.Spectrum.from_log_file(log)
    spec.plot(ax)
    print(log)
    plt.show()
