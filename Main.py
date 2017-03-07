

def lag_f(c, sim_env, i_cycle, lag, lagging, t):
    if lag:
        prev_lagging = lagging

        if i_cycle == 0:
            lagging = (sim_env['lag_time'][:c.FOUNDER_COUNT] > t)
        else:
            lagging = (sim_env['lag_time'][:c.SAMPLE_COUNT] > t)

        lag = any(lagging)
        sim_env['next_division'][lagging] += time_step  # Postpone next division
        lag_escapists = np.bool_(prev_lagging * (1 - lagging))
        sim_env['next_division'][lag_escapists] -= t - sim_env['lag_time'][lag_escapists]
    return sim_env


def save_growth(growth, growth_time, nr_alive, t): # Save data for growth curve.
    growth = np.append(growth, nr_alive)
    growth_time = np.append(growth_time, t)
    return growth, growth_time


def save_importants(c, i_cycle, growth, growth_time, meanGT, gt_cycle, cycle_time, nr_alive, t, nr_haploid_types):

    nr_haploid_types[i_cycle] = calc_nr_haplotypes(c, mutation)

    # Save data for histograms of GT
    gt_cycle[:c.MAXIMUM_NR_AGENTS, i_cycle] = (sim_env['cell_cycle_time'] - c.MEAN_CELL_CYCLE_TIME) / c.MEAN_CELL_CYCLE_TIME

    # Save meanGT
    meanGT[i_cycle] = np.mean(gt_cycle[:, i_cycle])  # np.mean(sim_env['cell_cycle_time'][:MAXIMUM_NR_AGENTS])

    cycle_time = np.append(cycle_time, t)  # stores cycle exit time

    # Save data for growth curve (one last time).
    growth, growth_time = save_growth(growth, growth_time, nr_alive, t)

    return growth, growth_time, meanGT, gt_cycle, cycle_time, nr_haploid_types


def divide(c, d, mutation, sim_env, nr_alive, t, still_in_cycle):
    to_divide = (sim_env['next_division'][:nr_alive] <= t)
    nr_divide = np.sum(to_divide)
    if nr_divide:
        divide_index = np.nonzero(to_divide)[0]
        to_birth = np.arange(nr_alive, (nr_alive + nr_divide))

        if nr_alive + len(to_birth) >= c.MAXIMUM_NR_AGENTS:  # Checks if it's time to begin a new cycle.
            nr_divide_reduced = c.MAXIMUM_NR_AGENTS - nr_alive
            to_birth = np.arange(nr_alive, (nr_alive + nr_divide_reduced))
            divide_index = divide_index[np.random.choice(nr_divide, nr_divide_reduced, replace=False)]
            to_divide = divide_index
            nr_divide = nr_divide_reduced
            # full = 1
            sim_env['age'][:MAXIMUM_NR_AGENTS] += c.EXPERIMENT_TIME
            still_in_cycle = 0
            print 'About to exit cycle'

        sim_env['founder_id'][to_birth] = divide_index
        sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
        sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
        sim_env['next_division'][to_divide] += sim_env['cell_cycle_time'][to_divide]
        sim_env['next_division'][to_birth] = sim_env['next_division'][to_divide]
        sim_env['nr_divisions'][to_divide] += 1
        mutation[to_birth] = mutation[to_divide]

        ## Mutate
        sim_env, mutation = mutate(c, d, mutation, sim_env, nr_divide, to_birth, divide_index)
        nr_alive += nr_divide
    return nr_alive, sim_env, mutation, still_in_cycle


