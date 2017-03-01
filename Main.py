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
    nr_divisions = \
    division_time = \
    mutation = None


def run():

    nr_alive = FOUNDER_COUNT
    growth = nr_alive
    growth_time = 0
    cycle_time = 0
    time_step = 20
    for i_cycle in xrange(NR_CYCLES):
        print 'i_env = ', i_env, 'i_cycle = ', i_cycle

        t = 0
        lag = 1
        lagging = np.ones(nr_alive)
        full = 0
        still_in_cycle = 1
        experiment_time = 72*60
        if __name__ == '__main__':
            while still_in_cycle:

                # Lag
                if lag:
                    prev_lagging = lagging
                    lagging = (sim_env['lag_time'][:nr_alive] > t)
                    lag = any(lagging)
                    sim_env['next_division'][lagging] += time_step # Postpone next division
                    lag_escapists = np.bool_(prev_lagging * (1 - lagging))
                    sim_env['next_division'][lag_escapists] -= t - sim_env['lag_time'][lag_escapists]

                # Save data for growth curve.
                growth = np.append(growth, nr_alive)
                growth_time = np.append(growth_time, t)
                
                if t >= experiment_time: # exit experiment
                    full = 1
                    
                t += time_step

                if not full:
                    ## Divide
                    to_divide = (sim_env['next_division'][:nr_alive] <= t)
                    nr_divide = np.sum(to_divide)
                    if nr_divide:
                        divide_index = np.nonzero(to_divide)[0]
                        to_birth = np.arange(nr_alive,(nr_alive + nr_divide))

                        if nr_alive + len(to_birth) >= MAXIMUM_NR_AGENTS: # If this is the last iteration before a new cycle. \todo: Do we even need this later
                            nr_divide_reduced = MAXIMUM_NR_AGENTS - nr_alive
                            to_birth = np.arange(nr_alive, (nr_alive + nr_divide_reduced))
                            divide_index = divide_index[np.random.choice(nr_divide, nr_divide_reduced, replace=False)]
                            to_divide = divide_index
                            nr_divide = nr_divide_reduced
                            full = 1
                            print 'About to exit cycle'

                        sim_env['founder_id'][to_birth] = divide_index
                        sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
                        sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
                        sim_env['next_division'][to_divide] += sim_env['cell_cycle_time'][to_divide]
                        sim_env['next_division'][to_birth] = sim_env['next_division'][to_divide]
                        sim_env['nr_divisions'][to_divide] += 1

                        ## Mutate
                        to_mutate = np.random.random(nr_divide) < PROB_MUTATION
                        if any(to_mutate): # \todo: store mutations. Make sure they are copied at division.
                            mutate_orf = np.random.random([sum(to_mutate), 1]) * (data1_Cum[-1]) # pick mutation
                            orf_index = np.searchsorted(data1_Cum, mutate_orf, side='right') # peek mutation
                            # mutation[to_birth[to_mutate]] = orf_index  # store mutation
                            # divide_index = np.nonzero(to_divide)[0]

                            sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
                                sim_env['cell_cycle_time'][divide_index[to_mutate]] + \
                                gen_time[orf_index, i_env] * MEAN_CELL_CYCLE_TIME

                            sim_env['next_division'][to_birth[to_mutate]] += \
                                sim_env['cell_cycle_time'][to_birth[to_mutate]] - \
                                sim_env['cell_cycle_time'][divide_index[to_mutate]]


                ## Population ages
                sim_env['age'][:nr_alive] += time_step
                nr_alive += nr_divide

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

        sim_env['next_division'][:SAMPLE_COUNT] = sim_env['cell_cycle_time'][:SAMPLE_COUNT]

    # Do After All cycles
    # \todo: generate plots, in a seperate function.
    import matplotlib.pyplot as plt
    plt.figure(1, figsize=(2.75, 2.0)) # \todo: Make the growth curves plot on top of each other, maybe by implementing a local, cycle time. As We did from the start.

    plt.plot(growth_time, growth, '-')

    plt.savefig('plt_ex1.pdf')

    plt.figure(2, figsize=(2.75, 2.0))
    plt.plot(meanGT)
    plt.savefig('plt_ex2.pdf')

    plt.show()

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
