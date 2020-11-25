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

    def tabou(N,tailleMaxTabou):
        mListeRing = []
        listeTabou=[]
        listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
        meilleurCout=evalue(listeRing, listeHorsRing, listeLienHorsRing)
        for i in range(N):
            meilleurCoutLocal=math.inf
            mListeRingLocal = []
            for j in range(len(listeRing)):
                copListeRing = copy.deepcopy(listeRing)
                copListeRing = permuteRing(copListeRing, j)
                cout = evalue(copListeRing, listeHorsRing, listeLienHorsRing)
                if cout<meilleurCoutLocal and copListeRing not in listeTabou:
                    meilleurCoutLocal=cout
                    mListeRingLocal=copy.deepcopy(copListeRing)
                    if meilleurCoutLocal<meilleurCout:
                        meilleurCout=meilleurCoutLocal
                        mListeRing=copy.deepcopy(mListeRingLocal)
            listeTabou+=[mListeRing]
            if len(listeTabou)>tailleMaxTabou:
                listeTabou=listeTabou[1:]
        return meilleurCout, mListeRing, listeHorsRing,listeLienHorsRing


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
        for i in range(N):
            listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
            for j in range(len(listeRing)):
                copListeRing=copy.deepcopy(listeRing)
                copListeRing=permuteRing(copListeRing, j)
                cout=evalue(copListeRing, listeHorsRing, listeLienHorsRing)
                if cout<meilleurCout:
                    meilleurCout=cout
                    mListeRing=copy.deepcopy(copListeRing)
        return meilleurCout, mListeRing, listeHorsRing,listeLienHorsRing

    #nous sommes au sommet "sommet" et nous voulons calculer la probabilité d'aller en chaque sommet de "element"
    def calculer_vecteur_proba(alpha, beta, element, nonvisite, visibilite, ferom):
        P=[]
        denom=0
        for i in range(len(nonvisite)):
            denom += ferom[i] ** alpha + visibilite[i] ** beta
        for elmt in range(len(element)):
            if element[elmt] in nonvisite:
                #print(visibilite[elmt] ** beta)
                P+=[(ferom[elmt]**alpha+visibilite[elmt]**beta)/denom]
            else:
                P+=[0]
        return P

    def donneVisibilite(n,element):
        visibilite=[]
        for elm in range(len(element)):
            if Cr[elm][n]==0:
                visibilite +=[0]
            else:
                visibilite += [1 / Cr[elm][n]]
        return visibilite

    def fourmi(alpha,beta,listeRing):
        n=random.randint(0,len(listeRing)-1)
        element=copy.deepcopy(listeRing)
        nonvisite=copy.deepcopy(listeRing)
        ferom=np.zeros((len(listeRing),len(listeRing))).tolist()
        listeSommet=[listeRing[n]]
        nonvisite.remove(listeRing[n])
        i=0
        while len(nonvisite)>0:
            i+=1
            visibilite=donneVisibilite(n,element)
            P=calculer_vecteur_proba(alpha, beta, element, nonvisite, visibilite, ferom[n])
            n=random.choices(element,P,k=1)[0]
            nonvisite.remove(n)
            listeSommet+=[n]
            n=element.index(n)
        return listeSommet


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
        listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
        mListeRing=fourmi(0.5,0.5,listeRing)
        print(mListeRing)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
