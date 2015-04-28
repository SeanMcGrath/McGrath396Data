# McGrath396Data

Sean McGrath's data and resources for a variety of quantum chemistry simulations performed with Dr. Scott Auerbach.

The files are organized in the following way:

`jaguar` contains data associated with simulations performed with Schrodinger's Jaguar simulation package. Use of this package is not recommended for future work due to Jaguar's poor support for higher-order basis sets and general instability.

`gaussian` contains input and output files for a number of simulations conducted in Gaussian, as well as files generated from analysis of the output.

`scripts` contains several bash tools for parsing Gaussian log files and generating plots from them. These functions are to be integrated into a cohesive command-line tool in the near future.

### File Types

`.mae`: A Project for the Maestro simulation manager. Not recommended for use.

`.vib`: IR vibrational analysis output of Jaguar.

`.spm`: Raman vibrational analysis ouput of Jaguar.

`.in`: Input file for Jaguar simulations.

`.out`: Output file for Jaguar simulations.

`.job`: A computational job to be submitted to Volta or another queue-managed system via the `qsub` command.

`.com`: A gaussian input file.

`.log`: For Jaguar, a relatively useless log of simulation detailes. For Gaussian, the main output file, which is fed into various parsing scripts to extract vibrational data and distance matrices.

`.csv`: The output of an analysis script; if it has "distance" in the title, it is probably an atomic distance matrix; otherwise, it is probably raman spectral data.

`.gnumeric`/`.xls`: a spreadsheet, probably used to calculate the RMS deviation of simulated Raman frequencies from experimental values.

### Submitting Jobs to Gaussian

Gaussian simulation jobs are represented by `.com` files, and can be submitted directly to Gaussian via the `gaussian` command or equivalent wherever the software is installed.

However, Gaussian jobs are best executed on the Volta supercomputer, and this is slightly more complicated. A `.job` file must be created for submission to the Volta' batch server; this can be done be copying `gaussian/dft.job` and replacing the `.com` file it references with the one you would like to submit. Ensure that both of these files are copied to volta and placed in a proper working directory (`scp` is useful for this) then simply execute `qsub <your_file>.com`.

If everything goes smoothly, Gaussian will generate a `.log` file in the working directory and no `.e` file, which documents errors.

### Recommended Settings.

Gaussian simulations should be carried out at the B3LYP level of density-functional theory, using a 6-31+G(2DF,P)
basis set. If a dissolved system is being simulated, the SMD solvation model seems to work nicely. Jaguar does NOT support this basis set for Raman analysis.

### Using Scripts

Until a comprehensive tool is implemented, the included scripts are the best way to extract information from Gaussian output.

`matrixparse` takes a single Gaussian `.log` file as its argument and outputs a comma-separated table representing the final atomic distance matrix of the simulated molecule. Table entries at position `(i,j)` represent the distance in angstroms between atom `i` and atom `j`. Consult the logfile itself for the atomic number scheme.

`matrixRMS` takes two matrices created by `matrixparse` and calculates the RMS deviation between them as a way of quantifying the degree to which two molecular structures differ.

`ramanparse` takes in a single Gaussian `.log` file which contains Raman data and outputs a comma-separated list of frequency-intensity pairs, with column headers.

`lorPlot` takes in the outout of `ramanparse` and constructs a Lorentzian fit to the frequency data. It outputs a plot of this fit as well. To run this, you will need the Python packages `matplotlib`, `seaborn` and their associated dependencies.
