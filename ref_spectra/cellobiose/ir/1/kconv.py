import shutil
from glob import glob

for f in glob('*C.csv'):
    num = int(''.join(filter(str.isdigit, f)))
    kelvin = num + 273
    if (kelvin % 10) == 8:
        kelvin += 2
    newfile = '{}K.csv'.format(kelvin)
    shutil.copyfile(f, newfile)
        
