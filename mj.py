import math
import random
import numpy as np
import copy

# construit la liste "listeLienHorsRing", en associant chaque sommet hors ring au sommet du ring le plus proche
def attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing):
    for i in range(len(listeHorsRing)):
        m = math.inf
        s = -1
        for j in range(len(listeRing)):
            if m > Ca[listeHorsRing[i]][listeRing[j]]:
                m = Ca[listeHorsRing[i]][listeRing[j]]
                s = listeRing[j]
        listeLienHorsRing[i] = s

#genénère une solution aléatoire avec N sommets dans le ring
def solutionAleatoire(N):
    listeHorsRing = np.array(np.linspace(1, len(Ca), len(Ca)-1, endpoint=False), dtype='int').tolist()
    listeRing = [0]
    for i in range(N-2):
        n = random.randint(0, len(Ca) - i - 2)
        listeRing.append(listeHorsRing[n])
        listeHorsRing.remove(listeHorsRing[n])
    listeLienHorsRing = np.zeros(len(listeHorsRing))
    attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing)
    return listeRing, listeHorsRing, listeLienHorsRing

# évalue un scénario donné
def evalue(listeRing, listeHorsRing, listeLienHorsRing):
    c=0
    for i in range(len(listeRing)):
        c+=Cr[listeRing[i-1]][listeRing[i]]
    for j in range(len(listeHorsRing)):
        c+=Ca[int(listeHorsRing[j])][int(listeLienHorsRing[j])]
    return c

#nous voulons calculer la probabilité d'aller en chaque sommet de "listeRingRef"
def calculer_vecteur_proba(alpha, beta, listeRingRef, nonvisite, visibilite, ferom):
    P=[]
    denom=0
    for i in nonvisite:
        denom += ferom[listeRingRef.index(i)] ** alpha + visibilite[listeRingRef.index(i)] ** beta
    for elmt in range(len(listeRingRef)):
        if listeRingRef[elmt] in nonvisite:
            P+=[(ferom[elmt]**alpha+visibilite[elmt]**beta)/denom]
        else:
            P+=[0]
    return P

#donne la visibilité de tout les sommets lors que nous sommes au sommet n
def donneVisibilite(n,listeRingRef):
    visibilite=[]
    for elm in range(len(listeRingRef)):
        #Si la distance est egale à 0, on mets une visibilité égale à 0
        if Cr[elm][n]==0:
            visibilite +=[0]
        else:
            visibilite += [1 / Cr[elm][n]]
    return visibilite

#algorithmes pour une fourmi
def fourmi(alpha,beta, listeRingRef, ferom):
    #on choisie un sommet de départ
    n=random.randint(0,len(listeRingRef)-1)
    nonvisite=copy.deepcopy(listeRingRef)
    listeSommet=[listeRingRef[n]]
    nonvisite.remove(listeRingRef[n])
    i=0
    #tant la fourmi n'a pas visité tout les sommets
    while len(nonvisite)>0:
        i+=1
        visibilite=donneVisibilite(n,listeRingRef)
        P=calculer_vecteur_proba(alpha, beta, listeRingRef, nonvisite, visibilite, ferom[n])
        n=random.choices(listeRingRef,P,k=1)[0]
        nonvisite.remove(n)
        listeSommet+=[n]
        n=listeRingRef.index(n)
    return listeSommet

def deposeFerom(dferom, listeRing, listeRingRef, Q, cout):
    for i in range(len(listeRing)-1):
        dferom[listeRingRef.index(listeRing[i])][listeRingRef.index(listeRing[i+1])]+=Q/cout
    return dferom

def evaporerFerom(dferom, ferom, omega):
    for i in range(len(ferom)):
        for j in range(len(ferom)):
            ferom[i][j]=ferom[i][j]*(1-omega)+dferom[i][j]
    dferom=np.zeros((len(dferom), len(dferom))).tolist()
    return ferom,dferom

