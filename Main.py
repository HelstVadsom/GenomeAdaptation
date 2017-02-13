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
            # Make time tic
            t += MINIMUM_TIME_RESOLUTION # Possible speed up? find biggest time increment...
            # Check exit lag, (and if no cells in lag, turn off check)
            if any(simEnv['lag_time'][0:nr_alive] > t):
                alive_n_lag = (simEnv['lag_time'][0:nr_alive] <= t).dot(simEnv['age'][0:nr_alive] >= 1)
                simEnv['lag_progress'][alive_n_lag] = 1
                #t += 1
            # \todo: check time to divide
            # Find dividing agents
            toDivide = simEnv['cell_cycle_time'][0:nr_alive] <= t) #.dot(simEnv['age'][0:nr_alive] >= 1)
            # Find mutations
            toMutate = np.random.random([len(toDivide,1)]) < PROB_MUTATION
            if any(toMutate):
                for iMutate in nonzero(toMutate)):
                    mutatedORF = floor(np.random.random() * (sum(data1) + 1))
                    


            # \todo: adjust time step
            # \todo: do mutate, in both or just ONE? calculate new ccycle time etc...
            # \todo: divide: set age, founder id
            # \todo: add born individuals to existing ones
            # Population ages
            nr_alive += 1 # expand to batch
            simEnv['age'][0:nr_alive] += 0.1
            # \todo: check cycle exit condition. stillInCycle = 0
        # \todo: Sample for next cycle
        # \todo: save importants
    # \todo: save importants
# \todo: generate plots,
# \todo: make the code faster.

