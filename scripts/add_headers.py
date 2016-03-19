import os
from glob import glob

header = '# freq=raman b3lyp/6-31+g(2d,p) geom=connectivity\n'

def is_numeric(string):
    try:
        float(string)
        return True
    except:
        return False

dirs = [os.path.abspath(dir) for dir in os.listdir('.') if is_numeric(dir)]

for dir in dirs:
    os.chdir(dir)
    files = [f for f in glob('**/*.com')]
    for f in files:
        lines = []
        with open(f) as open_file:
            lines = open_file.readlines()
        lines[0] = header
        lines[2] = dir.split('/')[-1] + ' ' + f + '\n'
        lines[4] = '0 1\n'
        with open(f, 'w') as open_file:
            for line in lines:
                open_file.write(line) 
