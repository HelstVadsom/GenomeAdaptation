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


def run():
    nr_alive = FOUNDER_COUNT
    # nr_mutations = 0
    for i_env in xrange(NR_ENVIRONMENTS):
        for i_cycle in xrange(NR_CYCLES):
            print 'i_env = ', i_env, 'i_cycle = ', i_cycle
            t = 0
            lag = 1
            still_in_cycle = 1 # 1
            while still_in_cycle:
                # print 'time is ', t
                # print 'alive: ', nr_alive

                t += MINIMUM_TIME_RESOLUTION # Possible speed up? find biggest time increment...
                # Check exit lag, (and if no cells in lag, turn off check)
                if lag:
                    lagging = (sim_env['lag_time'][:nr_alive] > 0) #.dot(sim_env['age'][0:nr_alive] >= 1)
                    lag = any(lagging)
                    sim_env['lag_time'][lagging] -= MINIMUM_TIME_RESOLUTION
                    sim_env['next_divition'][lagging] += MINIMUM_TIME_RESOLUTION

                ## Divide
                to_divide = (sim_env['next_divition'][:nr_alive] <= t)#.dot(sim_env['lag_time'][0:nr_alive] >= t)
                nr_divide = np.sum(to_divide)
                if nr_divide:
                    # print nr_divide
                    # print np.nonzero(to_divide)[0]
                    divide_index = np.nonzero(to_divide)[0]
                    to_birth = np.arange(nr_alive,(nr_alive + nr_divide))
                    sim_env['founder_id'][to_birth] = divide_index
                    sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
                    sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
                    sim_env['next_divition'][to_divide] = t + sim_env['cell_cycle_time'][to_divide]
                    sim_env['next_divition'][to_birth] = sim_env['next_divition'][to_divide]
                    # CELL_CYCLE_TIMES[sim_env['founder_id'][to_divide]]
                    sim_env['nr_divitions'][to_divide] += 1

                    ## Mutate
                    to_mutate = np.random.random(nr_divide) < PROB_MUTATION
                    if any(to_mutate):
                        mutate_orf = np.random.random([sum(to_mutate), 1]) * (data1_Cum[-1]) # pick mutation
                        orf_index = np.searchsorted(data1_Cum, mutate_orf, side='right') # peek mutation
                        mutation[to_birth[to_mutate]] = orf_index  # store mutation
                        # divide_index = np.nonzero(to_divide)[0]
                        # nr_mutations +=
                        print 'time is ', t
                        print 'alive: ', nr_alive
                        print gen_time[orf_index, i_env]
                        sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
                            sim_env['cell_cycle_time'][divide_index[to_mutate]] + gen_time[orf_index, i_env] * MEAN_CELL_CYCLE_TIME
                        sim_env['next_divition'][to_birth[to_mutate]] = t + sim_env['cell_cycle_time'][to_birth[to_mutate]]

                ## Population ages
                sim_env['age'][0:nr_alive] += 0.1 # worry, might take up alotta time.
                nr_alive += nr_divide
                # print 'alive: ', nr_alive

                # Check cycle exit condition

                if nr_alive >= MAXIMUM_NR_AGENTS - 10:
                    still_in_cycle = 0

                # \todo: Save data for Growth curve
                    # if i_cycle == 0 or 24 or 49:
                    # nr_alive at increments of 20 min. -> 30 points

                # \todo: Save data for Evolutionary tree, Look plot code online. Binary tree!
                    # mutations and mothers for all mutated cells
                    # nr unmutated cells,
                    # time of mutation

                # \todo: Save data for histograms of GT
                    # if i_cycle .. first middle last
                    # save hist GT

                # \todo: Save meanGT at end of cycles.

            # Sample for next cycle
            sample = np.random.random(SAMPLE_COUNT)*MAXIMUM_NR_AGENTS
            sim_env[0:SAMPLE_COUNT] = sim_env[sample]
            nr_alive = SAMPLE_COUNT
            sim_env['next_divition'][0:nr_alive] = sim_env['cell_cycle_time'][0:nr_alive]
            lag = 1
            t = 0
            # \todo: save importants
        # \todo: save importants
    # \todo: generate plots,
    # \todo: make the code faster.


if __name__ == "__main__":

    run()
