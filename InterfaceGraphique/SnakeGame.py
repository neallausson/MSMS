import pygame
import pygame.draw
from pygame.locals import *
from Snake import Snake
import random

def SpawnApple(taille,split,snake,ecran,square):
    case = []
    for i in range(split):
        for j in range(split):
            case.append([i,j])
    # full case
    # print("full case "+str(len(case)))
    # print(str(case))
    caseb = []
    for duo in case :
        # print(str(duo))
        # if duo[0]==0 or duo[1]==0 or duo[0]==split-1 or duo[1]==split-1:
        #     print("remove")
        # else:
        #     caseb.append(duo)
        caseb.append(duo)
    #case sans les bords
    # print("without border case "+str(len(caseb)))
    # print(str(caseb))
    for rect in snake.corps :
        try :
            if square:
                caseb.remove([rect.x/(taille/split),rect.y/(taille/split)])
            else:
                caseb.remove([(rect.x-int(taille/(split*2)))/(taille/split),(rect.y-int(taille/(split*2)))/(taille/split)])
        except ValueError :
            continue
    #case sans bord + Snake
    # print("without border snake case "+str(len(caseb)))
    # print(str(caseb))
    if len(caseb)==0:
        print("WIN")
        return None
    caseApple = random.choice(caseb)
    print("APPLE "+ str(caseApple))

    # position = Apple.get_rect()
    # position.x = caseApple[0]*(taille//split)
    # position.y = caseApple[1]*(taille//split)
    # Apple =Apple.get_rect().move(Apple,position)
    #Apple = pygame.draw.rect(ecran,(255,0,0) ,(caseApple[0]*(taille/split),caseApple[1]*(taille/split), taille/split, taille/split))
    return caseApple

def CheckDeath(snake,taille,split):
    if snake.corps[0].x<0 or snake.corps[0].y<0 or snake.corps[0].x>taille-split or snake.corps[0].y>taille-split:
        print("hors limite")
        return True
    for i in range(1,len(snake.corps)):
        if snake.corps[0].x == snake.corps[i].x and snake.corps[0].y == snake.corps[i].y:
            print("mange sa queue")
            return True
    return False

def CheckApple(snake,apple,taille ,split,square):
    if square:
        if (apple[0]*(taille//split) == snake.corps[0].x and apple[1]*(taille//split) == snake.corps[0].y ) :
            snake.grow()
            return None
    else:
        if apple[0]*(taille//split) == snake.corps[0].x-int(taille/(split*2)) and apple[1]*(taille//split) == snake.corps[0].y-int(taille/(split*2)) :
            print("grow")
            snake.grow()
            return None
    return apple

def main() :
    #Initialisation de la bibliothèque Pygame
    pygame.init()
    clock = pygame.time.Clock()
    TailleEcran = 1000
    split = 10
    square = False

    sable = [224,205,169]
    vert = [0, 150, 0]
    #Création de la fenêtre
    fenetre = pygame.display.set_mode((TailleEcran, TailleEcran))


    #Variable qui continue la boucle si = 1, stoppe si = 0
    continuer = 1
    snake = Snake(2,TailleEcran,split,fenetre,vert,square)
    caseApple = SpawnApple(TailleEcran,split,snake,fenetre,square)
    #Boucle infinie
    fenetre.fill(sable)
    while continuer:
        fenetre.fill(sable)
        snake.draw(TailleEcran,split)
        #pygame.draw.rect(fenetre,(255,0,0), apple)
        #fenetre.image.draw(apple)
        Apple = pygame.transform.scale(pygame.image.load("image/apple.png").convert_alpha(),(TailleEcran//split,TailleEcran//split))
        fenetre.blit(Apple,[caseApple[0]*(TailleEcran/split),caseApple[1]*(TailleEcran/split)])
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
               snake.move("left")
            if key[pygame.K_RIGHT]:
               snake.move("right")
            if key[pygame.K_UP]:
               snake.move("up")
            if key[pygame.K_DOWN]:
               snake.move("down")
        if CheckDeath(snake,TailleEcran,split):
            continuer = 0
        caseApple = CheckApple(snake,caseApple,TailleEcran,split,square)
        if caseApple == None:
            caseApple = SpawnApple(TailleEcran,split,snake,fenetre,square)
        if caseApple == None:
            continuer= 0
        pygame.display.update()
        clock.tick(20)


if __name__=='__main__' : main()
