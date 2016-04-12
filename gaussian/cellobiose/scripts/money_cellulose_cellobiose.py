import os
import sys
import gparse
import functools
import matplotlib
import seaborn as sns
from glob import glob
import matplotlib.pyplot as plt

def suplabel(axis,label,label_prop=None,
             labelpad=5,
             ha='center',va='center'):
    ''' Add super ylabel or xlabel to the figure
    Similar to matplotlib.suptitle
    axis       - string: "x" or "y"
    label      - string
    label_prop - keyword dictionary for Text
    labelpad   - padding from the axis (default: 5)
    ha         - horizontal alignment (default: "center")
    va         - vertical alignment (default: "center")
    '''
    fig = plt.gcf()
    xmin = []
    ymin = []
    for ax in fig.axes:
        xmin.append(ax.get_position().xmin)
        ymin.append(ax.get_position().ymin)
    xmin,ymin = min(xmin),min(ymin)
    dpi = fig.dpi
    if axis.lower() == "y":
        rotation=90.
        x = xmin-float(labelpad)/dpi
        y = 0.5
    elif axis.lower() == 'x':
        rotation = 0.
        x = 0.5
        y = ymin - float(labelpad)/dpi
    else:
        raise Exception("Unexpected axis: x or y")
    if label_prop is None: 
        label_prop = dict()
    plt.text(x,y,label,rotation=rotation,
               transform=fig.transFigure,
               ha=ha,va=va,
               **label_prop)

# plot setup
sns.set(context='poster', style='white', font_scale=1.2)

cellulose_ref_dir = '/home/sean/Documents/thesis/ref_spectra/cotton'
cellobiose_ref_dir = '/home/sean/Documents/thesis/ref_spectra/cellobiose'
cellulose_ref_files = [os.path.abspath(os.path.join(cellulose_ref_dir,f)) for f in os.listdir(cellulose_ref_dir) if 'bak' not in f]
cellobiose_ref_files = [os.path.abspath(os.path.join(cellobiose_ref_dir,f)) for f in os.listdir(cellobiose_ref_dir) if 'bak' not in f]

x_scale = 1.017
axis_range = [210, 1650, -0.05, 1.1]

log_glob1 = '**/1/2dp/*.log'
log_glob2 = '**/1/2dfp/*.log'
top_dir = os.path.abspath('.')
temp_dirs = ['423K', '473K']

# loop over temperature directories
for ax, dir in zip(plt.subplots(len(temp_dirs), sharex=True, sharey=True)[1][::-1], temp_dirs):
    print('entering ' + dir)
    os.chdir(dir)

    ref_file = [f for f in cellulose_ref_files if dir in f]
    if ref_file:
        ref_file = ref_file[0]
        with open(ref_file) as ref:
            lines = ref.readlines()
        split_lines = [line.split(',') for line in lines]
        freqs = [float(line[0]) for line in split_lines if float(line[0]) > 200]
        intens = [float(line[1]) for line in split_lines if float(line[0]) > 200]
        min_intens = min(intens)
        intens = [i - min_intens for i in intens]
        max_intens = max(intens)
        ax.plot(freqs, [i/max_intens for i in intens], label='Exp. cellulose', color='b')
    
    ref_file = [f for f in cellobiose_ref_files if dir in f]
    print(ref_file)
    if len(ref_file):
        ref_file = ref_file[0]
        with open(ref_file) as ref:
            lines = ref.readlines()
        split_lines = [line.split(',') for line in lines]
        freqs = [float(line[0]) for line in split_lines if float(line[0]) > 200]
        intens = [float(line[1]) for line in split_lines if float(line[0]) > 200]
        min_intens = min(intens)
        intens = [i - min_intens for i in intens]
        max_intens = max(intens)
        ax.plot(freqs, [i/max_intens for i in intens], label='Exp. cellobiose', color='r')

    spectra = []
    for f in glob(log_glob1) + glob(log_glob2):
        with open(f) as file:
            lines = file.readlines()
        if 'inished' in lines[-1]:
            spectra.append(gparse.Spectrum.from_log_file(f))
    try:
        max_x = max(freqs)
        avg_function = gparse.Spectrum.average_function(spectra)
        x_array = gparse.util.linspace(0, max_x, 10000)
        y_array = [avg_function(x) for x in x_array]
        max_y = max(y_array)

        ax.plot([x*x_scale for x in x_array], [y/max_y for y in y_array], label='Simulated', color='k')
    except Exception as e:
        print(e)
    finally:
        os.chdir(top_dir)
    plt.text(0.3, 0.7, dir, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.locator_params(axis='y', nbins=2)
    

plt.gcf().subplots_adjust(hspace=0.1)
plt.legend()
plt.axis(axis_range)
plt.xlabel('Frequency (cm$^{-1}$)', fontsize=20)
suplabel('y', 'Normalized Spectral Intensity (arb. units)')

plt.show()
