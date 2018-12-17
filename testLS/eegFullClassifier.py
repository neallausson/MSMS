import tensorflow as tf
import numpy as np
import os
import h5py as h5
from tensorflow import keras

#reecrire le dataset
#class dataset keras dataset generator
#lstm temps aleatoire  image cree Dataset
#t9 juste changer l'impact des classes
#t9 voir gregor
#strore
path = "Dataset/eeg_full"
path_save = "Dataset/eeg_full_clear"

#faire des batch 32

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
        tabOneDir = []
        fichier = open(path+"/"+directory+"/"+oneFile, "r")
        textBrut = fichier.read()
        fichier.close()
        lignes = textBrut.split('\n')
        classLabel = lignes[0][5]
        for i in range(4,len(lignes)):
            ligne_split = lignes[i].split(' ')
            # print(ligne_split)
            if ligne_split[0] == "#":
                i += 1
                tab=[]
                ligne_split = lignes[i].split(' ')
                while ligne_split[0] != "#" :
                    ligne_split = lignes[i].split(' ')
                    if len(ligne_split)==4 :
                        tab.append(ligne_split[3])
                        i += 1
                    else:
                        break;
            tabOneDir.append(np.array(tab))
            i -= 1
            #print(tab)
            #print(len(tab))
        to_save = np.array(tabOneDir)
        if not os.path.exists(path_save+"/"+directory):
            os.makedirs(path_save+"/"+directory)
        np.save(path_save+"/"+directory+"/"+oneFile+"_data",np.array(to_save))
print ("all is ok")
