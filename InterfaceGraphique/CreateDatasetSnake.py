import pygame
import pygame.draw
from pygame.locals import *
import random

nb_train = 20;
path="image/"
TailleEcran = 720
dicoClassImage = {}
dicoClassImage["Up"] = "ArrowUp.png"
dicoClassImage["Down"] = "ArrowDown.png"
dicoClassImage["Right"] = "ArrowRight.png"
dicoClassImage["Left"] = "ArrowLeft.png"
dicoClassImage["Nothing"] = "Nothing.png"

weakOrange=[255,178,102]
black = [0,0,0]
frame_train = 30
fps = 25

def drawScore(score,fenetre):
   font=pygame.font.Font(None,50)
   scoretext=font.render(str(score), 1,black)
   fenetre.blit(scoretext, (TailleEcran-100, TailleEcran-30))

def LaunchTraining(nb_train):
    pygame.init()
    keys = []
    clock = pygame.time.Clock()
    for key in dicoClassImage.keys():
        keys.append(str(key))
    print (keys)

    fenetre = pygame.display.set_mode((TailleEcran, TailleEcran))
    continuer = 1
    compteurTrain = 0
    compteurFrame = 0
    image = False
    imageToDisplay = ""

    while continuer:
        fenetre.fill(weakOrange)
        if image :
            if compteurFrame == 0:
                # nouvelle imageToDisplay
                imageToDisplay = random.choice(keys)
                compteurTrain += 1
                print(compteurTrain)
            imageClass = pygame.image.load(path+dicoClassImage[imageToDisplay]).convert_alpha()
            fenetre.blit(imageClass, (0,0))
            #attraper les données du casque
        drawScore(str(compteurTrain)+"/"+str(nb_train),fenetre)
        pygame.display.update()
        clock.tick(fps)
        compteurFrame +=1
        if compteurFrame == frame_train:
            image  = not image
            compteurFrame =0
        if compteurTrain == nb_train:
            continuer = 0

def main():
    LaunchTraining(nb_train);

if __name__=='__main__' : main()
