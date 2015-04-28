# Analyze.py

fn = "Benzene_raman_vib.spm"
data = []
with open(fn)as f:
	for line in f.readlines()[30:60]:
		row = line.split()[1:3]
		floatrow = []
		for r in row: floatrow.append(float(r))
		if floatrow[-1] > 1: data.append(floatrow)

outfile = "results.csv"
with open(outfile, 'w') as f:
	f.write("Frequency (cm^-1),Intensity\n")
	for d in data: f.write("{},{}\n".format(d[0],d[1]))
