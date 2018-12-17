import numpy as np
import scipy.io
import os.path
import h5py as h5
import tables

path ='Dataset/IIIa/k3b_mat/k3b.h5'

print(os.path.isfile(path))
print(os.access(path, os.R_OK))
#f2 = tables.openFile('Dataset/IIIa/k3b_mat/k3b.mat')
#f = scipy.io.loadmat(path)
f = h5.File(path,'r')
#print(f)
print(list(f.keys()))
data = f['TRIG'] # Get a certain dataset
print(data[0])
"""min_val = 0;
max_val = 0;
for value in data[0]:
    if min_val is 0 or value<min_val :
        min_val = value
    if max_val is 0 or value > max_val:
        max_val = value
print(max_val)
print(min_val)"""
#data = np.array(data)
#for i in range(1,len(data[0])):
#    print(str(data[0][i]-data[0][i-1]))
print ("OK")
