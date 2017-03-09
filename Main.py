"""This code grows yeast-cells that divide and mutate to adapt to an evolutionary pressure (a toxic environment).
 The growth happens in cycles where at the end of each cycle the population is reduced to then regrow in the next cycle.
 Over these cycles, agents collect mutations that can change its cycle time, making it divide faster or slower.

 The size of such a change is determined by deletion data (i.e real measurements of yeast growth change for each Loss of
 ORF-function for each evolutionary pressure.
 The likelihood of such mutations is weighted by the yeast's number of Non-Synonymous nucleotides for each ORF."""


def set_up():
    Data = nt('Data', ['orf_target_size_cums', 'gen_time', 'orfs'], verbose=True)
    d = Data(orf_target_size_cums, gen_time, orfs)

    Constants = nt('Constants', ['NR_CYCLES', 'FOUNDER_COUNT', 'SAMPLE_COUNT', 'YIELD', 'MAXIMUM_NR_AGENTS', 'MEAN_LAG_TIME',
                                                     'MEAN_CELL_CYCLE_TIME', 'EXPERIMENT_TIME', 'MUTATION_PROB',
                                                     'LAG_TIMES', 'CELL_CYCLE_TIMES', 'FOUNDER_ID'], verbose=True)
    c = Constants(NR_CYCLES, FOUNDER_COUNT, SAMPLE_COUNT, YIELD, MAXIMUM_NR_AGENTS, MEAN_LAG_TIME, MEAN_CELL_CYCLE_TIME,
                  EXPERIMENT_TIME, MUTATION_PROB, LAG_TIMES, CELL_CYCLE_TIMES, FOUNDER_ID)

    time_step = 20  # [min]
    nr_alive = int(c.FOUNDER_COUNT)

    return c, d, time_step, nr_alive


def lag_f(c, sim_env, i_cycle, lag, is_lagging, t, time_step):
    if lag:
        was_lagging = is_lagging
        if i_cycle == 0:
            is_lagging = (sim_env['lag_time'][:c.FOUNDER_COUNT] > t)
        else:
            is_lagging = (sim_env['lag_time'][:c.SAMPLE_COUNT] > t)
        lag = any(is_lagging)
        sim_env['next_division_time'][is_lagging] += time_step  # Postpone next division
        lag_escapists = np.bool_(was_lagging * (1 - is_lagging))
        sim_env['next_division_time'][lag_escapists] -= t - sim_env['lag_time'][lag_escapists]
    return lag, is_lagging, sim_env


def save_growth(s, nr_alive, t):
    s.append(('growth', nr_alive))
    s.append(('growth_time', t))
    return s


def save_importants(c, s, i_cycle, distribution_gt, nr_alive, t, mutation, sim_env):
    s.append(('nr_haploid_types', calc_nr_haplotypes(c, mutation)))
    distribution_gt[:c.MAXIMUM_NR_AGENTS, i_cycle] = (sim_env['cell_cycle_time'] - c.MEAN_CELL_CYCLE_TIME) / c.MEAN_CELL_CYCLE_TIME
    s.append(('mean_gt', np.mean(distribution_gt[:, i_cycle])))

    s = save_growth(s, nr_alive, t)
    return s, distribution_gt


def divide(c, d, mutation, sim_env, nr_alive, t, still_in_cycle, environment):
    to_divide = (sim_env['next_division_time'][:nr_alive] <= t)
    nr_divide = np.sum(to_divide)
    if nr_divide:
        to_divide_nz = np.nonzero(to_divide)[0]
        to_birth = np.arange(nr_alive, (nr_alive + nr_divide))

        if nr_alive + len(to_birth) >= c.MAXIMUM_NR_AGENTS: # Checks if it's time to begin a new cycle.
            nr_divide_reduced = c.MAXIMUM_NR_AGENTS - nr_alive
            to_birth = np.arange(nr_alive, (nr_alive + nr_divide_reduced))
            to_divide_nz = to_divide_nz[np.random.choice(nr_divide, nr_divide_reduced, replace=False)]
            to_divide = to_divide_nz
            nr_divide = nr_divide_reduced
            sim_env['age'][:MAXIMUM_NR_AGENTS] += c.EXPERIMENT_TIME
            still_in_cycle = 0
            print 'About to exit cycle'

        sim_env['founder_id'][to_birth] = to_divide_nz # Copies traits
        sim_env['lag_time'][to_birth] = sim_env['lag_time'][to_divide]
        sim_env['cell_cycle_time'][to_birth] = sim_env['cell_cycle_time'][to_divide]
        sim_env['next_division_time'][to_divide] += sim_env['cell_cycle_time'][to_divide]
        sim_env['next_division_time'][to_birth] = sim_env['next_division_time'][to_divide]
        sim_env['nr_divisions'][to_divide] += 1
        mutation[to_birth] = mutation[to_divide]

        ## Mutate
        sim_env, mutation = mutate(c, d, mutation, sim_env, nr_divide, to_birth, to_divide_nz, environment)
        nr_alive += nr_divide
    return nr_alive, sim_env, mutation, still_in_cycle


