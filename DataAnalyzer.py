import numpy as np
import pickle
import os
from collections import defaultdict as dd

# Import
dir = 'neutralModelData/'
filename = os.listdir(dir)
filename.sort()
reading_number = len(filename)/3
vec1 = []
vec2 = []
big_dic = {'growth': [], 'growth_time': [], 'nr_haploid_types': [], 'tot_nr_mutate': []}

for i in xrange(reading_number):

    vec1 = np.concatenate((vec1, np.load(dir + filename[i])))
    with open(dir + filename[i + reading_number], 'rb') as f:
        dic = pickle.load(f)

    save_processed = dd(list)
    for k, v in dic:
        save_processed[k].append(v)

    big_dic['growth'] = np.concatenate((save_processed['growth'], big_dic['growth']))
    big_dic['growth_time'] = np.concatenate((save_processed['growth_time'], big_dic['growth_time']))
    big_dic['nr_haploid_types'] = np.concatenate((save_processed['nr_haploid_types'], big_dic['nr_haploid_types']))
    print  big_dic['tot_nr_mutate']
    print save_processed['tot_nr_mutate']
    big_dic['tot_nr_mutate'] = np.concatenate((save_processed['tot_nr_mutate'], big_dic['tot_nr_mutate']))

    vec2 = np.concatenate((vec2, np.load(dir + filename[i + 2 * reading_number])))


print 'Processing Complete.'

# Saves data to Analyze in Matlab.
orfs = vec1
nr_orfs = vec2

uniq_orfs = np.unique(orfs)
uniq_nr_orfs = np.zeros(len(uniq_orfs))

for j, orf_name in enumerate(uniq_orfs):
    uniq_nr_orfs[j] = np.sum(nr_orfs[(orfs == orf_name)])

import scipy.io as sio

sio.savemat('uniq_nr_orfs.mat', {'uniqNrORFs':uniq_nr_orfs})
sio.savemat('uniq_orfs.mat', {'uniqORFs':uniq_orfs})

sio.savemat('growth.mat', {'growth':big_dic['growth']})
sio.savemat('growth_time.mat', {'growth_time':big_dic['growth_time']})
sio.savemat('nr_haploid_types.mat', {'nrHaploidTypes':big_dic['nr_haploid_types']})
sio.savemat('tot_nr_mutate.mat', {'tot_nr_mutate':big_dic['tot_nr_mutate']})



