import numpy as np

# mutational probability
nr_LOFM = np.loadtxt("nrLOFMut.txt") # dtype 'f64' # per ORF

nr_LOFM_cumsum = np.cumsum(nr_LOFM)

#data3 = np.loadtxt("ORF_Length") # dtype 'f64' % isn't needed?

# ORF names
orfs = np.loadtxt("LOF_ORFs.dat",dtype = 'S9')

# effects sizes
gen_time = np.loadtxt("mmGT.dat") # change in GT for each LOF mutation for each environment.
