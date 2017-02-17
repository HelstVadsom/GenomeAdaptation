import numpy as np

# mutational probability
data1 = np.loadtxt("nrLOFMut.txt") # dtype 'f64'

data1_Cum = np.cumsum(data1)

data2 = np.loadtxt("LOF_ORFs.dat",dtype = 'S9')

data3 = np.loadtxt("ORF_Length") # dtype 'f64'

# effects sizes

data4 = np.loadtxt("mmGT.dat")
