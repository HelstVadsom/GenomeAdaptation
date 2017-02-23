import numpy as np
# from numpy import *
# execfile("LoadData.py")
# execfile("InitilizeParameters.py")
# execfile("CreateIndividuals.py")

from LoadData import *
from InitilizeParameters import *
from CreateIndividuals import sim_env

# \todo: HERE, Delete variables we don't need anymore.
# data1 = data2 = None # delete unneccesary variables.

lag_time = \
lag_escape = \
cell_cycle_time = \
founder_id = \
age = \
nr_divitions = \
divition_time = \
mutation = None

def run():
    t = 0
    nr_alive = FOUNDER_COUNT
    for i_cycle in xrange(NR_CYCLES):
        print 'i_env = ', i_env, 'i_cycle = ', i_cycle
        lag = 1
        still_in_cycle = 1 # 1
        while still_in_cycle:

            t += MINIMUM_TIME_RESOLUTION # Possible speed up? find biggest time increment...

            # Check lag
            if lag:
                lagging = (sim_env['lag_time'][:nr_alive] > 0)
                lag = any(lagging)
                sim_env['lag_time'][lagging] -= MINIMUM_TIME_RESOLUTION
                sim_env['next_divition'][lagging] += MINIMUM_TIME_RESOLUTION

            ## Divide
            to_divide = (sim_env['next_divition'][:nr_alive] <= t)
            nr_divide = np.sum(to_divide)
            if nr_divide:
                divide_index = np.nonzero(to_divide)[0]
                to_birth = np.arange(nr_alive,(nr_alive + nr_divide))
                sim_env['founder_id'][to_birth] = divide_index
                sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
                sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
                sim_env['next_divition'][to_divide] = t + sim_env['cell_cycle_time'][to_divide]
                sim_env['next_divition'][to_birth] = sim_env['next_divition'][to_divide]
                sim_env['nr_divitions'][to_divide] += 1

                ## Mutate
                to_mutate = np.random.random(nr_divide) < PROB_MUTATION
                if any(to_mutate):
                    mutate_orf = np.random.random([sum(to_mutate), 1]) * (data1_Cum[-1]) # pick mutation
                    orf_index = np.searchsorted(data1_Cum, mutate_orf, side='right') # peek mutation
                    # mutation[to_birth[to_mutate]] = orf_index  # store mutation
                    # divide_index = np.nonzero(to_divide)[0]
                    print 'time is ', t
                    print 'alive: ', nr_alive
                    print gen_time[orf_index, i_env]
                    sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
                        sim_env['cell_cycle_time'][divide_index[to_mutate]] + gen_time[orf_index, i_env] * MEAN_CELL_CYCLE_TIME
                    sim_env['next_divition'][to_birth[to_mutate]] = t + sim_env['cell_cycle_time'][to_birth[to_mutate]]

            ## Population ages
            sim_env['age'][:nr_alive] += 0.1 # worry, might take up alotta time.
            nr_alive += nr_divide
            # print 'alive: ', nr_alive

            # Check cycle exit condition

            if nr_alive >= MAXIMUM_NR_AGENTS - 10:
                still_in_cycle = 0
                print 'Exiting cycle: ', i_cycle

            # Save data for Growth curve
            if t % 20 == 0:
                growth[t/20, i_cycle] = nr_alive

            # \todo: Save data for Evolutionary tree, Look plot code online. Binary tree!
                # mutations and mothers for all mutated cells
                # nr unmutated cells,
                # time of mutation

        # Save data for histograms of GT
        gt_cycle[:MAXIMUM_NR_AGENTS, i_cycle] = (sim_env['cell_cycle_time'] - MEAN_CELL_CYCLE_TIME) / MEAN_CELL_CYCLE_TIME

        # Save meanGT
        meanGT[i_cycle] = np.mean(sim_env['cell_cycle_time'][:MAXIMUM_NR_AGENTS])

        # Sample for next cycle
        sample = np.random.choice(MAXIMUM_NR_AGENTS, SAMPLE_COUNT,replace=False)
        sim_env[:SAMPLE_COUNT] = sim_env[sample]
        nr_alive = SAMPLE_COUNT

        # \todo: save importants
    # \todo: save importants

    # \todo: generate plots,
    # \todo: make the code faster.




if __name__ == "__main__":
    i_env = 0
    run()
