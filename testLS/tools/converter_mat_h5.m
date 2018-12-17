path = '/home/neallausson/Documents/Innovation/Dataset/IIIa/l1b_mat/l1b.mat'
nom_fichier = 'l1b.h5'
dataset =load(path)
dataset.HDR

h5create(nom_fichier,'/TRIG',[240 1])
h5write(nom_fichier, '/TRIG', dataset.HDR.TRIG)
h5create(nom_fichier,'/s',[633430 60])
h5write(nom_fichier, '/s', dataset.s)
h5create(nom_fichier,'/Classlabel',[240 1])
h5write(nom_fichier, '/Classlabel', dataset.HDR.Classlabel)