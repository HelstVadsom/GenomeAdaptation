import numpy as np
from InitilizeConstants import *

DTYPE1 = 'float16'
DTYPE2 = 'uint8'

lag_time                        = np.zeros([MAXIMUM_NR_AGENTS], dtype=DTYPE1)
lag_time[:FOUNDER_COUNT]        = LAG_TIMES
cell_cycle_time                 = np.zeros([MAXIMUM_NR_AGENTS], dtype=DTYPE1)
cell_cycle_time[:FOUNDER_COUNT] = CELL_CYCLE_TIMES
founder_id                      = np.zeros([MAXIMUM_NR_AGENTS], dtype="uint32")
founder_id[:FOUNDER_COUNT]      = FOUNDER_ID
age                             = np.zeros([MAXIMUM_NR_AGENTS], dtype='float64')
nr_divisions                    = np.zeros([MAXIMUM_NR_AGENTS], dtype=DTYPE1)

# pre-allocate
sim_env = np.zeros(MAXIMUM_NR_AGENTS, dtype={'names':['lag_time', 'cell_cycle_time', 'next_division_time',
                                                       'founder_id', 'age', 'nr_divisions', 'division_time', 'mutation'],
                                            'formats':[DTYPE1, DTYPE1, DTYPE1, 'uint32', DTYPE1, DTYPE2, DTYPE1, 'uint16']})

# initilize
sim_env['lag_time'] = lag_time
sim_env['cell_cycle_time'] = cell_cycle_time
sim_env['next_division_time']  = lag_time + cell_cycle_time
sim_env['founder_id'] = founder_id
sim_env['age'] = age
sim_env['nr_divisions'] = nr_divisions

mutation =  - np.ones([MAXIMUM_NR_AGENTS, 10], dtype = 'int16')
