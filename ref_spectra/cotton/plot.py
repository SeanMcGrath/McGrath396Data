import seaborn as sns
from glob import glob
from matplotlib import pyplot as plt

sns.set(context='poster', style='white', font_scale=1.2)

def parse(f):
    with open(f) as the_file:
        lines = [line.split(',') for line in the_file.readlines()]
    freqs = [float(line[0]) for line in lines]
    intens = [float(line[1]) for line in lines]
    return freqs, intens

fig = plt.figure(figsize=(16, 6))
ax = plt.subplot(111)

for f in sorted(glob('cotton*.csv')):
    temp = ''.join([char for char in f if char.isdigit()])
    freq, intens = parse(f)
    ax.plot(freq, intens, label=str(temp) + ' $^\circ$C')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.xlim(0, 1700)

plt.xlabel('Frequency (cm$^{-1}$)')
plt.ylabel('Raman Activity (arb. units)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('plot.eps')
plt.savefig('plot.png')
plt.show()
