import os
from glob import glob

with open('dft.job') as template_file:
    template_lines = template_file.readlines()

top_level = os.path.abspath('.')
for file in glob('**/**/**/2dp/*.com'):
    folder = '/'.join(os.path.abspath(file).split('/')[:-1])
    os.chdir(folder)
    com_file = glob('*.com')[0]
    print(com_file)
    with open('dft.job', 'w') as new_file:
        for line in template_lines:
            if 'YOUR-COMMAND' in line:
                line = 'g09run ' + com_file + '\n'
            new_file.write(line)
    os.chdir(top_level)
