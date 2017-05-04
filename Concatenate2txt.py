import numpy as np
import pickle
import os
from collections import defaultdict as dd
# Export
dir_out = 'dataConcatenated/'

# Import
dir = 'trashData/'
filename = os.listdir(dir)
filename.sort()
reading_number = len(filename)/4
#distr = np.load(dir + filename[0])

vec1 = []
vec2 = []
big_dic = {'growth': [], 'growth_time': [], 'nr_haploid_types': [], 'tot_nr_mutate': []}
#for i in xrange(reading_number-1):
#    distr = np.concatenate((distr,np.load(dir + filename[i+1])))

for i in xrange(reading_number):
    vec1 = np.concatenate((vec1, np.load(dir + filename[i + reading_number])))
    with open(dir + filename[i + 2 * reading_number], 'rb') as f:
        dic = pickle.load(f)

    save_processed = dd(list)
    for k, v in dic:
        save_processed[k].append(v)

    big_dic['growth'] = np.concatenate((save_processed['growth'], big_dic['growth']))
    big_dic['growth_time'] = np.concatenate((save_processed['growth_time'], big_dic['growth_time']))
    big_dic['nr_haploid_types'] = np.concatenate((save_processed['nr_haploid_types'], big_dic['nr_haploid_types']))
    # big_dic['fixation_at_cycle'] = np.concatenate((save_processed['fixation_at_cycle'], big_dic['fixation_at_cycle']))
    # big_dic['extinction_at_cycle'] = np.concatenate((save_processed['extinction_at_cycle'], big_dic['extinction_at_cycle']))

    print  big_dic['tot_nr_mutate']
    print save_processed['tot_nr_mutate']
    big_dic['tot_nr_mutate'] = np.concatenate((save_processed['tot_nr_mutate'], big_dic['tot_nr_mutate']))

    vec2 = np.concatenate((vec2, np.load(dir + filename[i + 3 * reading_number])))


print 'Concatenation Complete, now Saving...'

# Save data to txt.
orfs = vec1
nr_orfs = vec2

uniq_orfs = np.unique(orfs)
uniq_nr_orfs = np.zeros(len(uniq_orfs))

for j, orf_name in enumerate(uniq_orfs):
    uniq_nr_orfs[j] = np.sum(nr_orfs[(orfs == orf_name)])

import scipy.io as sio

np.savetxt(dir_out + 'uniq_nr_orfs.txt',uniq_nr_orfs,delimiter='\n')
np.savetxt(dir_out + 'uniq_orfs.mat',uniq_orfs})

np.savetxt(dir_out + 'growth.mat', big_dic['growth'], delimiter='\n')
np.savetxt(dir_out + 'growth_time.mat', big_dic['growth_time'], delimiter='\n')
np.savetxt(dir_out + 'nr_haploid_types.mat', big_dic['nr_haploid_types'], delimiter='\n')
np.savetxt(dir_out + 'tot_nr_mutate.mat', big_dic['tot_nr_mutate'], delimiter='\n')
#sio.savemat('fixation_at_cycle.mat', big_dic['fixation_at_cycle'], delimiter='\n')
#sio.savemat('extinction_at_cycle.mat', big_dic['extinction_at_cycle'], delimiter='\n')
#sio.savemat(dir_out + 'distribution_gt', distr, delimiter='\n')

print Done!

