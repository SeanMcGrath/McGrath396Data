#!/usr/bin/python

import os
from glob import glob

def is_numeric(string):
    try:
        float(string)
        return True
    except:
        return False

dirs = [os.path.abspath(dir) for dir in os.listdir('.') if is_numeric(dir)]

for dir in dirs:
    os.chdir(dir)
    for timedir in os.listdir():
        os.chdir(timedir)
        pdbs = [f.split('.')[0] for f in glob('*.pdb')]
        command_template = 'babel -i pdb {}.pdb -o com {}.com'
        for pdb in pdbs:
            os.system(command_template.format(pdb, pdb))
        os.chdir('..')

