import gparse
import sys
import os
import itertools
from glob import glob

X_SCALE = 1.017

def avg(iterable):
    return sum(iterable)/len(iterable)

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

def tablepad(items, header=False):
    padded = []
    try:
        if header:
            padded.append(str(items[0]).rjust(21))
            padded.append(format(items[1]).rjust(23))
            padded.append(format(items[2]).rjust(23))
        else:
            padded.append(format(items[0], '.4f').rjust(11))
            padded.append(format(items[1], '.4f').rjust(23))
            padded.append(format(items[2], '.4f').rjust(23))
    except:
        pass
    return padded

def atompad(atoms):
    num = str(atoms[0].number).rjust(6)
    element = str(atoms[0].element).rjust(4)
    padded = num + element
    for atom in atoms:
        padded += format(atom.eigen_x, '.2f').rjust(9)
        padded += format(atom.eigen_y, '.2f').rjust(7)
        padded += format(atom.eigen_z, '.2f').rjust(7)
    return padded

top_dir = os.getcwd()
temp_dirs = [dir for dir in os.listdir() if dir.endswith('K') and dir is not '450K']

for dir in sorted(temp_dirs):
    os.chdir(dir)
    logs = glob('**/**/**/*.log')
    assignments = [gparse.PeakAssigner(log).peaks for log in logs]
    peaks = list([item for sublist in assignments for item in sublist])
    peak_nums = set([p.number for p in peaks])
    avg_peaks = []
    for peak_number in peak_nums:
        peaks_with_num = [p for p in peaks if p.number == peak_number]
        avg_frequency = round(avg([p.frequency for p  in peaks_with_num]), 4)
        avg_redmass =  round(avg([p.reduced_mass for p in peaks_with_num]), 4)
        avg_frc_const =  round(avg([p.frc_const for p in peaks_with_num]), 4)
        avg_ir =  round(avg([p.ir_intensity for p in peaks_with_num]), 4)
        avg_raman =  round(avg([p.raman_activity for p in peaks_with_num]), 4)
        avg_depolar_p =  round(avg([p.depolar_p for p in peaks_with_num]), 4)
        avg_depolar_u =  round(avg([p.depolar_u for p in peaks_with_num]), 4)

        all_atoms = []
        for peak in peaks_with_num:
            all_atoms += peak.atoms
        avg_atoms = []
        for num in sorted(list(set([a.number for a in all_atoms]))):
            atoms_with_num = [a for a in all_atoms if a.number == num]
            avg_x = avg([a.eigen_x for a in atoms_with_num])
            avg_y = avg([a.eigen_y for a in atoms_with_num])
            avg_z = avg([a.eigen_z for a in atoms_with_num])
            avg_atoms.append(gparse.spectrum.Atom(
                num, atoms_with_num[0].element, eigen_x=avg_x, eigen_y=avg_y, eigen_z=avg_z))
        
        avg_peak = gparse.spectrum.SpectralPeak(
            peak_number,
            avg_frequency,
            avg_redmass,
            avg_frc_const,
            avg_ir,
            avg_raman,
            avg_depolar_p,
            avg_depolar_u)

        avg_peak.set_atoms(avg_atoms)
        avg_peaks.append(avg_peak)

    with open(os.path.join('../avg_logs', dir +'.log'), 'w') as outfile:
        for group in grouper(3, peak_nums):
            print(' {}{}{}'
                .format(*tablepad(group, True)), file=outfile)
            # print(' {}{}{}'.format(*tablepad(['A','A','A'], True)))
            print('                     A                      A                      A', file=outfile)
            print(' Frequencies --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].frequency for i in group])), file=outfile)
            print(' Red. Masses --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].reduced_mass for i in group])), file=outfile)
            print(' Frc consts  --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].frc_const for i in group])), file=outfile)
            print(' IR Inten    --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].ir_intensity for i in group])), file=outfile)
            print(' Raman activ --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].raman_activity for i in group])), file=outfile)
            print(' Depolar (P) --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].depolar_p for i in group])), file=outfile)
            print(' Depolar (U) --{}{}{}'
                .format(*tablepad([avg_peaks[i-1].depolar_u for i in group])), file=outfile)
            print('  Atom  AN      X      Y      Z        X      Y      Z        X      Y      Z', file=outfile)

            num_atoms = len(avg_peaks[0].atoms)
            for i in range(num_atoms):
                print(atompad([avg_peaks[j-1].atoms[i] for j in group]), file=outfile)

    os.chdir(top_dir)
