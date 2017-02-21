import numpy as np
#from numpy import *
#execfile("LoadData.py")
#execfile("InitilizeParameters.py")
#execfile("CreateIndividuals.py")

from LoadData import *
from InitilizeParameters import *
from CreateIndividuals import simEnv

# \todo: HERE, Delete variables we don't need anymore.
#data1 = data2 = None # delete unneccesary variables.

def run():
    nr_alive = FOUNDER_COUNT
    nr_mutations = 0
    for iEnv in xrange(NR_ENVIRONMENTS):
        for iCycle in xrange(NR_CYCLES):
            print 'iEnv = ', iEnv, 'iCycle = ', iCycle
            t = 0
            lag = 1
            stillInCycle = 1 # 1
            while stillInCycle:
                #print 'time is ', t
                #print 'alive: ', nr_alive

                t += MINIMUM_TIME_RESOLUTION # Possible speed up? find biggest time increment...
                # Check exit lag, (and if no cells in lag, turn off check)
                if lag: # \todo: Fix Lagging mechanics
                    lagging = (simEnv['lag_time'][0:nr_alive] > 0) #.dot(simEnv['age'][0:nr_alive] >= 1)
                    lag = any(lagging)
                    simEnv['lag_time'][lagging] -= MINIMUM_TIME_RESOLUTION
                    simEnv['next_divition'][lagging] += MINIMUM_TIME_RESOLUTION
                    print lagging

                ## Divide
                toDivide = (simEnv['next_divition'][0:nr_alive] <= t)#.dot(simEnv['lag_time'][0:nr_alive] >= t)
                nr_Divide = np.sum(toDivide)
                if nr_Divide != 0:
                    #print nr_Divide
                    #print np.nonzero(toDivide)[0]
                    idxDivide = np.nonzero(toDivide)[0]
                    toBirth = np.arange(nr_alive,(nr_alive + nr_Divide))
                    simEnv['founder_id'][toBirth] = idxDivide
                    simEnv['lag_time'][toBirth] = simEnv['lag_time'][toDivide]
                    simEnv['cell_cycle_time'][toBirth] = simEnv['cell_cycle_time'][toDivide]
                    simEnv['next_divition'][toDivide] = t + simEnv['cell_cycle_time'][toDivide]
                    simEnv['next_divition'][toBirth] = simEnv['next_divition'][toDivide]
                    #CELL_CYCLE_TIMES[simEnv['founder_id'][toDivide]]
                    simEnv['nr_divitions'][toDivide] += 1

                    ## Mutate
                    toMutate = np.random.random(nr_Divide) < PROB_MUTATION
                    if any(toMutate):
                        mutateORF = np.random.random([sum(toMutate),1]) * (data1_Cum[-1]) # pick mutation
                        idxORF = np.searchsorted(data1_Cum, mutateORF, side='right') # peek mutation
                        mutation[toBirth[toMutate]] = idxORF  # store mutation
                        #idxDivide = np.nonzero(toDivide)[0]
                        #nr_mutations +=
                        print 'time is ', t
                        print 'alive: ', nr_alive
                        print data4[idxORF,iEnv]

                        simEnv['cell_cycle_time'][toBirth[toMutate]] = simEnv['cell_cycle_time'][idxDivide[toMutate]] + \
                                                                       data4[idxORF,iEnv]*MEAN_CELL_CYCLE_TIME #(CELL_CYCLE_TIMES[simEnv['founder_id'][idxDivide[toMutate]]])
                        simEnv['next_divition'][toBirth[toMutate]] = t + simEnv['cell_cycle_time'][toBirth[toMutate]]

                ## Population ages
                simEnv['age'][0:nr_alive] += 0.1 # worry, might take up alotta time.
                nr_alive += nr_Divide
                #print 'alive: ', nr_alive

                # Check cycle exit condition
                if nr_alive >= MAXIMUM_NR_AGENTS:
                    stillInCycle = 0



            # \todo: Sample for next cycle
            # \todo: save importants
        # \todo: save importants
    # \todo: generate plots,
    # \todo: make the code faster.


if __name__ == "__main__":

    run()
