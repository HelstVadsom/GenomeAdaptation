#import numpy as np
from InitilizeParameters import *

# pre-allocate
simEnv = np.zeros(MAXIMUM_NR_AGENTS,dtype = {'names':['lag_time','lag_progress','cell_cycle_time','next_divition','founder_id','age','nr_divitions'],\
                                      'formats':[DTYPE1,DTYPE1,DTYPE1,DTYPE1,'uint32',DTYPE1,DTYPE2]})

# initilize
simEnv['lag_time'] = lag_time
simEnv['lag_progress'] = lag_progress
simEnv['cell_cycle_time'] = cell_cycle_time
simEnv['next_divition']  = cell_cycle_time
#simEnv['mutation'] = mutation
simEnv['founder_id'] = founder_id
simEnv['age'] = age
simEnv['nr_divitions'] = nr_divitions
