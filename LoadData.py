#from numpy import *

# mutational probability
data1 = loadtxt("nrLOFMut.txt") # dtype 'f64'

data1_Cum = np.cumsum(data1)

data2 = loadtxt("LOF_ORFs.dat",dtype = 'S9')

data3 = loadtxt("ORF_Length") # dtype 'f64'

# effects sizes
