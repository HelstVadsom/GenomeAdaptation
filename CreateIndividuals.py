#import numpy as np
from InitilizeParameters import *

# pre-allocate
sim_env = np.zeros(MAXIMUM_NR_AGENTS,dtype = {'names':['lag_time','lag_escape','cell_cycle_time','next_division','founder_id','age','nr_divisions','division_time','mutation'],\
                                      'formats':[DTYPE1,DTYPE1,DTYPE1,DTYPE1,'uint32',DTYPE1,DTYPE2,DTYPE1,'uint16']})

# initilize
sim_env['lag_time'] = lag_time
sim_env['lag_escape'] = lag_escape
sim_env['cell_cycle_time'] = cell_cycle_time
sim_env['next_division']  = cell_cycle_time
sim_env['founder_id'] = founder_id
sim_env['age'] = age
sim_env['nr_divisions'] = nr_divisions
sim_env['division_time'] = division_time
#sim_env['mutation'] = mutation