def mutate(c, d, mutation, sim_env, nr_divide, to_birth, divide_index):
    to_mutate = np.random.random(nr_divide) < c.PROB_MUTATION
    if any(to_mutate):
        mutate_orf = np.random.random([sum(to_mutate), 1]) * (d.nr_LOFM_cumsum[-1])  # pick mutation
        orf_index = np.searchsorted(nr_LOFM_cumsum, mutate_orf, side='right')  # peek mutation
        overlap = (mutation[[to_birth[to_mutate]], :] == orf_index)[0] # check that they don't mutate the same orf twice.
        # Warning: Above line, Not the same in ipython as pycharm
        # (in ipython this line is to be runned without the [0])
        if np.any(overlap):
            print 'Found mutational overlap'
            columns = np.nonzero(overlap)[0]  # [1][0]
            orf_index = np.delete(orf_index, columns)
            compact_to_mutate = np.nonzero(to_mutate)[0]
            to_mutate[compact_to_mutate[columns]] = False
            print 'Deleted mutational overlap'

        first_zeros = np.argmin(mutation[to_birth[to_mutate]], 1)
        mutation[to_birth[to_mutate], first_zeros] = orf_index.T[0]  # store mutation
        # print mutation[to_birth[to_mutate],:]

        sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
            sim_env['cell_cycle_time'][divide_index[to_mutate]] + \
            d.gen_time[orf_index, i_env] * c.MEAN_CELL_CYCLE_TIME

        sim_env['next_division'][to_birth[to_mutate]] += \
            sim_env['cell_cycle_time'][to_birth[to_mutate]] - \
            sim_env['cell_cycle_time'][divide_index[to_mutate]]

    return sim_env, mutation

def sample_and_reset(c, mutation, sim_env):
    # Sample for next cycle
    sample = np.random.choice(c.MAXIMUM_NR_AGENTS, c.SAMPLE_COUNT, replace=False)
    sim_env[:c.SAMPLE_COUNT] = sim_env[sample]
    nr_alive = c.SAMPLE_COUNT
    mutational_sample = mutation[sample]
    mutation = - np.ones([c.MAXIMUM_NR_AGENTS, 10], dtype='int16')
    mutation[:SAMPLE_COUNT] = mutational_sample
    sim_env['next_division'][:c.SAMPLE_COUNT] = sim_env['cell_cycle_time'][:c.SAMPLE_COUNT]
    return sim_env, mutation, nr_alive


def process_data_and_plot(c, d, mutation, growth, growth_time, meanGT):
    nr_haploid_types = calc_nr_haplotypes(c, mutation)

    different_mutations = np.unique(mutation[mutation >= 0])
    count_mutations = np.zeros(len(different_mutations))
    for mut in enumerate(different_mutations):
            count_mutations[mut[0]] = np.count_nonzero(mutation == mut[1])
    sorted_count_index = np.argsort(count_mutations)

    different_mutations = different_mutations[sorted_count_index]
    count_mutations = count_mutations[sorted_count_index]
    different_mutations_ORF_names = orfs[different_mutations]
    print different_mutations_ORF_names
    print different_mutations
    print count_mutations
    print [different_mutations, i_env]
    print count_mutations * d.gen_time[different_mutations, i_env] / c.MAXIMUM_NR_AGENTS
    plot_importants(different_mutations_ORF_names, count_mutations, growth, growth_time, meanGT)


def calc_nr_haplotypes(c, mutation):
    m = mutation
    haplo_types = np.zeros(c.MAXIMUM_NR_AGENTS)
    for i in xrange(c.MAXIMUM_NR_AGENTS):
        haplo_types[i] = hash(
            (m[i, 0], m[i, 1], m[i, 2], m[i, 3], m[i, 4], m[i, 5], m[i, 6], m[i, 7], m[i, 8], m[i, 9]))

    nr_haplotypes = len(np.unique(haplo_types))

    return nr_haplotypes


def plot_importants(different_mutations_ORF_names, count_mutations, growth, growth_time, meanGT):

    import matplotlib.pyplot as plt
    plt.figure(1, figsize=(2.75, 2.0))

    plt.plot(growth_time, growth, '-')

    plt.savefig('plt_ex1.pdf')

    plt.figure(2, figsize=(2.75, 2.0))
    plt.plot(meanGT)
    plt.savefig('plt_ex2.pdf')

    plt.figure(4, figsize=(2.75, 2.0))
    plt.xticks(np.arange(10) + 0.4, different_mutations_ORF_names[-10:],rotation='vertical')
    plt.bar(np.arange(10), count_mutations[-10:], log=True)
    plt.xlabel("FOO")
    plt.ylabel("FOO")
    plt.title("Testing")
    plt.yscale('log')

    plt.show()


