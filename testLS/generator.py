# -*- coding:utf-8 -*-
import tensorflow as tf
from tensorflow import keras
import numpy as np
import math
import random

class Generator(keras.utils.Sequence):

    def __init__(self,paths,labels,batch_size):
        self.paths = paths
        self.labels = labels
        self.batch_size=batch_size

    def __len__(self):
        return math.ceil(len(self.paths)/self.batch_size)

    def __getitem__(self,id):
        batch_features = np.zeros((self.batch_size,16449))

        batch_labels = np.zeros(self.batch_size)
        print(str(self.batch_size))
        for i in range(self.batch_size):
           # choose random index in features
           index= random.randint(0,len(self.paths))-1
           data = np.load(self.paths[index])
           print(str(i))
           print(str(type(data)))
           print(str(data.shape))
           batch_features[i] = data
           batch_labels[i] = self.labels[index]
        print(str(type(batch_features))+" "+str(type(batch_labels)))
        return batch_features, batch_labels
