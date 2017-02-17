#import numpy as np
from InitilizeParameters import *

# pre-allocate
simEnv = np.zeros(MAXIMUM_NR_AGENTS,dtype = {'names':['lag_time','lag_progress','cell_cycle_time','mutation','founder_id','age'],\
                                      'formats':[DTYPE1,DTYPE1,DTYPE1,DTYPE2,'uint32',DTYPE1]})

# initilize
simEnv['lag_time'] = lag_time
simEnv['lag_progress'] = lag_progress
simEnv['cell_cycle_time'] = cell_cycle_time
simEnv['mutation'] = mutation
simEnv['founder_id'] = founder_id
simEnv['age'] = age