def mutate(c, d, mutation, sim_env, nr_divide, to_birth, to_divide_nz, environment):
    to_mutate = np.random.random(nr_divide) < c.MUTATION_PROB
    if any(to_mutate):
        mutation_cite = np.random.random([sum(to_mutate), 1]) * (d.orf_target_size_cums[-1])  # pick mutation
        orf_mutation = np.searchsorted(d.orf_target_size_cums, mutation_cite, side='right')  # peek mutation
        
        overlap = (mutation[[to_birth[to_mutate]], :] == orf_mutation)[0]  # forbids > 1 mutation per orf for each agent.
        # Warning: Above line, Not the same in ipython as pycharm
        # (in ipython this line is to be exec. without the [0]).
        if np.any(overlap):
            print 'Found mutational overlap'
            overlapping_columns = np.nonzero(overlap)[0]
            orf_mutation = np.delete(orf_mutation, overlapping_columns)  # disposes agents ORF mutation.
            orf_mutation_nz = np.nonzero(to_mutate)[0]
            to_mutate[orf_mutation_nz[overlapping_columns]] = False  # prevents agents ORF to mutate.
            print 'Deleted mutational overlap'

        index_free_from_mutation = np.argmin(mutation[to_birth[to_mutate]], 1)
        mutation[to_birth[to_mutate], index_free_from_mutation] = orf_mutation.T[0]  # store mutation

        sim_env['cell_cycle_time'][to_birth[to_mutate]] = \
            sim_env['cell_cycle_time'][to_divide_nz[to_mutate]] + \
            d.gen_time[orf_mutation, environment] * c.MEAN_CELL_CYCLE_TIME

        sim_env['next_division_time'][to_birth[to_mutate]] += \
            sim_env['cell_cycle_time'][to_birth[to_mutate]] - \
            sim_env['cell_cycle_time'][to_divide_nz[to_mutate]]

    return sim_env, mutation


def sample_and_reset(c, mutation, sim_env):
    # Sample for next cycle
    sample = np.random.choice(c.MAXIMUM_NR_AGENTS, c.SAMPLE_COUNT, replace=False)
    sim_env[:c.SAMPLE_COUNT] = sim_env[sample]
    nr_alive = c.SAMPLE_COUNT
    mutational_sample = mutation[sample]
    mutation = - np.ones([c.MAXIMUM_NR_AGENTS, 10], dtype='int16')
    mutation[:SAMPLE_COUNT] = mutational_sample
    sim_env['next_division_time'][:c.SAMPLE_COUNT] = sim_env['cell_cycle_time'][:c.SAMPLE_COUNT]
    return sim_env, mutation, nr_alive


def process_data_and_plot(c, d, s, mutation, environment):
    s_new = dd(list)
    for k, v in s:
        s_new[k].append(v)

    growth_index = np.where(s_new['growth'] == c.MAXIMUM_NR_AGENTS)[0] + 1
    growth_index = np.insert(growth_index, 0, 0)

    unique_mutations = np.unique(mutation[mutation >= 0])
    nr_unique_mutations = np.zeros(len(unique_mutations))
    for mut in enumerate(unique_mutations):
            nr_unique_mutations[mut[0]] = np.count_nonzero(mutation == mut[1])
    sorted_count_index = np.argsort(nr_unique_mutations)

    unique_mutations = unique_mutations[sorted_count_index]
    nr_unique_mutations = nr_unique_mutations[sorted_count_index]
    unique_mutated_orfs = orfs[unique_mutations]
    print unique_mutated_orfs
    print unique_mutations
    print nr_unique_mutations
    print [unique_mutations, environment]
    print nr_unique_mutations * d.gen_time[unique_mutations, environment] / c.MAXIMUM_NR_AGENTS
    plot_importants(unique_mutated_orfs, nr_unique_mutations, s_new, growth_index)


