# Initilization of Constants
import numpy as np
from LoadData import orf_target_size_cums #, data3

# GENERAL
MUTATION_RATE           = 0.33*10**-9  # per base, per division.
MUTATION_PROB           = MUTATION_RATE * orf_target_size_cums[-1]
OVERLAP_ALLOWED         = True  # Is > 1 mutation per orf for each agent allowed? (False recommended)
TIME_STEP               = 20  #[min]

# CONSTANT:
# scalars
NR_CYCLES               = 20
FOUNDER_COUNT           = 10**5 # Nr. initial agents.
SAMPLE_COUNT            = 10**5 # Nr. sampled agents after each cycle
YIELD                   = 5 # Nr. of allowed population doublings.
MAXIMUM_NR_AGENTS       = FOUNDER_COUNT*2**YIELD # per cycle,
MAXIMUM_NR_DIVISIONS    = 1000
MEAN_LAG_TIME           = 90 # [min]  # Happens in the beginning of each cycle. Cells will not further its cell cycle while in lag.
MEAN_CELL_CYCLE_TIME    = 90 # [min]
EXPERIMENT_TIME         = 1 #72*60 # [min]


# vectors
LAG_TIMES               = MEAN_LAG_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
CELL_CYCLE_TIMES        = MEAN_CELL_CYCLE_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
FOUNDER_ID              = range(FOUNDER_COUNT)
