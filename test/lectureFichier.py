import tensorflow as tf
import numpy as np
import os
import h5py as h5
from tensorflow import keras
import random
from generator import Generator

# def generator(features, labels, batch_size):
#  # Create empty arrays to contain batch of features and labels#
#   while True:
#       batch_features = []
#       batch_labels = []
#       for i in range(batch_size):
#          print (str(i))
#          # choose random index in features
#          index= random.randint(0,len(features))-1
#          batch_features.append(np.load(DataPath[index]))
#          print(np.load(DataPath[index]).shape); exit()
#          batch_labels.append(DataLabel[index])
#       yield batch_features, batch_labels

#16449
batch_size = 4
taille_Dataset = 0
DataPath = []
DataLabel = []
path = "Dataset/eeg_full_clear"

list_dir = os.listdir(path)
print(list_dir)

compteurDir = 0;
for directory in list_dir:
    compteurDir += 1 ;
    print("DIRECTORY"+str(directory) + " "+ str(compteurDir)+"/"+str(len(list_dir)))
    classLabel=""
    compteurFic = 0;
    list_file = os.listdir(path+"/"+directory)
    for oneFile in list_file:
        compteurFic += 1 ;

        print("FICHIER "+str(oneFile) +" "+ str(compteurFic)+"/"+str(len(list_file)))
        DataPath.append(path+"/"+directory+"/"+oneFile)
        if oneFile[3]=="c":
            DataLabel.append(0);
        else:
            DataLabel.append(1);

dataloader=Generator(DataPath,DataLabel,batch_size)
#taille_Dataset = int(len(Data)/0.9)
model = keras.models.Sequential()
model.add(keras.layers.Embedding(len(dataloader), 5000))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(1000, activation=tf.nn.relu))
model.add(keras.layers.Dense(500, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])



history = model.fit_generator(dataloader, steps_per_epoch=5, epochs=20)

# results = model.evaluate(Data[taille_Dataset:], DataLabel[taille_Dataset:])
#
# print(results)
#
# history_dict = history.history
# print(history_dict.keys())
#
# #dict_keys(['acc', 'val_loss', 'loss', 'val_acc'])
#
# import matplotlib.pyplot as plt
#
# acc = history.history['acc']
# val_acc = history.history['val_acc']
# loss = history.history['loss']
# val_loss = history.history['val_loss']
#
# epochs = range(1, len(acc) + 1)
#
# # "bo" is for "blue dot"
# plt.plot(epochs, loss, 'bo', label='Training loss')
# # b is for "solid blue line"
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
#
# plt.show()
#
# plt.clf()   # clear figure
# acc_values = history_dict['acc']
# val_acc_values = history_dict['val_acc']
#
# plt.plot(epochs, acc, 'bo', label='Training acc')
# plt.plot(epochs, val_acc, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()
#
# plt.show()

print("FIN")
