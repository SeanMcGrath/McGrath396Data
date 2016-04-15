import gparse
import os
import sys
import numpy as np
from glob import glob

cutoff = float(sys.argv[1])

def average_matrix(matrices):
    avg_matrix = []
    for i in range(len(matrices[0])):
        avg = np.mean([m[i] for m in matrices], axis=0)
        avg_matrix.append(avg)
    return gparse.DistanceMatrix(avg_matrix)

ref_matrix = average_matrix([gparse.DistanceMatrix.from_log_file(m) for m in glob('10K/*.log')])

temp_dirs = sorted([dir for dir in os.listdir() if len(dir) == 4 and dir.endswith('K') and dir != '450K'])
top_dir = os.getcwd()
dp_glob = '**/1/2dp/*.log'
dpf_glob = '**/1/2dpf/*.log'

for dir in temp_dirs:
    os.chdir(dir)
    logs = glob(dp_glob) + glob(dpf_glob)
    matrices = [gparse.DistanceMatrix.from_log_file(log) for log in logs]
    avg = average_matrix(matrices)
    print(dir, ref_matrix.rms_deviation(avg, cutoff))
    os.chdir(top_dir)
