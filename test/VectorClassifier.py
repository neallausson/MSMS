import tensorflow as tf
import numpy as np
import os.path
import h5py as h5
from tensorflow import keras
#import tensorflow.keras as keras

path ='Dataset/IIIa/k3b_mat/k3b.h5'
path2 ='Dataset/IIIa/k6b_mat/k6b.h5'
paths = ['Dataset/IIIa/k3b_mat/k3b.h5','Dataset/IIIa/k6b_mat/k6b.h5','Dataset/IIIa/l1b_mat/l1b.h5']
#path ='Dataset/IIIa/l1b_mat/l1b.h5'

s = []
trig = []
classlabel = []

for value in paths:
    print("le fichier existe : " + str(os.path.isfile(value)))
    print("le fichier peut être lu : " + str(os.access(value, os.R_OK)))
    f = h5.File(value,'r')
    print("List group : "+ str(list(f.keys())))
    s += list(f['s'][0])
    #print (s)
    trig += list(f['TRIG'][0])
    #print(type(f["Classlabel"][0]))
    classlabel += list(f["Classlabel"][0])

#print (s.shape)
#print (trig.shape)
#print (classlabel.shape)
#trouve min e max
np.nan_to_num(s,copy=False)
min_val = 0;
max_val = 0;
for value in s:
    if min_val is 0 or value < min_val :
        min_val = value
    if max_val is 0 or value > max_val:
        max_val = value
print(max_val)
print(min_val)

#normaliser s entre 0 et 1
for i in range(0,len(s)):
    s[i] = (s[i] - min_val)/(max_val-min_val)
print("données normalisée")
#print(s)

#séparer les données
data = []
ClassLabelClear = []
for i in range(0,len(trig)-1):
    #if str(classlabel[i]) is "1.0" or str(classlabel[i]) is "2.0" or str(classlabel[i]) is "3.0" or str(classlabel[i]) is "4.0":
    np.nan_to_num(classlabel,copy = False)
    #print (classlabel[i])
    #print (type(classlabel[i]))
    if not np.isnan(classlabel[i]) :
        if trig[i+1] - trig[i] == 2560 or trig[i+1] - trig[i] == 2561:
                ClassLabelClear.append(int(classlabel[i]))
                data.append(s[int(trig[i]):int(trig[i]+2560)])
print ("données clear")
print (ClassLabelClear)
print (len(ClassLabelClear))
print (len(data[0]))
#print (data[0])

class_names = ['Class 1','Class 2','Class 3','Class 4']

model = keras.models.Sequential([
    keras.layers.Dense(4096,input_shape=(2560,), activation=tf.nn.tanh),
    keras.layers.Dense(4096, activation=tf.nn.tanh),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
data = np.nan_to_num(data,copy=False)
train_images = np.array(data[0:int(len(data)/10)*9],dtype = np.float32)
train_labels = np.array(ClassLabelClear[0:int(len(data)/10)*9],dtype = np.float32).reshape((-1,1))
print(train_images[0])


print(type(train_images))
print(train_images.shape)
print(type(train_images[0]))
print(train_images[0].shape)
#print(train_labels)
print(type(train_labels))
print(train_labels.shape)
model.fit(train_images, train_labels, epochs=40)

test_images = np.array(data[len(train_images):len(data)],dtype = np.float32)
test_labels = np.array(ClassLabelClear[len(train_images):len(data)],dtype = np.float32).reshape((-1,1))
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)