def run(c, d, mutation, sim_env, i_env, time_step):
    nr_alive = c.FOUNDER_COUNT
    growth = c.FOUNDER_COUNT
    growth_time = 0
    meanGT = np.zeros(c.NR_CYCLES)
    nr_haploid_types = np.zeros(c.NR_CYCLES)
    gt_cycle = np.zeros([c.MAXIMUM_NR_AGENTS,c.NR_CYCLES])
    cycle_time = 0

    for i_cycle in xrange(c.NR_CYCLES):
        i_cycle = i_cycle
        print 'i_env = ', i_env, 'i_cycle = ', i_cycle
        t = 0
        lag = 1
        lagging = np.ones(nr_alive)
        still_in_cycle = 1

        while still_in_cycle:
            sim_env = lag_f(c, sim_env, i_cycle, lag, lagging, t)
            growth, growth_time = save_growth(growth, growth_time, nr_alive, t)
            t += time_step
            nr_alive, sim_env, mutation, still_in_cycle = divide(c, d, mutation, sim_env, nr_alive, t, still_in_cycle)
            # \todo: Save data to determine nr of haplotypes.

        # Do After a cycle
        growth, growth_time, meanGT, gt_cycle, cycle_time, nr_haploid_types \
            = save_importants(c, i_cycle, growth, growth_time, meanGT, gt_cycle, cycle_time, nr_alive, t, nr_haploid_types)
        if not i_cycle == c.NR_CYCLES - 1:
            sim_env, mutation, nr_alive = sample_and_reset(c, mutation, sim_env)

    # Do After All cycles
    process_data_and_plot(c, d, mutation, growth, growth_time, meanGT)

if __name__ == "__main__": # \todo Create functions
    import numpy as np
    import collections
    from LoadData import *
    from InitilizeConstants import *
    from CreateIndividuals import sim_env, mutation

    Data = collections.namedtuple('Data', ['nr_LOFM_cumsum', 'gen_time', 'orfs'], verbose=True)
    d = Data(nr_LOFM_cumsum, gen_time, orfs)

    Constants = collections.namedtuple('Constants', ['NR_CYCLES', 'FOUNDER_COUNT', 'SAMPLE_COUNT',
                                                     'YIELD', 'MAXIMUM_NR_AGENTS', 'MEAN_LAG_TIME',
                                                     'MEAN_CELL_CYCLE_TIME', 'EXPERIMENT_TIME', 'PROB_MUTATION',
                                                     'LAG_TIMES', 'CELL_CYCLE_TIMES', 'FOUNDER_ID'], verbose=True)
    c = Constants(NR_CYCLES, FOUNDER_COUNT, SAMPLE_COUNT, YIELD, MAXIMUM_NR_AGENTS, MEAN_LAG_TIME, MEAN_CELL_CYCLE_TIME,
                  EXPERIMENT_TIME, PROB_MUTATION, LAG_TIMES, CELL_CYCLE_TIMES, FOUNDER_ID)

    i_env = 0
    time_step = 20

    run(c, d, mutation, sim_env, i_env, time_step)
    # \todo: Clean up the code! it's messy!

    #  MEMORY TABLE:
    # 'Arsenite'   (i_env = 0)
    # 'Citric_Acid'(i_env = 1)
    # 'Citrulline' (i_env = 2)
    # 'Glycine'    (i_env = 3)
    # 'Isoleucine' (i_env = 4)
    # 'Paraquat'   (i_env = 5)
    # 'Rapamycin'  (i_env = 6)
    # 'SC'         (i_env = 7)
    # 'Tryptophan' (i_env = 8)
