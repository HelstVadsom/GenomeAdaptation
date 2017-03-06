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
    division_time = None


def run():

    nr_alive = FOUNDER_COUNT
    growth = nr_alive
    growth_time = 0
    cycle_time = 0
    time_step = 20
    mutation = - np.ones([MAXIMUM_NR_AGENTS, 10], dtype='int16')  # dtype =
    for i_cycle in xrange(NR_CYCLES):
        print 'i_env = ', i_env, 'i_cycle = ', i_cycle

        t = 0
        lag = 1
        lagging = np.ones(nr_alive)
        full = 0
        still_in_cycle = 1
        experiment_time = 72*60
        while still_in_cycle:

            # Lag
            if lag:
                prev_lagging = lagging

                if i_cycle == 1:
                    lagging = (sim_env['lag_time'][:FOUNDER_COUNT] > t)
                else:
                    lagging = (sim_env['lag_time'][:SAMPLE_COUNT] > t)

                lag = any(lagging)
                sim_env['next_division'][lagging] += time_step # Postpone next division
                lag_escapists = np.bool_(prev_lagging * (1 - lagging))
                sim_env['next_division'][lag_escapists] -= t - sim_env['lag_time'][lag_escapists]

            # Save data for growth curve.
            growth = np.append(growth, nr_alive)
            growth_time = np.append(growth_time, t)

            #if t >= experiment_time: # exit experiment
            #    full = 1

            t += time_step

            #if not full:
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
                    #full = 1
                    sim_env['age'][:MAXIMUM_NR_AGENTS] += experiment_time
                    still_in_cycle = 0
                    print 'About to exit cycle'

                sim_env['founder_id'][to_birth] = divide_index
                sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
                sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
                sim_env['next_division'][to_divide] += sim_env['cell_cycle_time'][to_divide]
                sim_env['next_division'][to_birth] = sim_env['next_division'][to_divide]
                sim_env['nr_divisions'][to_divide] += 1
                mutation[to_birth] = mutation[to_divide]
                #print mutation[to_divide]
                #print mutation[to_birth]
                ## Mutate
                to_mutate = np.random.random(nr_divide) < PROB_MUTATION
                if any(to_mutate):
                    mutate_orf = np.random.random([sum(to_mutate), 1]) * (data1_Cum[-1]) # pick mutation
                    orf_index = np.searchsorted(data1_Cum, mutate_orf, side='right') # peek mutation
                    #print 'orf_infdex ', orf_index
                    #print orf_index
                    #print mutation
                    # check that they don't mutate the same orf twice.
                    overlap = (mutation[[to_birth[to_mutate]], :] == orf_index)[0]
                    # Warning: Above line, Not the same in ipython as pycharm
                    # (in ipython this line is to be runned without the [0])
                    #print overlap
                    if np.any(overlap):
                        print 'Found mutational overlap'
                        columns = np.nonzero(overlap)[0]#[1][0]
                        orf_index = np.delete(orf_index, columns)
                        compact_to_mutate = np.nonzero(to_mutate)[0]
                        to_mutate[compact_to_mutate[columns]] = False
                        print 'Deleted mutational overlap'

                    first_zeros = np.argmin(mutation[to_birth[to_mutate]],1)
                    mutation[to_birth[to_mutate],first_zeros] = orf_index.T[0]  # store mutation
                    #print mutation[to_birth[to_mutate],:]

                    sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
                        sim_env['cell_cycle_time'][divide_index[to_mutate]] + \
                        gen_time[orf_index, i_env] * MEAN_CELL_CYCLE_TIME

                    sim_env['next_division'][to_birth[to_mutate]] += \
                        sim_env['cell_cycle_time'][to_birth[to_mutate]] - \
                        sim_env['cell_cycle_time'][divide_index[to_mutate]]


            ## Population ages
            #sim_env['age'][:nr_alive] += time_step No reason to track age if we have a set experiment_time
            nr_alive += nr_divide

            # \todo: Save data for Evolutionary tree, Look plot code online. Binary tree!
                # mutations and mothers for all mutated cells
                # nr unmutated cells,
                # time of mutation

            # \todo: Save data to create histogram of mutations

            # \todo: Save data to determine nr of haplotypes.

        # Exit of while-loop
        # Save data for histograms of GT
        gt_cycle[:MAXIMUM_NR_AGENTS, i_cycle] = (sim_env['cell_cycle_time'] - MEAN_CELL_CYCLE_TIME) / MEAN_CELL_CYCLE_TIME

        # Save meanGT
        meanGT[i_cycle] = np.mean(gt_cycle[:,i_cycle]) #np.mean(sim_env['cell_cycle_time'][:MAXIMUM_NR_AGENTS])

        cycle_time = np.append(cycle_time, t) # stores cycle exit time

        # Save data for growth curve (one last time).
        growth = np.append(growth, nr_alive)
        growth_time = np.append(growth_time, t)

        # Sample for next cycle
        if not i_cycle == NR_CYCLES - 1:
            sample = np.random.choice(MAXIMUM_NR_AGENTS, SAMPLE_COUNT,replace=False)
            sim_env[:SAMPLE_COUNT] = sim_env[sample]
            nr_alive = SAMPLE_COUNT
            mutational_sample = mutation[sample]
            mutation =  - np.ones([MAXIMUM_NR_AGENTS, 10], dtype='int16')  # dtype =
            mutation[:SAMPLE_COUNT] = mutational_sample
            sim_env['next_division'][:SAMPLE_COUNT] = sim_env['cell_cycle_time'][:SAMPLE_COUNT]

    # Do After All cycles


    # calculate nr of haploid types
    different_mutations = np.unique(mutation[mutation >= 0])
    count_mutations = np.zeros(len(different_mutations))
    for mut in enumerate(different_mutations):
            count_mutations[mut[0]] = np.count_nonzero(mutation == mut[1])
    sorted_count_index = np.argsort(count_mutations)

    different_mutations = different_mutations[sorted_count_index]
    count_mutations = count_mutations[sorted_count_index]
    different_mutations_ORF_names = data2[different_mutations]
    print different_mutations_ORF_names
    print different_mutations
    print count_mutations
    print [different_mutations, i_env]
    print count_mutations * gen_time[different_mutations, i_env] / MAXIMUM_NR_AGENTS


    # \todo: generate plots, in a seperate function.
    import matplotlib.pyplot as plt
    plt.figure(1, figsize=(2.75, 2.0)) # \todo: Make the growth curves plot on top of each other, maybe by implementing a local, cycle time. As We did from the start.

    plt.plot(growth_time, growth, '-')

    plt.savefig('plt_ex1.pdf')

    plt.figure(2, figsize=(2.75, 2.0))
    plt.plot(meanGT)
    plt.savefig('plt_ex2.pdf')

    #plt.figure(3, figsize=(2.75, 2.0))
    #plt.xticks(different_mutations[-1:-10], different_mutations_ORF_names[-1:-10])
    #plt.hist(mutation[mutation >= 0])

    plt.figure(4, figsize=(2.75, 2.0))
    plt.xticks(range(10), different_mutations_ORF_names[-10:],rotation='vertical')
    plt.bar(np.arange(10)+0.5,count_mutations[-10:])
    plt.xlabel("FOO")
    plt.ylabel("FOO")
    plt.title("Testing")
    plt.yscale('log')

    plt.show()

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
