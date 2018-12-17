from numpy import array
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.utils import to_categorical
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Embedding
from tensorflow.python.keras.callbacks import ModelCheckpoint
from lxml import etree


data_path ="save"
# generate a sequence from a language model
def generate_seq(model, tokenizer, max_length, seed_text, n_words):
	in_text = seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		# pre-pad sequences to a fixed length
		encoded = pad_sequences([encoded], maxlen=max_length, padding='pre')
		# predict probabilities for each word
		yhat = model.predict_classes(encoded, verbose=0)
		# map predicted word index to word
		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break
		# append to input
		in_text += ' ' + out_word
	return in_text

def addmaxs(maxs,index,yhat):
	for i in range(len(maxs)):
		if maxs[i]==-1:
			maxs[i]=index
			break
		if yhat[0][index]>yhat[0][maxs[i]]:
			for j in range(i,len(maxs)-2):
				maxs[len(maxs)-j-1]=maxs[len(maxs)-j-2]
			maxs[i]=index
			break
	return maxs

def generate_T9(model, tokenizer, max_length, seed_text, n_words):
	in_text = seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		# pre-pad sequences to a fixed length
		encoded = pad_sequences([encoded], maxlen=max_length, padding='pre')
		# predict probabilities for each word
		yhat = model.predict(encoded, verbose=0)
		maxs = [-1,-1,-1,-1]
		for i in range(len(yhat[0])):
			maxs = addmaxs(maxs,i,yhat)

		# map predicted word index to word
		print(maxs)
		for i in range(len(maxs)):
			out_word = ''
			for word, index in tokenizer.word_index.items():
				maxIndex = maxs[i]
				#print(index)
				if index == maxs[i]:
					out_word = str(i)+ " : " +word+'\n'
					print(out_word)
					break
			# append to input
		chooseWord = input("choisie le mot suivant :")
		in_text +=' '+ chooseWord
		print("text : "+in_text)
	return in_text
# source text
# data = """ Jack and Jill went up the hill\n
# 		To fetch a pail of water\n
# 		Jack fell down and broke his crown\n
# 		And Jill came tumbling after\n """
data =[]
tree = etree.parse("../datasetSMS/dataSMS3.xml")
compteur = 0
for sms in tree.xpath("/corpus/sms/cont"):
    compteur +=1
    if type(sms.text) is str:
        data.append(sms.text)
print (compteur)
# prepare the tokenizer on the source text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)
# determine the vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print('Vocabulary Size: %d' % vocab_size)
# create line-based sequences
sequences = list()
for i in range(len(data)):
    for line in data[i].split('\n'):
    	encoded = tokenizer.texts_to_sequences([line])[0]
    	for i in range(1, len(encoded)):
    		sequence = encoded[:i+1]
    		sequences.append(sequence)
print('Total Sequences: %d' % len(sequences))
# pad input sequences
max_length = max([len(seq) for seq in sequences])
sequences = pad_sequences(sequences, maxlen=max_length, padding='pre')
print('Max Sequence Length: %d' % max_length)
# split into input and output elements
sequences = array(sequences)
X, y = sequences[:,:-1],sequences[:,-1]
y = to_categorical(y, num_classes=vocab_size)
# define model
# model = Sequential()
# model.add(Embedding(vocab_size, 10, input_length=max_length-1))
# model.add(LSTM(50))
# model.add(Dense(vocab_size, activation='softmax'))
# print(model.summary())
# compile network
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model = tf.keras.models.load_model("save/model5-50.hdf5",custom_objects=None,compile=True)

# checkpointer = ModelCheckpoint(filepath=data_path + '/model5-{epoch:02d}.hdf5', verbose=1)
# tbCallBack = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
# fit network
# model.fit(X, y, epochs=100, verbose=1,callbacks=[checkpointer,tbCallBack])
# evaluate model
#print(generate_seq(model, tokenizer, max_length-1, '', 20))
print(generate_T9(model, tokenizer, max_length-1, '', 3))
# print(generate_seq(model, tokenizer, max_length-1, 'je', 5))
print(generate_T9(model, tokenizer, max_length-1, 'je', 5))
#print(generate_seq(model, tokenizer, max_length-1, 'nous', 20))
#print(generate_T9(model, tokenizer, max_length-1, 'nous', 20))
