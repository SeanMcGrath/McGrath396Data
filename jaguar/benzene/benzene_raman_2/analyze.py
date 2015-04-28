import math, matplotlib.pyplot as pl

fn = 'benzene_raman_2.vib'
lines = [line.strip() for line in open(fn,'r')]

lines = lines[101:131]

cols = [line.split(' ') for line in lines]

x = [float(col[1]) for col in cols]
y = [float(col[4]) for col in cols]

pl.plot(x,y)
pl.suptitle('Simulated Raman Spectrum of Benzene')
pl.xlabel('Frequency (cm^-1)')
pl.ylabel('Raman Intensity')
pl.show()