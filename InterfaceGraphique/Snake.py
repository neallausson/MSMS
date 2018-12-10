# -*- coding: utf-8 -*-
import pygame
import pygame.draw
from pygame.locals import *
import numpy as np

class Snake :

    def __init__(self,lenght,taille,split,ecran,couleur,square):
        self.corps = []
        self.taille = taille
        self.split = split
        self.ecran = ecran
        self.couleur = couleur
        self.square = square
        self.factor = 0.8
        for i in range(lenght):
            if square:
                body = pygame.draw.rect(ecran,couleur , (taille/split, (taille/split)+i*(taille/split), taille/split, taille/split))
            else:
                body = pygame.draw.circle(ecran,couleur , (int(taille/split)*2, int((taille/split)+i*(taille/split))), int(taille/(split*2)))
            self.corps.append(body)

    def grow(self):
        self.corps.append(self.corps[-1].copy())

    def move(self,direction):
        toMove = self.corps.pop(len(self.corps)-1)
        if direction == "up":
            toMove.move_ip((self.corps[0].x-toMove.x),(self.corps[0].y-toMove.y)-self.taille/self.split)
        if direction == "down":
            toMove.move_ip((self.corps[0].x-toMove.x),(self.corps[0].y-toMove.y)+self.taille/self.split)
        if direction == "left":
            toMove.move_ip((self.corps[0].x-toMove.x)-self.taille/self.split,(self.corps[0].y-toMove.y))
        if direction == "right":
            toMove.move_ip((self.corps[0].x-toMove.x)+self.taille/self.split,(self.corps[0].y-toMove.y))
        self.corps.insert(0,toMove)


    def draw(self,taille,split):
        for i in range(len(self.corps)):
            if self.square:
                pygame.draw.rect(self.ecran, self.couleur, self.corps[i])
            else:
                pygame.draw.circle(self.ecran, self.couleur, (self.corps[i].x, self.corps[i].y), int((self.taille / (self.split*2)) *max((np.exp(-i*0.02)),0.1)))
        eye = pygame.transform.scale(pygame.image.load("image/eye.png").convert_alpha(),(np.array(self.corps[0].size)*self.factor).astype(np.uint8))
        if self.square:
            self.ecran.blit(eye, (self.corps[0].x+(self.corps[0].width//2)*(1-self.factor),self.corps[0].y+(self.corps[0].height//2)*(1-self.factor)))
        else:
            self.ecran.blit(eye,(self.corps[0].x-self.corps[0].width*(self.factor)//2,self.corps[0].y-self.corps[0].width*(self.factor)//2))