def calc_nr_haplotypes(c, mutation):
    m = np.sort(mutation)
    haplo_types = np.zeros(c.MAXIMUM_NR_AGENTS)
    for i in xrange(c.MAXIMUM_NR_AGENTS):
        haplo_types[i] = hash(
            (m[i, 0], m[i, 1], m[i, 2], m[i, 3], m[i, 4], m[i, 5], m[i, 6], m[i, 7], m[i, 8], m[i, 9]))

    nr_haplotypes = len(np.unique(haplo_types))
    print 'Nr. different haploid types: ', nr_haplotypes
    return nr_haplotypes


def plot_importants(unique_mutated_orfs, nr_unique_mutations, s, growth_index):

    import matplotlib.pyplot as plt
    plt.figure(1, figsize=(2.75, 2.0))
    for i in range(len(growth_index) - 1):
        plt.plot(s['growth_time'][growth_index[i]:growth_index[i+1]], s['growth'][growth_index[i]:growth_index[i+1]], '-')
    plt.xlabel("t [min]")
    plt.ylabel("Population")
    plt.title("Growth Curves")

    plt.figure(2, figsize=(2.75, 2.0))
    plt.plot(s['mean_gt'])
    plt.xlabel("Cycle")
    plt.ylabel("Mean GT")
    plt.title("Mean GT")

    fig = plt.figure(3, figsize=(2.75, 2.0))
    ax = fig.add_subplot(111)
    if len(unique_mutated_orfs) > 10:
        plt.xticks(np.arange(10) + 0.4, unique_mutated_orfs[-10:],rotation='vertical')
        ax.bar(np.arange(10), nr_unique_mutations[-10:], log=True)
    else:
        plt.xticks(np.arange(5) + 0.4, unique_mutated_orfs[-5:],rotation='vertical')
        ax.bar(np.arange(5), nr_unique_mutations[-5:], log=True)
    ax.set_xlabel("ORF Names")
    ax.set_ylabel("Nr. of Copies")
    ax.set_title("Top Mutations")
    ax.set_yscale('log', nonposy="clip")

    plt.figure(4, figsize=(2.75, 2.0))
    plt.plot(s['nr_haploid_types'])
    plt.xlabel("Cycle")
    plt.ylabel("Nr. of Haploid Types")
    plt.show()


def run(environment):
    from CreateIndividuals import sim_env, mutation
    c, d, time_step, nr_alive = set_up()

    s = [('growth', c.FOUNDER_COUNT), ('growth_time', 0), ('nr_haploid_types', 0)] # 1D saveables
    distribution_gt = np.zeros([c.MAXIMUM_NR_AGENTS, c.NR_CYCLES])

    for i_cycle in xrange(c.NR_CYCLES):
        i_cycle = i_cycle
        print 'environment = ', environment, 'i_cycle = ', i_cycle
        t = 0
        lag = 1
        is_lagging = np.ones(nr_alive)
        still_in_cycle = 1

        while still_in_cycle:
            lag, is_lagging, sim_env = lag_f(c, sim_env, i_cycle, lag, is_lagging, t, time_step)
            s = save_growth(s, nr_alive, t)
            t += time_step
            nr_alive, sim_env, mutation, still_in_cycle = \
                divide(c, d, mutation, sim_env, nr_alive, t, still_in_cycle, environment)
            # \todo: Save data to determine nr of haplotypes.

        # Do After a cycle
        s, distribution_gt = save_importants(c, s, i_cycle, distribution_gt, nr_alive, t, mutation, sim_env)
        if i_cycle != c.NR_CYCLES - 1:
            sim_env, mutation, nr_alive = sample_and_reset(c, mutation, sim_env)

    # Do After All cycles
    process_data_and_plot(c, d, s, mutation, environment)

if __name__ == "__main__": # \todo Create functions
    import numpy as np
    from collections import namedtuple as nt
    from collections import defaultdict as dd
    from LoadData import orf_target_size_cums, gen_time, orfs
    from InitilizeConstants import *

    run(environment=0)
    #  MEMORY TABLE:
    # 'Arsenite'   (environment = 0)
    # 'Citric_Acid'(environment = 1)
    # 'Citrulline' (environment = 2)
    # 'Glycine'    (environment = 3)
    # 'Isoleucine' (environment = 4)
    # 'Paraquat'   (environment = 5)
    # 'Rapamycin'  (environment = 6)
    # 'SC'         (environment = 7)
    # 'Tryptophan' (environment = 8)

