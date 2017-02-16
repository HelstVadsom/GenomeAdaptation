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
        stillInCycle = 1 # 1
        while stillInCycle:
            print 'time is ', t
            t += MINIMUM_TIME_RESOLUTION # Possible speed up? find biggest time increment...
            # Check exit lag, (and if no cells in lag, turn off check)
            if any(simEnv['lag_time'][0:nr_alive] > t):
                alive_n_lag = (simEnv['lag_time'][0:nr_alive] <= t).dot(simEnv['age'][0:nr_alive] >= 1)
                simEnv['lag_progress'][alive_n_lag] = 1

            ## Divide
            toDivide = (simEnv['cell_cycle_time'][0:nr_alive] <= t) #.dot(simEnv['age'][0:nr_alive] >= 1)
            #print simEnv[18,19]
            toBirth = np.arange(nr_alive,(nr_alive + len(toDivide)))
            #simEnv[toBirth] = simEnv[toDivide] # transcribe properties

            ## Mutate
            toMutate = np.random.random([len(toDivide),1]) < PROB_MUTATION
            if any(toMutate):
                idxMutate = nonzero(toMutate) # Which individuals dividing that mutate.
                mutateORF = np.random.random([sum(toMutate),1]) * (data1_Cum[-1]) # pick mutations
                idxORF = np.searchsorted(data1_Cum, mutateORF, side='right') # see which mutation it was
                # \todo: check if that mutation has already happend.
                # calculate mutation impact on cell cycle time
                simEnv['cell_cycle_time'][idxMutate[0]] = simEnv['cell_cycle_time'][idxMutate[0]] + \
                                                          data4[idxORF,iEnv].T*(CELL_CYCLE_TIMES[simEnv['founder_id'][idxMutate[0]]])
            nr_alive += 1
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
