# Analyze.py

fn = "furfural_raman_1_vib.spm"
data = []
with open(fn)as f:
	for line in f.readlines()[30:57]:
		row = line.split()[1:3]
		floatrow = [float(r) for r in row]
		if floatrow[-1] > 1: data.append(floatrow)

outfile = "results.csv"
with open(outfile, 'w') as f:
	f.write("Frequency (cm^-1),Intensity\n")
	for d in data: f.write("{},{}\n".format(round(d[0]),round(d[1])))
