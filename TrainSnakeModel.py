#model.save(filepath)
import tensorflow as tf
from tensorflow import keras
import numpy as np

nb_r = 20
input_shape = (8,nb_r)

modelSimple = keras.models.Sequential([
    keras.layers.Flatten(input_shape=input_shape),
    keras.layers.Dense(128,activation=tf.nn.relu),
    keras.layers.Dense(5,activation=tf.nn.softmax)
])

modelSimple.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

modelConv = keras.models.Sequential([
    keras.layers.Conv2D(28,kernel_size = (3,3),input_shape=input_shape),
    keras.layers.MaxPooling2D(pool_size=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128,tf.nn.relu),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(5,activation=tf.nn.softmax)
])

modelConv.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

#fit
#test
#save
