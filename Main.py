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
    growth = nr_alive
    growth_time = 0
    cycle_time = 0
    for i_cycle in xrange(NR_CYCLES):
        print 'i_env = ', i_env, 'i_cycle = ', i_cycle
        lag = 1
        still_in_cycle = 1 # 1
        if __name__ == '__main__':
            while still_in_cycle:

                # Check lag \todo: make into seperate functions. (LAG AND TIME_STEP)
                if lag: # \todo: Make lagging take place at every cycle. And introduce lag escape.
                    time_step = MINIMUM_TIME_RESOLUTION
                    lagging = (sim_env['lag_time'][:nr_alive] > 0)
                    lag = any(lagging)
                    sim_env['lag_time'][lagging] -= time_step
                    sim_env['next_divition'][lagging] += time_step
                else: # set another time_step
                    if time_step != MINIMUM_TIME_RESOLUTION or np.random.random() < A_MYSTICAL_SPEED_UP_PARAMETER:
                            soonest_division = np.min([sim_env['next_divition'][:nr_alive]])
                            time_step = np.max([MINIMUM_TIME_RESOLUTION, soonest_division - t]) # find biggest time increment

                if MEASUREMENTS_AT_EVERY:
                    do_measurements = np.floor((t + time_step) / MEASUREMENTS_AT_EVERY) - np.floor(t / MEASUREMENTS_AT_EVERY)
                    if do_measurements: # Saves data for Growth curve
                        growth = np.append(growth, np.tile(nr_alive,do_measurements))
                        # \todo:  growth_time = np.append(MEASUREMENTS_AT_EVERY)
                else:
                    growth = np.append(growth, nr_alive)
                    growth_time = np.append(growth_time, t)

                t += time_step

                ## Divide
                to_divide = (sim_env['next_divition'][:nr_alive] <= t)
                nr_divide = np.sum(to_divide)
                if nr_divide:
                    divide_index = np.nonzero(to_divide)[0]
                    to_birth = np.arange(nr_alive,(nr_alive + nr_divide))

                    if nr_alive + len(to_birth) >= MAXIMUM_NR_AGENTS: # If this is the last iteration before a new cycle.
                        nr_divide_reduced = MAXIMUM_NR_AGENTS - nr_alive
                        to_birth = np.arange(nr_alive, (nr_alive + nr_divide_reduced))
                        divide_index = divide_index[np.random.choice(nr_divide, nr_divide_reduced, replace=False)]
                        to_divide = divide_index
                        nr_divide = nr_divide_reduced
                        still_in_cycle = 0 # Exits while loop.
                        print 'About to exit cycle'

                    sim_env['founder_id'][to_birth] = divide_index
                    sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
                    sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
                    sim_env['next_divition'][to_divide] = t + sim_env['cell_cycle_time'][to_divide] # \todo: review division.
                    sim_env['next_divition'][to_birth] = sim_env['next_divition'][to_divide]
                    sim_env['nr_divitions'][to_divide] += 1

                    ## Mutate
                    to_mutate = np.random.random(nr_divide) < PROB_MUTATION
                    if any(to_mutate): # \todo: store mutations. Make sure they are copied at division.
                        mutate_orf = np.random.random([sum(to_mutate), 1]) * (data1_Cum[-1]) # pick mutation
                        orf_index = np.searchsorted(data1_Cum, mutate_orf, side='right') # peek mutation
                        # mutation[to_birth[to_mutate]] = orf_index  # store mutation
                        # divide_index = np.nonzero(to_divide)[0]
                        print 'time is ', t
                        print 'alive: ', nr_alive
                        print 'GT mutaion(s): ', gen_time[orf_index, i_env]
                        sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
                            sim_env['cell_cycle_time'][divide_index[to_mutate]] + gen_time[orf_index, i_env] * MEAN_CELL_CYCLE_TIME
                        sim_env['next_divition'][to_birth[to_mutate]] = t + sim_env['cell_cycle_time'][to_birth[to_mutate]]

                ## Population ages
                sim_env['age'][:nr_alive] += 0.1
                nr_alive += nr_divide

                # Check cycle exit condition
                #if nr_alive >= MAXIMUM_NR_AGENTS: # superfluos? Seems so! Most likely so! OF COURSE!
                #    still_in_cycle = 0
                #    print 'Exiting cycle: ', i_cycle

                # \todo: Save data for Evolutionary tree, Look plot code online. Binary tree!
                    # mutations and mothers for all mutated cells
                    # nr unmutated cells,
                    # time of mutation
                # \todo: Save data to create histogram of mutations
                # \todo: Save data to determine nr of haplotypes.

        # Save data for histograms of GT
        gt_cycle[:MAXIMUM_NR_AGENTS, i_cycle] = (sim_env['cell_cycle_time'] - MEAN_CELL_CYCLE_TIME) / MEAN_CELL_CYCLE_TIME

        # Save meanGT
        meanGT[i_cycle] = np.mean(gt_cycle[:,i_cycle]) #np.mean(sim_env['cell_cycle_time'][:MAXIMUM_NR_AGENTS])

        cycle_time = np.append(cycle_time, t) # stores cycle exit time

        # Sample for next cycle
        sample = np.random.choice(MAXIMUM_NR_AGENTS, SAMPLE_COUNT,replace=False)
        sim_env[:SAMPLE_COUNT] = sim_env[sample]
        nr_alive = SAMPLE_COUNT


    # \todo: generate plots, in a seperate function.
    import matplotlib.pyplot as plt
    plt.figure(1, figsize=(2.75, 2.0)) # \todo: Make the growth curves plot on top of each other, maybe by implementing a local, cycle time. As We did from the start.

    if MEASUREMENTS_AT_EVERY:
        plt.plot(np.linspace(0, len(growth)*MEASUREMENTS_AT_EVERY, len(growth)), growth, '-')
    else:
        plt.plot(growth_time, growth, '-')

    plt.savefig('plt_ex1.pdf')

    plt.figure(2, figsize=(2.75, 2.0))
    plt.plot(meanGT)
    plt.savefig('plt_ex2.pdf')

    plt.show()

 # \todo: reset time, for simplicity. (How it used to be)

    #if cycle_time > i * MEASUREMENTS_AT_EVERY

#def plot():


if __name__ == "__main__": # \todo Create functions
    i_env = 0

    # 'Arsenite'   (i_env = 0)
    # 'Citric_Acid'(i_env = 1)
    # 'Citrulline' (i_env = 2)
    # 'Glycine'    (i_env = 3)
    # 'Isoleucine' (i_env = 4)
    # 'Paraquat'   (i_env = 5)
    # 'Rapamycin'  (i_env = 6)
    # 'SC'         (i_env = 7)
    # 'Tryptophan' (i_env = 8)

    #[growth, meanGT] = run()
    run()
    #plot()
    # \todo: Clean up the code! it's messy!

    # \todo: save the last time point as well.
# But Wait we already know the times at which the number is set.
