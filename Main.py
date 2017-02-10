import numpy as np
from numpy import *

execfile("LoadData.py")

# \todo: HERE, Decide which mutations to look at.

execfile("InitilizeParameters.py")

execfile("CreateIndividuals.py")

# \todo: HERE, Delete variables we don't need anymore.
#data1 = data2 = None # delete unneccesary variables.

for iEnv in xrange(NR_ENVIRONMENTS):
    for iCycle in xrange(NR_CYCLES):
        print 'iEnv = ', iEnv, 'iCycle = ', iCycle
        stillInCycle = 1
        while stillInCycle:
            # \todo: Make time tic
            # \todo: check exit lag, (and if no cells in lag, turn off check)
            # \todo: check time to divide
            # \todo: adjust time step
            # \todo: do mutate, in both or just ONE? calculate new ccycle time etc...
            # \todo: divide: set age, founder id
            # \todo: add born individuals to existing ones
            # \todo: check cycle exit condition. stillInCycle = 0
        # \todo: save importants
    # \todo: save importants
# \todo: generate plots,
# \todo: make the code
