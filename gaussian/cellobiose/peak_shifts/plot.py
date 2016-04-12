import numpy as np
import sys
from matplotlib import pyplot as plt
import seaborn as sns

sns.set(context='poster', style='white', font_scale=1.2)

exp = sys.argv[1]
sim = sys.argv[2]

with open(exp) as main:
    main_lines = main.readlines()
    main_lines = [line.split(',') for line in main_lines]
main_temps = [float(line[0]) for line in main_lines]
main_freqs = [float(line[1]) for line in main_lines]

with open(sim) as sim:
    sim_lines = sim.readlines()
    sim_lines = [line.split(',') for line in sim_lines]
sim_temps = [float(line[0])*1.017 for line in sim_lines]
sim_freqs = [float(line[1]) for line in sim_lines]

main_fit = np.polyfit(main_temps, main_freqs, 1)
sim_fit = np.polyfit(sim_temps, sim_freqs, 1)
main_slope = 'slope: {0:0.2f}'.format(main_fit[0]) + ' cm$^{-1}$K$^{-1}$'
sim_slope = 'slope: {0:0.2f}'.format(sim_fit[0]) + ' cm$^{-1}$K$^{-1}$'
print(main_slope, sim_slope)
main_func = np.poly1d(main_fit)
sim_func = np.poly1d(sim_fit)

x_arr = np.linspace(min(sim_temps), max(sim_temps), 1000)

plt.scatter(sim_temps, sim_freqs, label='simulation', c='k')
plt.scatter(main_temps, main_freqs, label='experiment', c='r')
plt.plot(x_arr, [main_func(x) for x in x_arr], 'r--')
plt.plot(x_arr, [sim_func(x) for x in x_arr], 'k--')

plt.ylabel('Main Peak Wavenumber (cm$^{-1}$)')
plt.xlabel('Temperature (K)')
plt.text(340, 1088,  main_slope, fontsize=16)
plt.text(340, 1080, sim_slope, fontsize=16)
plt.legend()
plt.tight_layout()
plt.show()
