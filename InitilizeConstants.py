# Initilization of Constants
import numpy as np
from LoadData import nr_LOFM_cumsum #data3

# GENERAL
MUTATION_RATE = 0.33*10**-9 # per base, per division.
PROB_MUTATION = MUTATION_RATE * nr_LOFM_cumsum[-1]

## CONSTANT:
# scalars
NR_CYCLES = 50
FOUNDER_COUNT = 10**5 # Nr. initial agents.
SAMPLE_COUNT = 10**5 # Nr. sampled agents for each cycle
YIELD = 5 # Nr. population doublings.
MAXIMUM_NR_AGENTS = FOUNDER_COUNT*2**YIELD # per cycle,
MEAN_LAG_TIME = 90 # [min]
MEAN_CELL_CYCLE_TIME = 90 # [min]
EXPERIMENT_TIME = 72*60

# vectors
LAG_TIMES = MEAN_LAG_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
CELL_CYCLE_TIMES = MEAN_CELL_CYCLE_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
FOUNDER_ID = range(FOUNDER_COUNT) # max: 4,294,967,295
