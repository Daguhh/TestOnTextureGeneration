#!/usr/bin/python3

import numpy as np
from numpy.random import choice

import sys
from PIL import Image


'''
a : proba a proba b proba c

arbre
maison
champs
'''

class Obj:
    def __init__(self, indice, dessin, size):
        self.indice = indice
        self.dessin = Image.open(dessin)
        self.size = size


class Markov:

    def __init__(self):

        self.P = np.loadtxt("Proba.csv")
        arbre = Obj(0,"sapin.png", 25)
        maison = Obj(1,"house_wood.png", 100)
        champ = Obj(2,"champs2.png", 100)

        self.liste_obj = [arbre, maison, champ]
        self.last_elt = 0

    def gen(self, size, heightmap):

        new_im = Image.new('RGBA', (size, 400))
        chaine = [self.liste_obj[self.last_elt]]
        print("================================")
        print(heightmap[0])
        new_im.paste(chaine[0].dessin, (0, heightmap[0]))
        chaine_size = chaine[0].size
        while chaine_size <  size-100:
        #for i in range(100):
            last_elt = chaine[-1]
            Pelt = self.P[last_elt.indice,]
            new_obj = choice(self.liste_obj, p=Pelt)
            chaine += [new_obj]
            chaine_size += new_obj.size
        offset = chaine[0].size
        for elt in chaine :
            height = heightmap[offset]
            new_im.alpha_composite(elt.dessin, (offset,height))
            offset+=elt.size
            #new_im.paste(elt.dessin, (i*15,0))

        new_im.save('test4.png')
        self.last_elt = chaine[-1].indice
        return new_im

if __name__ == '__main__':

    markov = Markov()
    heightmap = (20*np.sin(np.arange(500)*np.pi/100)).astype(int)+20
    new_im = Image.new('RGBA', (400*4,400))
    #np.random.randint(0,15,210)
    last_elt = 0
    offset = 0
    for i in range(4):
        im = markov.gen(400, heightmap)
        new_im.alpha_composite(im, (offset,0))
        print(im.size)
        offset += im.size[0]

    new_im.save("balbla.png")
#a=np.array([0,1,2,3])
#p=np.array([0.05,0.04,0.01,0.9])

#for i in range(20):
#    print(choice(a,p=p))
