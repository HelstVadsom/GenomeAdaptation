# Initilization of Constants, parameters and distributions.
import numpy as np
from LoadData import data3

# GENERAL
DTYPE1 = 'float16'
DTYPE2 = 'uint8'
MINIMUM_TIME_RESOLUTION = .1 # [min] (0.1 min = 6 sek) min: ~6 otherwise change float16 @ CreateInd...
# should be quantized to float16 decimal
MUTATION_RATE = 0.33*10**-9 # per base, per division.
GENOME_SIZE = 1.3*10**7 # nr. of bases
ORF_SIZE = sum(data3)
PROB_MUTATION = MUTATION_RATE * ORF_SIZE

## CONSTANT:
# scalars
NR_ENVIRONMENTS = 1#8
NR_CYCLES = 1#50
FOUNDER_COUNT = 10**5 # Nr. initial agents.
SAMPLE_COUNT = 10**5 # Nr. sampled agents for each cycle
YIELD = 5 # Nr. population doublings.
MAXIMUM_NR_AGENTS = FOUNDER_COUNT*2**YIELD # per cycle
MEAN_LAG_TIME = 90 # [min]
MEAN_CELL_CYCLE_TIME = 90 # [min]
GENOME_LENGTH = 5 # Nr. of possible mutations. max: 9, otherwise change uint8 @ CreateInd...

# vectors
LAG_TIMES = MEAN_LAG_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
CELL_CYCLE_TIMES = MEAN_CELL_CYCLE_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
FOUNDER_ID = range(FOUNDER_COUNT) #np.array(range(FOUNDER_COUNT)).T # max: 4,294,967,295

## CHANGEABLE:
# scalars
nr_alive = FOUNDER_COUNT

# vectors
lag_progress = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)

lag_time = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)
lag_time[0:FOUNDER_COUNT] = LAG_TIMES

cell_cycle_time = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)
cell_cycle_time[0:FOUNDER_COUNT] = CELL_CYCLE_TIMES

mutation = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE2)

founder_id = np.zeros([MAXIMUM_NR_AGENTS],dtype = "uint32")
founder_id[0:FOUNDER_COUNT] = FOUNDER_ID

age = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1) # unsure Dtype
age[0:FOUNDER_COUNT] = 1 # Born
