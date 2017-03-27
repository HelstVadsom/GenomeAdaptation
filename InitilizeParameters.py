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
A_MYSTICAL_SPEED_UP_PARAMETER = 0.4 # Parameter value was set after trying a a few numbers.

## CONSTANT:
# scalars
NR_ENVIRONMENTS = 1#8
NR_CYCLES = 3#50
FOUNDER_COUNT = 10**5 # Nr. initial agents.
SAMPLE_COUNT = 10**5 # Nr. sampled agents for each cycle
YIELD = 5 # Nr. population doublings.
MAXIMUM_NR_AGENTS = FOUNDER_COUNT*2**YIELD # per cycle,
MEAN_LAG_TIME = 90 # [min]
MEAN_CELL_CYCLE_TIME = 90 # [min]
#GENOME_LENGTH = 5 # Nr. of possible mutations. max: 9, otherwise change uint8 @ CreateInd...
MEASUREMENTS_AT_EVERY = 20 # [min], put = 0 for measurements at ALL relevant time-steps.

# vectors
LAG_TIMES = MEAN_LAG_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
CELL_CYCLE_TIMES = MEAN_CELL_CYCLE_TIME + np.random.normal(0, 1, [FOUNDER_COUNT])
FOUNDER_ID = range(FOUNDER_COUNT) # max: 4,294,967,295

## CHANGEABLE:
# scalars
nr_alive = FOUNDER_COUNT
lag = 1
meanGT = np.zeros(50)
gt_cycle = np.zeros([MAXIMUM_NR_AGENTS,NR_CYCLES])
#to_divide = np.zeros(MAXIMUM_NR_AGENTS,dtype = 'bool_')
#to_birth = np.zeros(MAXIMUM_NR_AGENTS,dtype = 'uint32')
# vectors
lag_escape = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)

lag_time = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)
lag_time[0:FOUNDER_COUNT] = LAG_TIMES

cell_cycle_time = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)
cell_cycle_time[0:FOUNDER_COUNT] = CELL_CYCLE_TIMES

mutation = np.zeros([MAXIMUM_NR_AGENTS],dtype = 'uint16')

founder_id = np.zeros([MAXIMUM_NR_AGENTS],dtype = "uint32")
founder_id[0:FOUNDER_COUNT] = FOUNDER_ID

age = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1) # unsure Dtype

nr_divitions = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)

divition_time = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)

mutation = np.zeros([MAXIMUM_NR_AGENTS],dtype = DTYPE1)