'''algorithme pour une colonie de fourmis
N: nombre de fois qu'on fait parourir le ring par les fourmis
alpha: poids donné aux féromones pour choisir le chemin pris par une fourmi
beta: poids donné à la visibilité pour choisir le chemin pris par une fourmi
omega: taux (entre 0 et 1) de féromone gardée à chaque parcour du graphe
Q: quantité (feromone*poids) de féromones déposées quand une fourmie passe sur un sommet'''
def colonieFourmi(nbParcour, nbFourmis, alpha,beta,Q,omega, mlisteRing, listeHorsRing, listeLienHorsRing):
    dferom = np.zeros((len(mlisteRing), len(mlisteRing))).tolist()
    ferom = np.zeros((len(mlisteRing), len(mlisteRing))).tolist()
    mcout=evalue(mlisteRing,listeHorsRing,listeLienHorsRing)
    listeRingRef=copy.deepcopy(mlisteRing)
    for k in range(nbParcour):
        for f in range(nbFourmis):
            listeRing=fourmi(alpha, beta, listeRingRef, ferom)
            cout=evalue(listeRing,listeHorsRing,listeLienHorsRing)
            dferom=deposeFerom(dferom,listeRing, listeRingRef, Q, cout)
            if cout<mcout:
                mcout=cout
                mlisteRing=copy.deepcopy(listeRing)
        ferom, dferom=evaporerFerom(dferom, ferom,omega)
    return mlisteRing, listeHorsRing, listeLienHorsRing, mcout

def recherche(nbParcour, nbIter, nbFourmis, alpha, beta, Q, omega):
    mcout = math.inf
    mlisteRing, mlisteHorsRing, mlisteLienHorsRing=[],[],[]
    coutSelonNbSommet=[]
    for i in range(len(Ca)):
        mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing=fourmiApertirDAleatoire(20,i, 20, alpha, beta, Q,
                                                                                      omega, coutSelonNbSommet, mcout,
                                                                                      mlisteRing, mlisteHorsRing, mlisteLienHorsRing)
    listeNbSommet = np.array(np.linspace(1, len(Ca)+1, len(Ca), endpoint=False), dtype='int').tolist()
    probaNbSommet=construitProbaNbSommet(coutSelonNbSommet)
    for j in range(nbIter):
        n = random.choices(listeNbSommet, probaNbSommet, k=1)[0]
        mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing = fourmiApertirDAleatoire(nbParcour, n, nbFourmis, alpha, beta, Q,
                                                                                        omega, coutSelonNbSommet, mcout,
                                                                                        mlisteRing, mlisteHorsRing, mlisteLienHorsRing)
    return mlisteRing, mlisteHorsRing, mlisteLienHorsRing, mcout

def construitProbaNbSommet(coutSelonNbSommet):
    probaNbSommet = []
    somme=sum(coutSelonNbSommet)
    for i in coutSelonNbSommet:
        probaNbSommet+=[i/somme]
    return probaNbSommet

#Dans tout le code nous travaillons avec des sommets dont le premier est le numéro 0, or dans l'énoncé le premier
#sommet est le 1. Nous décalons donc tout nos sommets afin de respecter l'énoncé.
def convertion(mlisteRing, listeHorsRing, listeLienHorsRing):
    mlisteRing = np.array(mlisteRing) + np.ones((1, len(mlisteRing)))
    listeHorsRing = np.array(listeHorsRing) + np.ones((1, len(listeHorsRing)))
    listeLienHorsRing = np.array(listeLienHorsRing) + np.ones((1, len(listeLienHorsRing)))
    return mlisteRing, listeHorsRing, listeLienHorsRing

def fourmiApertirDAleatoire(nbParcour,i, nbFourmis, alpha, beta, Q, omega, coutSelonNbSommet, mcout,mlisteRing, mlisteHorsRing, mlisteLienHorsRing):
    listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire(i)
    listeRing = colonieFourmi(nbParcour, nbFourmis, alpha, beta, Q, omega, listeRing, listeHorsRing, listeLienHorsRing)[0]
    cout = evalue(listeRing, listeHorsRing, listeLienHorsRing)
    coutSelonNbSommet += [cout]
    if cout < mcout:
        mcout = cout
        mlisteRing = copy.deepcopy(listeRing)
        mlisteHorsRing = copy.deepcopy(listeHorsRing)
        mlisteLienHorsRing = copy.deepcopy(listeLienHorsRing)
    return mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing

if __name__ == '__main__':
    Cr = []  # cout du ring
    Ca = []  # cout des liens vers ring

    #on récupère les données
    with open("Datasets/data4.txt") as f:
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
        mlisteRing, listeHorsRing, listeLienHorsRing, mcout = recherche(50, 50, 20, 1, 1, 1, 0.75)
        print(mcout, mlisteRing)