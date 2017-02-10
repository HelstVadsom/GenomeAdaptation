# Initilization of Constants, parameters and distributions.
#import numpy as np

# GENERAL
DTYPE1 = 'float16'
DTYPE2 = 'uint8'
MINIMUM_TIME_RESOLUTION = .1 # [min] (0.1 min = 6 sek) min: ~6 otherwise change float16 @ CreateInd...


# CONSTANT:
# scalars
FOUNDER_COUNT = 10^5 # Nr. initial agents.

SAMPLE_COUNT = 10^5 # Nr. sampled agents for each cycle

YIELD = 5 # Nr. population doublings.

NR_CYCLES = 50

LAG_TIME_MEAN = 90 # [min]

CELL_CYCLE_TIME_MEAN = 90 # [min]

GENOME_LENGTH = 5 # Nr. of possible mutations. max: 9, otherwise change uint8 @ CreateInd...

MAXIMUM_NR_AGENTS = FOUNDER_COUNT*2^YIELD # per cycle

# vectors
LAG_TIMES = LAG_TIME_MEAN + np.random.normal(0, 1, [FOUNDER_COUNT, 1])

CELL_CYCLE_TIMES = CELL_CYCLE_TIME_MEAN + np.random.normal(0, 1, [FOUNDER_COUNT, 1])

FOUNDER_ID = np.array([range(FOUNDER_COUNT)]).T # max: 4,294,967,295

#MUTATION_PROB = data1[range(5)]

#MUTATION_CELL_CYCLE_EFFECT = [0.5, 1.2


# CHANGEABLE:
# vectors
lag_progress = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = DTYPE1)

lag_time = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = DTYPE1)
lag_time[0:FOUNDER_COUNT] = LAG_TIMES

cell_cycle_time = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = DTYPE1)
cell_cycle_time[0:FOUNDER_COUNT] = CELL_CYCLE_TIMES

mutation = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = DTYPE2)

founder_ID = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = "uint32")
founder_ID[0:FOUNDER_COUNT] = FOUNDER_ID

age = np.zeros([MAXIMUM_NR_AGENTS,1],dtype = DTYPE1) # unsure Dtype

