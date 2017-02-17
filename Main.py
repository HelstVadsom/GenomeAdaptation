import numpy as np
#from numpy import *
#execfile("LoadData.py")
#execfile("InitilizeParameters.py")
#execfile("CreateIndividuals.py")

from LoadData import *
# \todo: HERE, Decide which mutations to look at.
from InitilizeParameters import *
from CreateIndividuals import simEnv

# \todo: HERE, Delete variables we don't need anymore.
#data1 = data2 = None # delete unneccesary variables.

def run():
    nr_alive = FOUNDER_COUNT
    nr_mutated = 0
    for iEnv in xrange(NR_ENVIRONMENTS):
        # \todo: set mutations and effects
        for iCycle in xrange(NR_CYCLES):
            print 'iEnv = ', iEnv, 'iCycle = ', iCycle
            t = 80
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
                nr_Divide = np.sum(toDivide)
                toBirth = np.arange(nr_alive,(nr_alive + nr_Divide))
                simEnv['founder_id'][toBirth] = simEnv['founder_id'][toDivide]
                simEnv['lag_time'][toBirth] = LAG_TIMES[simEnv['founder_id'][toDivide]]
                cct = CELL_CYCLE_TIMES[simEnv['founder_id'][toDivide]]
                simEnv['cell_cycle_time'][toDivide] = simEnv['cell_cycle_time'][toDivide] + cct
                simEnv['cell_cycle_time'][toBirth] = simEnv['cell_cycle_time'][toDivide]

                ## Mutate
                toMutate = np.random.random(nr_Divide) < PROB_MUTATION
                if any(toMutate):
                    mutateORF = np.random.random([sum(toMutate),1]) * (data1_Cum[-1]) # pick mutation
                    idxORF = np.searchsorted(data1_Cum, mutateORF, side='right') # peek mutation
                    # \todo: check if that mutation has already happend.
                    # update cell cycle time
                    divided = np.nonzero(toDivide)[0]
                    nr_mutated += len(divided)
                    simEnv['cell_cycle_time'][toBirth[toMutate]] = simEnv['cell_cycle_time'][divided[toMutate]] + \
                                                                   data4[idxORF,iEnv].T*(CELL_CYCLE_TIMES[simEnv['founder_id'][divided[toMutate]]]) # wrong: implement nextPoint to divide
                # Population ages
                simEnv['age'][0:nr_alive] += 0.1
                print 'alive: ', nr_alive
                #print 'nDivide', nr_Divide
                nr_alive += nr_Divide #Something is weird
                # \todo: check cycle exit condition. stillInCycle = 0

            # \todo: Sample for next cycle
            # \todo: save importants
        # \todo: save importants
    # \todo: generate plots,
    # \todo: make the code faster.


if __name__ == "__main__":

    run()
