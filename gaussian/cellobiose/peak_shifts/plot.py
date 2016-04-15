import numpy as np
import sys
from matplotlib import pyplot as plt
import seaborn as sns

def plot(exp, sim, ax):
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

    ax.scatter(sim_temps, sim_freqs, label='simulation', c='k')
    ax.scatter(main_temps, main_freqs, label='experiment', c='r')
    ax.plot(x_arr, [main_func(x) for x in x_arr], 'r--')
    ax.plot(x_arr, [sim_func(x) for x in x_arr], 'k--')
    ax.locator_params(axis='y', nbins=4)

    #plt.ylabel('Main Peak Wavenumber (cm$^{-1}$)')
    ax.set_xlabel('Temperature (K)')
    #plt.text(340, 1088,  main_slope, fontsize=16)
    #plt.text(340, 1080, sim_slope, fontsize=16)
    ax.legend()


sns.set(context='poster', style='white', font_scale=1.5)

exp1 = 'mainpeak.csv'
sim1 = 'peak63.csv'
exp2 = '1330peak.csv'
sim2 = 'mode87.csv'

f, (ax1, ax2) = plt.subplots(1, 2)

plot(exp1, sim1, ax1)
plot(exp2, sim2, ax2)
ax1.set_ylabel('Frequency (cm$^{-1}$)')
ax2.yaxis.tick_right()
plt.gcf().subplots_adjust(wspace=0.1)

plt.tight_layout()
plt.show()
