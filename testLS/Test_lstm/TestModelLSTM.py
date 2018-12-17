import collections
import os
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Activation, Embedding, Dropout, TimeDistributed
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.utils import to_categorical
from tensorflow.python.keras.callbacks import ModelCheckpoint
from KerasBatchGenerator import KerasBatchGenerator
from AttentionLayer import AttentionLayer
from AttentionDecoder import AttentionDecoder

data_path = "simple-examples/data/"
use_dropout=True
# parser = argparse.ArgumentParser()
# parser.add_argument('run_opt', type=int, default=1, help='An integer: 1 to train, 2 to test')
# parser.add_argument('--data_path', type=str, default=data_path, help='The full path of the training data')
# args = parser.parse_args()
# if args.data_path:
#     data_path = args.data_path

num_steps=30

batch_size=20

hidden_size=500

num_epochs = 50

def read_words(filename):
    with tf.gfile.GFile(filename, "rb") as f:
        return f.read().decode("utf-8").replace("\n", "<eos>").split()
        #return bytes(f.read(),"utf-8").replace("\n", "<eos>").split()

def file_to_word_ids(filename, word_to_id):
    data = read_words(filename)
    return [word_to_id[word] for word in data if word in word_to_id]

def build_vocab(filename):
    data = read_words(filename)

    counter = collections.Counter(data)
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    words, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id

def load_data():
    # get the data paths
    train_path = os.path.join(data_path, "ptb.train.txt")
    valid_path = os.path.join(data_path, "ptb.valid.txt")
    test_path = os.path.join(data_path, "ptb.test.txt")

    # build the complete vocabulary, then convert text data to list of integers
    word_to_id = build_vocab(train_path)
    train_data = file_to_word_ids(train_path, word_to_id)
    valid_data = file_to_word_ids(valid_path, word_to_id)
    test_data = file_to_word_ids(test_path, word_to_id)
    vocabulary = len(word_to_id)
    reversed_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))

    # print(train_data[:5])
    # print(word_to_id)
    # print(vocabulary)
    # print(" ".join([reversed_dictionary[x] for x in train_data[:10]]))
    return train_data, valid_data, test_data, vocabulary, reversed_dictionary

def train():
    train_data, valid_data, test_data, vocabulary, reversed_dictionary = load_data()

    train_data_generator = KerasBatchGenerator(train_data, num_steps, batch_size, vocabulary,skip_step=num_steps)
    valid_data_generator = KerasBatchGenerator(valid_data, num_steps, batch_size, vocabulary,skip_step=num_steps)

    model = Sequential()
    model.add(Embedding(vocabulary, hidden_size, input_length=num_steps))
    model.add(LSTM(hidden_size, return_sequences=True))
    # if use_dropout:
    #     model.add(Dropout(0.5))
    model.add(LSTM(hidden_size, return_sequences=True))
    model.add(AttentionDecoder(150,50))
    if use_dropout:
        model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(vocabulary)))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1)

    tbCallBack = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
    model.fit_generator(train_data_generator.generate(), len(train_data)//(batch_size*num_steps), num_epochs,
                            validation_data=valid_data_generator.generate(),
                            validation_steps=len(valid_data)//(batch_size*num_steps), callbacks=[checkpointer,tbCallBack])

    model.save(data_path + "final_model.hdf5")

def test():
    train_data, valid_data, test_data, vocabulary, reversed_dictionary = load_data()
    model = load_model(data_path + "model-09.hdf5")
    dummy_iters = 40
    example_training_generator = KerasBatchGenerator(train_data, num_steps, 1, vocabulary,
                                                         skip_step=1)
    print("Training data:")
    for i in range(dummy_iters):
        dummy = next(example_training_generator.generate())
    num_predict = 15
    true_print_out = "Actual words: "
    pred_print_out = "Predicted words: "
    for i in range(num_predict):
        data = next(example_training_generator.generate())
        prediction = model.predict(data[0])
        predict_word = np.argmax(prediction[:, num_steps-1, :])
        true_print_out += reversed_dictionary[train_data[num_steps + dummy_iters + i]] + " "
        pred_print_out += reversed_dictionary[predict_word] + " "
    print(true_print_out)
    print(pred_print_out)

if __name__=='__main__' :
    train()
    #test()
