import numpy as np

# mutational probability
orf_target_size = (np.loadtxt("targetSizeDel.dat") + \
                  np.loadtxt("targetSizeStp.dat"))/3

orf_target_size_cums = np.cumsum(orf_target_size)

# ORF names
orfs = np.loadtxt("uniqueORF2.txt",dtype = 'S9')

# effects sizes
gen_time = np.loadtxt("GT_Env.dat") # change in GT for each LOF mutation for each environment.
