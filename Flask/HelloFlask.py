from flask import Flask
from flask import request
from flask_cors import CORS
import sys
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
app = Flask(__name__)
CORS(app)

# model global
model = tf.keras.models.load_model("../test/LstmTest2/save/model5-50.hdf5",custom_objects=None,compile=True)
graph = tf.get_default_graph()
# with tf default graph  ,, graph defaut pour pas le multiplier par thread # par defaut normalement

data =[]
tree = etree.parse("../test/datasetSMS/dataSMS3.xml")
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
print('Vocabulary Size: %d' % vocab_size, file=sys.stdout)
# create line-based sequences
sequences = list()
for i in range(len(data)):
    for line in data[i].split('\n'):
    	encoded = tokenizer.texts_to_sequences([line])[0]
    	for i in range(1, len(encoded)):
    		sequence = encoded[:i+1]
    		sequences.append(sequence)
print('Total Sequences: %d' % len(sequences), file=sys.stdout)
# pad input sequences
max_length = max([len(seq) for seq in sequences])
sequences = pad_sequences(sequences, maxlen=max_length, padding='pre')
print('Max Sequence Length: %d' % max_length, file=sys.stdout)

@app.route("/")
def hello():
    print('Hello', file=sys.stdout)
    return  "Hello World!"

@app.route("/api",methods=['POST', 'GET'])
def parse_request():
    #global graph pour appeler
    print('une requete', file=sys.stdout)
    data = request.args
    print(str(data["var"]), file=sys.stdout)
    reponse = generate_T9(model,tokenizer, max_length-1,data["var"])
    return  str(reponse)

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

def generate_T9(model, tokenizer, max_length, seed_text):
    in_text = seed_text
    encoded = tokenizer.texts_to_sequences([in_text])[0]
    encoded = pad_sequences([encoded], maxlen=max_length, padding='pre')
    yhat= ""
    global graph
    with graph.as_default():
        yhat = model.predict(encoded, verbose=0)
    maxs = [-1,-1,-1,-1]
    for i in range(len(yhat[0])):
        maxs = addmaxs(maxs,i,yhat)
    # map predicted word index to word
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
    print("text : "+in_text, file=sys.stdout)
    return in_text
