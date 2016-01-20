import os
import shutil
from glob import glob

top_level = os.path.abspath('.')
for folder in os.listdir('.'):
    if os.path.isdir(folder):
        os.chdir(folder)
        for file in glob('*unit*'):
            time = file.split('.')[0]
            os.mkdir(time)
            shutil.move(file, time)
        
        os.chdir(top_level)
