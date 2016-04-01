import shutil
from glob import glob

for f in glob('*.csv'):
    num = int(f[6:][:-4].replace('C', ''))
    kelvin = num + 273
    if (kelvin % 10) == 8:
        kelvin += 2
    newfile = '{}K.csv'.format(kelvin)
    shutil.copyfile(f, newfile)
        
