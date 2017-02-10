import numpy as np
from numpy import *

execfile("LoadData.py")

# \todo: HERE, Decide which mutations to look at.

execfile("InitilizeParameters.py")

execfile("CreateIndividuals.py")

# \todo: HERE, Delete variables we don't need anymore.
#data1 = data2 = None # delete unneccesary variables.

for iEnv in xrange(NR_ENVIRONMENTS):
    if __name__ == '__main__':
        for iCycle in xrange(NR_CYCLES):
            print 'iEnv = ', iEnv,'iCycle = ',iCycle
            # \todo: Make time tic
            # \todo: check exit lag, (and if no cells in lag, turn off check)
            # \todo: check time to divide
            # \todo: do mutate, in both or just ONE? calculate new ccycle time etc...
            # \todo: divide: set age, founder id
            # \todo: add born individuals to existing ones
            # \todo: check cycle exit condition. break
    
