import numpy as np

# mutational probability
orf_target_size = np.loadtxt("nrLOFMut.txt") # dtype 'f64' # per ORF

orf_target_size_cums = np.cumsum(orf_target_size)

data3 = np.loadtxt("ORF_Length") # dtype 'f64' % isn't needed?

# ORF names
orfs = np.loadtxt("LOF_ORFs.dat",dtype = 'S9')

# effects sizes
gen_time = np.loadtxt("mmGT.dat") # change in GT for each LOF mutation for each environment.
