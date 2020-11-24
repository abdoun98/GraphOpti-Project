import math
import random
import numpy as np
import copy

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    def permuteRing(listeRing, i):
        listeRing[i], listeRing[i - 1] = listeRing[i - 1], listeRing[i]
        return listeRing

    def entreRing(listeRing, listeHorsRing, listeLienHorsRing, i, j):
        listeRing = listeRing[:j] + [listeHorsRing[i]] + listeRing[j:]
        listeHorsRing.remove(listeHorsRing[i])
        listeLienHorsRing.remove(listeLienHorsRing[i])
        attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing)


    def attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing):
        for i in range(len(listeHorsRing)):
            m = math.inf
            s = -1
            for j in range(len(listeRing)):
                if m > Ca[listeHorsRing[i]][listeRing[j]]:
                    m = Ca[listeHorsRing[i]][listeRing[j]]
                    s = listeRing[j]
            listeLienHorsRing[i] = s


    def solutionAleatoire():
        listeHorsRing = np.array(np.linspace(0, len(Ca), len(Ca), endpoint=False), dtype='int').tolist()
        N = random.randint(0, len(Ca))
        listeRing = []
        for i in range(N):
            n = random.randint(0, len(Ca) - i -1)
            listeRing.append(listeHorsRing[n])
            listeHorsRing.remove(listeHorsRing[n])
        listeLienHorsRing = np.zeros(len(listeHorsRing))
        attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing)
        return listeRing, listeHorsRing, listeLienHorsRing

    def evalue(listeRing, listeHorsRing, listeLienHorsRing):
        c=0
        for i in range(len(listeRing)):
            c+=Cr[listeRing[i-1]][listeRing[i]]
        for j in range(len(listeHorsRing)):
            c+=Ca[int(listeHorsRing[j])][int(listeLienHorsRing[j])]
        return c

    def voisinageVariable(N):
        meilleurCout=math.inf
        mListeRing=[]
        mListeHorsRing=[]
        mListeLienHorsRing=[]
        for i in range(N):
            listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
            for j in range(len(listeRing)):
                copListeRing=copy.deepcopy(listeRing)
                copListeRing=permuteRing(copListeRing, j)
                cout=evalue(copListeRing, listeHorsRing, listeLienHorsRing)
                if cout<meilleurCout:
                    meilleurCout=cout
                    mListeRing=copy.deepcopy(copListeRing)
                    mListeHorsRing=copy.deepcopy(listeHorsRing)
                    mListeLienHorsRing=copy.deepcopy(listeLienHorsRing)
        return meilleurCout, mListeRing, mListeHorsRing,mListeLienHorsRing

    Cr = []  # cout du ring
    Ca = []  # cout des liens vers ring

    with open("Datasets/data1.txt") as f:
        data = f.readline()
        data = data.split()
        data = list(map(int, data))
        N = data[0]  # Nombre de sommets du problème
        print(N)

        for i in range(N):
            sommet = f.readline()
            sommet = sommet.split()
            sommet = list(map(int, sommet))
            Cr.append(sommet)

        for j in range(N):
            sommet2 = f.readline()
            sommet2 = sommet2.split()
            sommet2 = list(map(int, sommet2))
            Ca.append(sommet2)

        print(Ca[1][2])
        print("fin d'extraction des donnees")
        meilleurCout, mListeRing, mListeHorsRing,mListeLienHorsRing = voisinageVariable(10000)
        print(meilleurCout)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
