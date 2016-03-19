import gparse
from matplotlib import pyplot as plt

for width in range(1, 10):
    ax = plt.gca()
    spec = gparse.Spectrum.from_log_file('5000.log', width=width)
    spec.plot(ax)
    plt.xlim(950, 1250)
    plt.ylim(0, 40)
    print(width)
    plt.show()
