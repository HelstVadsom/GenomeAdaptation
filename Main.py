import numpy as np
from numpy import *

execfile("LoadData.py")

# \todo: HERE, Decide which mutations to look at.

execfile("InitilizeParameters.py")

execfile("CreateIndividuals.py")

# \todo: HERE, Delete variables we don't need anymore.
#data1 = data2 = None # delete unneccesary variables.

for iEnv in xrange(NR_ENVIRONMENTS):
    # \todo: set mutations and effects
    for iCycle in xrange(NR_CYCLES):
        print 'iEnv = ', iEnv, 'iCycle = ', iCycle
        t = 0
        stillInCycle = 1#1
        while stillInCycle:
            print 'time is ', t
            # \todo: Make time tic
            # \todo: check exit lag, (and if no cells in lag, turn off check)
            if sum(simEnv['lag_time'] > t) != 0:
                alive_n_lag = (simEnv['lag_time'] <= t).dot(simEnv['age'] >= 1)
                simEnv['lag_progress'][alive_n_lag] = 1
            # \todo: check time to divide
            # \todo: adjust time step
            # \todo: do mutate, in both or just ONE? calculate new ccycle time etc...
            # \todo: divide: set age, founder id
            # \todo: add born individuals to existing ones
            # \todo: check cycle exit condition. stillInCycle = 0
        # \todo: Sample for next cycle
        # \todo: save importants
    # \todo: save importants
# \todo: generate plots,
# \todo: make the code faster.

