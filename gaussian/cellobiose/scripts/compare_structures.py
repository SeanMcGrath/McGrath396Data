import gparse
import os
import numpy as np
from glob import glob

dp_glob = '**/1/2dp/*.log'
dpf_glob = '**/1/2dpf/*.log'
ref_dir = '/home/sean/Documents/thesis/gaussian/cellobiose/280K'

ref_structs = [gparse.Structure.from_log_file(log) for log in glob(ref_dir + '/' + dp_glob)]
avg_ref_struct = gparse.Structure.average(ref_structs)

temp_dirs = sorted([dir for dir in os.listdir() if len(dir) == 4 and dir.endswith('K') and dir != '450K'])
top_dir = os.getcwd()

for dir in temp_dirs:
    os.chdir(dir)
    logs = glob(dp_glob) + glob(dpf_glob)
    devs = []
    for log in logs:
        struct = gparse.Structure.from_log_file(log)
        devs.append(struct.avg_deviation(avg_ref_struct, 29))
    print(dir, np.mean(devs), np.std(devs), max(devs))
    os.chdir(top_dir)
 
