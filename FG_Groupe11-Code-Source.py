#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 20:19:21 2020

@author: francois
"""

################ Graphes et optimisation combinatoire ################

####################### CHALLENGE 2020-2021 ##########################
#
# MEMBRES (GROUPE 11) :
#   - Maël Jaouen
#   - Corentin Sculteur
#   - François Gérémie
#   - Abderrahmen Abdoun
#
############################## SECTIONS ##############################
#
#   - Section 1 : IMPORTATIONS DES LIBRAIRIRES
#   - Section 2 : LECTURE & ECRITURE DES FICHIERS
#   - Section 3 : RECHERCHE TABOU
#   - Section 4 : VOISINAGE VARIABLE
#   - Section 5 : RECUIT SIMULE
#   - Section 6 : ALGORITHME COLONIE DE FOURMIS
#   - Section 7 : ALGORITHME EVOLUTIONNAIRE
#   - Section 8 : MAIN


######################################################################
#                   IMPORTATION DES LIBRAIRIES                      #
######################################################################

import random
import numpy as np
import math
import copy
import time

######################################################################
#                   LECTURE & ECRITURE DES FICHIERS                  #
######################################################################

# LECTURE
def dataExtract(file):
    Cr = []  # cout du ring
    Ca = []  # cout des liens vers ring
    with open("Datasets/" + file + ".txt") as f:
        data = f.readline()
        data = data.split()
        data = list(map(int, data))
        N = data[0]  # Nombre de sommets du problème
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
        print("fin d'extraction des donnees")
    return N, Ca, Cr


# ECRITURE
def writeOutput(file, listRing, listHorsRing, cout):
    with open("Outputs/output-" + file + ".txt", "w") as f:
        f.write("RING {}\n".format(len(listRing)))
        for elem in listRing:
            f.write("{} ".format(elem))
        f.write("\nSTAR")
        for elem in listHorsRing:
            f.write("\n{} {}".format(elem[0], elem[1]))
        f.write("\nCOST {}".format(cout))


######################################################################
#                          RECHERCHE TABOU                           #
######################################################################
#
# Execution de l'algorithme de recherche tabou.
#
# A appeler dans le main (dernière section).
#

def tabou(N, tailleMaxTabou):
    mListeRing = []
    listeTabou = []
    listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
    meilleurCout = evalue(listeRing, listeHorsRing, listeLienHorsRing)
    for i in range(N):
        meilleurCoutLocal = math.inf
        mListeRingLocal = []
        for j in range(len(listeRing)):
            copListeRing = copy.deepcopy(listeRing)
            copListeRing = permuteRing(copListeRing, j)
            cout = evalue(copListeRing, listeHorsRing, listeLienHorsRing)
            if cout < meilleurCoutLocal and copListeRing not in listeTabou:
                meilleurCoutLocal = cout
                mListeRingLocal = copy.deepcopy(copListeRing)
                if meilleurCoutLocal < meilleurCout:
                    meilleurCout = meilleurCoutLocal
                    mListeRing = copy.deepcopy(mListeRingLocal)
        listeTabou += [mListeRing]
        if len(listeTabou) > tailleMaxTabou:
            listeTabou = listeTabou[1:]
    return meilleurCout, mListeRing, listeHorsRing, listeLienHorsRing


######################################################################
#                      VOISINAGE VARIABLE                            #
######################################################################
#
# Fonction nécessaire à l'utilisation de l'algorithme à voisinage variable.
#

def permuteRing(listeRing, i):
    listeRing[i], listeRing[i - 1] = listeRing[i - 1], listeRing[i]
    return listeRing


######################################################################
#
# Execution de l'algorithme à voisinage variable.
#
# Elle renvoie :
# le ring (mlisteRing), les points hors du ring (mlisteHorsRing),
# les couples de points ring et hors-ring (mlisteLienHorsRing)
# et le cout de cette configuration (mcout).
#
# A appeler dans le main (dernière section).
#

def voisinageVariable(N):
    meilleurCout = math.inf
    mListeRing = []
    for i in range(N):
        listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire()
        for j in range(len(listeRing)):
            copListeRing = copy.deepcopy(listeRing)
            copListeRing = permuteRing(copListeRing, j)
            cout = evalue(copListeRing, listeHorsRing, listeLienHorsRing)
            if cout < meilleurCout:
                meilleurCout = cout
                mListeRing = copy.deepcopy(copListeRing)
    return meilleurCout, mListeRing, listeHorsRing, listeLienHorsRing


######################################################################
#                           RECUIT SIMULE                            #
######################################################################
#
# Une fonction de calcul du cout d'une configuration envoyée.
#

def getScore(Cr, Ca, ring, star, link):
    score = 0
    # Calcul du score du ring
    for i, elem in enumerate(ring):
        cr = Cr[ring[i] - 1][ring[(i + 1) % len(ring)] - 1]
        score += cr

    # Calcul du score d'assignement (dans le star)
    for i, elem in enumerate(star):
        ca = Ca[star[i] - 1][link[i] - 1]
        score += ca
    return score


######################################################################
#
# Les 3 fonctions suivantes sont des modifications possibles dans le ring :
#   - permRing : Une fonction qui permute deux élements dans le ring.
#   - permOutRing : Une fonction qui retire un élement du ring.
#   - permIntoRing : Une fonction qui ajoute un élement dans le ring.
#

def permRing(ring):
    # print("ping permRing")

    # Choisi deux elements du ring
    i = random.randrange(1, len(ring))
    j = random.randrange(len(ring))
    while i == j or j == 0:
        # Si c'est les mêmes ou on touche au premier, on en prend un autre
        j = random.randrange(len(ring))
    tmp = ring[i]
    ring[i] = ring[j]
    ring[j] = tmp
    return ring


def permOutOfRing(ring, star, link, Ca):
    # print("ping permOutOfRing")
    i = random.randrange(1, len(ring))
    elem = ring[i]
    # print(elem)
    del ring[i]

    # Si un élement du star était assigné à l'élement retiré,
    # on le reassigne au meilleur dispo
    for i, j in enumerate(link):
        if elem == j:
            minimum = min([j for i, j in enumerate(Ca[elem - 1]) if i + 1 in ring])
            minPos = Ca[elem - 1].index(minimum) + 1
            link[i] = minPos

    # On ajoute l'element retiré du ring dans le star,
    # et on l'assigne au meilleur élement du ring disponible
    star.append(elem)
    # j = random.randrange(len(ring))
    minimum = min([j for i, j in enumerate(Ca[elem - 1]) if i + 1 in ring])
    minPos = Ca[elem - 1].index(minimum) + 1
    link.append(minPos)
    return ring, star, link


def permIntoRing(ring, star, link):
    # print("ping permIntoRing")
    i = random.randrange(len(star))
    elem = star[i]
    del star[i]
    del link[i]
    ring.append(elem)
    return ring, star, link


######################################################################
#
# 'Create movement' est la manière de passer à un voisin.
#

def createMovement(ring, star, link, Ca):
    # On crée de nouvelles listes pour éviter des problemes de programmation, sinon ca bug
    newRing = ring[:]
    newStar = star[:]
    newLink = link[:]
    # Les trois mouvements disponibles sont: permuter dans le ring, ajouter un élement dans le ring et retirer un élement
    # du ring
    # on en prend un au hasard
    select = random.randrange(3)
    if select == 0:  # on fait une permutation dans le ring
        if len(newRing) <= 2:  # on ne peut pas faire une permutation si il n'y a qu'un seul élement
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing = permRing(newRing)
    elif select == 1:  # on retire un element du ring
        if len(newRing) <= 1:  # il doit toujours avoir un element du ring
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing, newStar, newLink = permOutOfRing(newRing, newStar, newLink, Ca)
    else:
        if len(newStar) <= 0:  # on ne peut pas ajouter un element dans le ring si il ne reste rien à ajouter
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing, newStar, newLink = permIntoRing(newRing, newStar, newLink)
    return newRing, newStar, newLink


######################################################################
#
# 'randomSolution' est la création d'une solution comme point de départ.
#

def randomSolution(nbr, Ca):
    ringRndTreshold = 0.5  # chance de mettre un élement dans le ring
    listOfPoint = list(range(2, nbr + 1))  # creation d'une liste de 2 à n

    random.shuffle(listOfPoint)  # on mélange
    ring = [1]  # le premier element du ring est toujours 1

    while len(
            ring) == 0:  # Ring peut pas etre vide. Ca devrait etre toujours le cas mais avant ring = [1] n'existait pas
        for i, elem in enumerate(listOfPoint):
            if random.random() <= ringRndTreshold:
                ring.append(elem)
                del listOfPoint[i]

    star = listOfPoint  # star est les points restant
    link = []
    for elem in star:  # on crée des affectations, qui sont les meilleurs disponibles
        # print(ring)
        # print(Ca[elem-1])
        # print([j for i, j in enumerate(Ca[elem-1]) if i + 1 in ring])
        minimum = min([j for i, j in enumerate(Ca[elem - 1]) if i + 1 in ring])
        minPos = Ca[elem - 1].index(minimum) + 1
        link.append(minPos)
    return ring, star, link


######################################################################
#
# Execution de l'algorithme Recuit Simulé.
#
# La fonction renvoie un ring, la liste de points en dehors du ring (star)
# et les liens entre les points du ring et  du star (link).
#
# Le cout est calculé à chaque itération dans le script, elle est bien sûr une condition
# essentielle dans la recherche de la meilleure configuration du problème.
#
# A appeler dans le main (dernière section).
#

def recuit(Cr, Ca, beginRing=None, beginStar=None, beginLink=None):
    nbrItr = 100000  # nombre d'iteration

    size = len(Cr[0])
    if beginRing == None or beginStar == None or beginLink == None:
        ring, star, link = randomSolution(size, Ca)
    else:  # on copie pour éviter les problemes
        ring = beginRing[:]
        star = beginStar[:]
        link = beginLink[:]
    t = 1000000  # temperature initiale
    tf = 1  # temperature finale
    N = 0.9  # palier
    currentScore = getScore(Cr, Ca, ring, star, link)

    while t > tf:
        for i in range(nbrItr):
            newRing, newStar, newLink = createMovement(ring, star, link, Ca)
            newScore = getScore(Cr, Ca, newRing, newStar, newLink)
            if newScore < currentScore:
                currentScore = newScore
                ring = newRing
                star = newStar
                link = newLink
            else:
                # sans cette ligne, les nombres deviennent trop extreme pour l'exp()
                if (newScore - currentScore) / t < -20:
                    P = 0
                else:
                    P = math.exp((currentScore - newScore) / t)
                if P >= random.random():
                    currentScore = newScore
                    ring = newRing
                    star = newStar
                    link = newLink

        print(ring, star, link, currentScore, t)
        if t > tf:
            t = t * N
    return ring, star, link


######################################################################
#                 ALGORITHME COLONIE DE FOURMIS                      #
######################################################################
#
# Fonction qui associe un point hors du ring à un autre point du ring
# le plus proche.
#

def donneSommetRingPlusProche(RING, sommet):
    m = math.inf
    s = -1
    for j in RING:
        if m > Ca[sommet - 1][j - 1]:
            m = Ca[sommet - 1][j - 1]
            s = j
    return s


######################################################################
#
# Fonction qui calcule le cout pour une configuration donnée.
#

def evalue(listeRing, listeHorsRing, listeLienHorsRing, Cr, Ca):
    c = 0
    for i in range(len(listeRing)):
        c += Cr[int(listeRing[i - 1])][int(listeRing[i])]
    for j in range(len(listeHorsRing)):
        c += Ca[int(listeHorsRing[j])][int(listeLienHorsRing[j])]
    return c


######################################################################
#
# Les deux fonctions suivantes ('donneVisibilite' et 'calculer_vecteur_proba')
# sont utilisées dans la fonction 'fourmi'.
#
# 'donneVisivilite' donne la visibilité de tout les points lorsque nous sommes au point n.
#

def donneVisibilite(n, listeRingRef, Cr):
    visibilite = []
    for elm in range(len(listeRingRef)):
        # Si la distance est egale à 0, on mets une visibilité égale à 0
        if Cr[elm][n] == 0:
            visibilite += [0]
        else:
            visibilite += [1 / Cr[elm][n]]
    return visibilite


#
# Fonction pour calculer la probabilité d'aller en chaque point de "listeRingRef".
#

def calculer_vecteur_proba(alpha, beta, listeRingRef, nonvisite, visibilite, ferom):
    P = []
    denom = 0
    for i in nonvisite:
        denom += ferom[listeRingRef.index(i)] ** alpha + visibilite[listeRingRef.index(i)] ** beta
    for elmt in range(len(listeRingRef)):
        if listeRingRef[elmt] in nonvisite:
            P += [(ferom[elmt] ** alpha + visibilite[elmt] ** beta) / denom]
        else:
            P += [0]
    return P


#
# Algorithme pour une fourmi. Pour fonctionner, elle a besoin des deux
# dernières fonctions : 'donneVisibilite' et 'calculer_vecteur_proba'.
#

def fourmi(alpha, beta, listeRingRef, ferom, Cr):
    # on choisie un sommet de départ
    n = random.randint(0, len(listeRingRef) - 1)
    nonvisite = copy.deepcopy(listeRingRef)
    listeSommet = [listeRingRef[n]]
    nonvisite.remove(listeRingRef[n])
    i = 0
    # tant la fourmi n'a pas visité tout les sommets
    while len(nonvisite) > 0:
        i += 1
        visibilite = donneVisibilite(n, listeRingRef, Cr)
        P = calculer_vecteur_proba(alpha, beta, listeRingRef, nonvisite, visibilite, ferom[n])
        n = random.choices(listeRingRef, P, k=1)[0]
        nonvisite.remove(n)
        listeSommet += [n]
        n = listeRingRef.index(n)
    return listeSommet


######################################################################
#
# Fonctions nécessaires à l'implémentation de la colonie de fourmis.
#

def conversionAller(RING, PEER):
    listeHorsRing = []
    listeLienHorsRing = []
    listeRing = (np.array(RING) - np.ones((1, len(RING)))).tolist()[0]
    for i in PEER:
        listeHorsRing += [i[0]]
        listeLienHorsRing += [i[1]]
    return listeRing, listeHorsRing, listeLienHorsRing


def conversionRetour(listeRing, listeHorsRing=[], listeLienHorsRing=[]):
    RING = np.array(listeRing) + np.ones((1, len(listeRing)))
    RING = np.array(RING.tolist(), dtype='int').tolist()[0]
    RING = RING[RING.index(1.):len(RING)] + RING[:RING.index(1)]
    '''PEER=[]
    STAR=listeHorsRing
    for i in range(listeLienHorsRing):
        PEER+=[[listeHorsRing[i],listeLienHorsRing[i]]]'''
    return RING


def deposeFerom(dferom, listeRing, listeRingRef, Q, cout):
    for i in range(len(listeRing) - 1):
        dferom[listeRingRef.index(listeRing[i])][listeRingRef.index(listeRing[i + 1])] += Q / cout
    return dferom


def evaporerFerom(dferom, ferom, omega):
    for i in range(len(ferom)):
        for j in range(len(ferom)):
            ferom[i][j] = ferom[i][j] * (1 - omega) + dferom[i][j]
    dferom = np.zeros((len(dferom), len(dferom))).tolist()
    return ferom, dferom


######################################################################
#
# Algorithme pour une colonie de fourmis :
#
# Il faut notamment lui fournir :
#   - N : nombre de fois qu'on fait parourir le ring par les fourmis.
#   - alpha : poids donné aux féromones pour choisir le chemin pris par une fourmi.
#   - beta : poids donné à la visibilité pour choisir le chemin pris par une fourmi.
#   - omega : taux (entre 0 et 1) de féromone gardée à chaque parcour du graphe.
#   - Q : quantité (feromone*poids) de féromones déposées quand une fourmi passe sur un sommet.


def colonieFourmi(nbParcour, nbFourmis, alpha, beta, Q, omega, mlisteRing, listeHorsRing, listeLienHorsRing, Cr, Ca):
    dferom = np.zeros((len(mlisteRing), len(mlisteRing))).tolist()
    ferom = np.zeros((len(mlisteRing), len(mlisteRing))).tolist()
    mcout = evalue(mlisteRing, listeHorsRing, listeLienHorsRing, Cr, Ca)
    listeRingRef = copy.deepcopy(mlisteRing)
    for k in range(nbParcour):
        for f in range(nbFourmis):
            listeRing = fourmi(alpha, beta, listeRingRef, ferom, Cr)
            cout = evalue(listeRing, listeHorsRing, listeLienHorsRing, Cr, Ca)
            dferom = deposeFerom(dferom, listeRing, listeRingRef, Q, cout)
            if cout < mcout:
                mcout = cout
                mlisteRing = copy.deepcopy(listeRing)
        ferom, dferom = evaporerFerom(dferom, ferom, omega)
    return mlisteRing, listeHorsRing, listeLienHorsRing, mcout


######################################################################
#
# Pour executer 'CDF' (l'algorithme de colonie de fourmis),
# il lui faut ces fonctions nécessaires à son bon déroulement :
#

# construit la liste "listeLienHorsRing",
# en associant chaque sommet hors ring au sommet du ring le plus proche
def attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing):
    for i in range(len(listeHorsRing)):
        m = math.inf
        s = -1
        for j in range(len(listeRing)):
            if m > Ca[listeHorsRing[i]][listeRing[j]]:
                m = Ca[listeHorsRing[i]][listeRing[j]]
                s = listeRing[j]
        listeLienHorsRing[i] = s


def solutionAleatoire(N):
    listeHorsRing = np.array(np.linspace(1, len(Ca), len(Ca) - 1, endpoint=False), dtype='int').tolist()
    listeRing = [0]
    for i in range(N - 2):
        n = random.randint(0, len(Ca) - i - 2)
        listeRing.append(listeHorsRing[n])
        listeHorsRing.remove(listeHorsRing[n])
    listeLienHorsRing = np.zeros(len(listeHorsRing))
    attributSommetRing(listeRing, listeHorsRing, listeLienHorsRing)
    return listeRing, listeHorsRing, listeLienHorsRing


def fourmiApartirDAleatoire(nbParcour, i, nbFourmis, alpha, beta, Q, omega, coutSelonNbSommet, mcout, mlisteRing,
                            mlisteHorsRing, mlisteLienHorsRing):
    listeRing, listeHorsRing, listeLienHorsRing = solutionAleatoire(i)
    listeRing = \
    colonieFourmi(nbParcour, nbFourmis, alpha, beta, Q, omega, listeRing, listeHorsRing, listeLienHorsRing, Cr, Ca)[0]
    cout = evalue(listeRing, listeHorsRing, listeLienHorsRing, Cr, Ca)
    coutSelonNbSommet += [cout]
    if cout < mcout:
        mcout = cout
        mlisteRing = copy.deepcopy(listeRing)
        mlisteHorsRing = copy.deepcopy(listeHorsRing)
        mlisteLienHorsRing = copy.deepcopy(listeLienHorsRing)
    return mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing


def construitProbaNbSommet(coutSelonNbSommet):
    probaNbSommet = []
    somme = sum(coutSelonNbSommet)
    for i in coutSelonNbSommet:
        probaNbSommet += [i / somme]
    return probaNbSommet


######################################################################
#CDF est un hybride entre colonie de fourmis et une recherche aléatoire
#Dans un premier temps on fait tourner l'algorithme des foumis sur des solutions
#générées aléatoirement, dont la taille du ring va de 1 element à 100% des éléments
#Ensuite nous relançons l'algo des fourmis sur nbIter solutions générées aléatoirement,
#avec une probabilité supérieure que la taille du ring soit de la taille même taille
#que celle des solutions qui ont renvoyé de bonnes solutions lors de la première phase
# Execution de l'algorithme pour une colonie de fourmis :
# Cette fonction renvoie :
# le ring (mlisteRing), les points hors du ring (mlisteHorsRing),
# les couples de points ring et hors-ring (mlisteLienHorsRing)
# et le cout de cette configuration (mcout).
#
# A appeler dans le main (dernière section).
#
def CDF(nbParcour, nbIter, nbFourmis, alpha, beta, Q, omega):
    mcout = math.inf
    mlisteRing, mlisteHorsRing, mlisteLienHorsRing = [], [], []
    coutSelonNbSommet = []
    for i in range(len(Ca)):
        mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing = fourmiApartirDAleatoire(20, i, 20, alpha, beta, Q,
                                                                                        omega, coutSelonNbSommet, mcout,
                                                                                        mlisteRing, mlisteHorsRing,
                                                                                        mlisteLienHorsRing)
    listeNbSommet = np.array(np.linspace(1, len(Ca) + 1, len(Ca), endpoint=False), dtype='int').tolist()
    probaNbSommet = construitProbaNbSommet(coutSelonNbSommet)
    for j in range(nbIter):
        n = random.choices(listeNbSommet, probaNbSommet, k=1)[0]
        mcout, mlisteRing, mlisteHorsRing, mlisteLienHorsRing = fourmiApartirDAleatoire(nbParcour, n, nbFourmis, alpha,
                                                                                        beta, Q,
                                                                                        omega, coutSelonNbSommet, mcout,
                                                                                        mlisteRing, mlisteHorsRing,
                                                                                        mlisteLienHorsRing)
    return mlisteRing, mlisteHorsRing, mlisteLienHorsRing, mcout


######################################################################
#                   ALGORITHME EVOLUTIONNAIRE                        #
######################################################################
#
# Classe INDIVIDU qui représente une configuration du problème.
#
# Pour un individu, nous avons donc :
#   - RING : le ring sous forme d'une liste de points.
#   - STAR : liste de points hors du ring.
#   - PEER : liste couples de points.
#   - Cost : cout total de la configuration.
#

class Individu:
    def __init__(self, RING, STAR, PEER, Cost):
        self.RING = RING
        self.STAR = STAR
        self.PEER = PEER
        self.Cost = Cost


######################################################################
#
# Initialisation des RINGS & STARS (les points hors du ring).
#
# 2 initialisations différentes :
#   - initiaterandom(N) : initialisation aléatoire.
#   - initiate_GT(N, L) : initialisation de RINGS  de grande taille.


# Initialisation aléatoire
def initiaterandom(N):
    RING = [1]
    # STAR contient initialement tous les sommets nommés: 2 -> N
    # linspace(START, STOP (on ne prend pas cette valeur), nrbe éléments)
    STAR = np.array(np.linspace(2, N + 1, (N - 1), endpoint=False),
                    dtype='int').tolist()
    # print(STAR)
    # nombre d'éléments à switch entre STAR et RING,
    # donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(0, N - 1)
    for i in range(nbr):
        # numéro du sommet à switch
        n = random.randint(0, N - i - 2)
        # 0 -> (N-2) car correspond à l'indice du sommet et non à sa valeur
        RING.append(STAR[n])
        STAR.remove(STAR[n])
    return RING, STAR


# Initialise des individus de grande taille.
# L'algo evolutionnaire ne trouve pas de bonne valeur quand le RING est grand,
# d'où l'utilité d'en avoir de grande taille.
def initiate_GT(N, L):
    RING = [1]
    # STAR contient initialement tous les sommets nommés: 2 -> N
    # linspace(START, STOP (on ne prend pas cette valeur), nrbe éléments)
    STAR = np.array(np.linspace(2, N + 1, (N - 1), endpoint=False),
                    dtype='int').tolist()
    # print(STAR)
    # nombre d'éléments à switch entre STAR et RING,
    # donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(L, N - 1)
    for i in range(nbr):
        # numéro du sommet à switch
        n = random.randint(0, N - i - 2)
        # 0 -> (N-2) car correspond à l'indice du sommet et non à sa valeur
        RING.append(STAR[n])
        STAR.remove(STAR[n])
    return RING, STAR


######################################################################
#
# Fonction d'évaluation :
#

# Retourne le coût total (c) et les arcs optimaux (PEER)
def evaluate(RING, STAR, Cr, Ca):
    c = Cr[0][RING[-1] - 1]  # lien entre dernier elem de RING et 1
    # print("cout initial : ", c)
    PEER = []  # Contient les arcs optimaux pour STAR
    # Coût du RING
    for i in range(len(RING) - 1):
        c += Cr[RING[i] - 1][RING[i + 1] - 1]
        # print("update cout r ({}) : {}".format(i, c))
    # MAJ de PEER et du coût
    for e in STAR:
        # par défaut, pointe vers 1 qui est de toute façon dans le RING
        cmin = Ca[e - 1][0]
        r_min = RING[0]  # pareil
        for r in RING:
            if Ca[e - 1][r - 1] < cmin:
                cmin = Ca[e - 1][r - 1]
                r_min = r
        PEER.append([e, r_min])
        c += cmin
        # print("update cout hr ({}) : {}".format(i, c))
    return c, PEER


######################################################################
#
# Fonctions de croisement :
#
# Ces fonctions créent, à partir de parents,
# les enfants qui deviendront les parents lors de l'itération suivante
# On distingue 3 fonctions différentes :
#   - croisement_1pt
#   - croisement_2pt
#   - croisement_uniforme
#

# On commence à remplir e1 par p1 puis par p2
def croisement_1pt(p1, p2):
    enfants = []
    e1 = [1]
    e2 = [1]
    # enfant1
    n1 = random.randint(1, len(p1))
    for i in range(1, n1):
        e1.append(p1[i])
    if n1 < len(p2):  # si on a complètement rempli e1 par p1, on passe à e2
        for i in range(n1, len(p2)):  # si n1 == len(p2), il ne se passe rien
            if p2[i] in e1:
                continue
            else:
                e1.append(p2[i])
    enfants.append(e1)
    # enfant2
    n2 = random.randint(1, len(p2))
    for i in range(1, n2):
        e2.append(p2[i])
    if n2 < len(p1):
        for i in range(n2, len(p1)):
            if p1[i] in e2:
                continue
            else:
                e2.append(p1[i])
    enfants.append(e2)
    # print("p1 : " + str(p1) + "\n" + "p2 : " + str(p2) + "\n" + "e1 : " + str(e1) + "\n" + "e2 : " + str(e2) + "\n")
    return enfants


# On remplit e1 par p1, puis par p2 et on finit par p1
def croisement_2pt(p1, p2):
    enfants = []
    e1 = [1]
    e2 = [1]
    # enfant1
    n11 = random.randint(1, min(len(p1), len(p2)) - 1)
    # on coupe avant à la fin du plus petit parent,
    # pour être sûr d'avoir un mélange génétique (sinon pas d'intérêt de croiser)
    n12 = random.randint(n11, min(len(p1), len(p2)))
    # si n12 - n11 == 1, c'est l'équivalent du croisement_1pt sur le dernier indice
    # et la dernière boucle for doit être ignorée
    for i in range(1, n11):
        e1.append(p1[i])
    for i in range(n11, n12):
        if p2[i] in e1:
            continue
        else:
            e1.append(p2[i])
    if n12 < len(p1):
        for i in range(n12, len(p1)):
            e1.append(p1[i])
    enfants.append(e1)
    # enfant2
    n21 = random.randint(1, min(len(p1), len(p2)) - 1)
    n22 = random.randint(n11, min(len(p1), len(p2)))
    for i in range(1, n11):
        e2.append(p2[i])
    for i in range(n21, n22):
        if p1[i] in e2:
            continue
        else:
            e1.append(p1[i])
    if n22 < len(p2):
        for i in range(n22, len(p2)):
            e2.append(p2[i])
    enfants.append(e2)
    # print(n11, n12)
    # print("p1 : " + str(p1) + "\n" + "p2 : " + str(p2) + "\n" + "e1 : " + str(e1) + "\n" + "e2 : " + str(e2) + "\n")
    return enfants


# on choisit aléatoirement pour chaque sommet si l'enfant hérite de p1 ou p2
def croisement_uniforme(p1, p2):
    enfants = []
    e1 = [1]
    e2 = [1]
    # enfant1
    # e1 aura la taille de p1
    for i in range(1, min(len(p1), len(p2))):
        choix = bool(random.getrandbits(1))  # return True or False
        if choix:
            e1.append(p1[i])
        else:
            e1.append(p2[i])
    if len(p1) > len(p2):
        for i in range(len(p2), len(p1)):
            e1.append(p1[i])
    enfants.append(e1)
    # enfant2
    # e2 aura la taille de p2
    for i in range(1, min(len(p1), len(p2))):
        choix = bool(random.getrandbits(1))  # return True or False
        if choix:
            e2.append(p2[i])
        else:
            e2.append(p2[i])
    if len(p2) > len(p1):
        for i in range(len(p1), len(p2)):
            e2.append(p2[i])
    enfants.append(e2)
    # print("p1 : " + str(p1) + "\n" + "p2 : " + str(p2) + "\n" + "e1 : " + str(e1) + "\n" + "e2 : " + str(e2) + "\n")
    return enfants


######################################################################
#
# Fonctions de sélection : Permet la sélection d'individus dans une population.
# Les trois fonctions suivantes représentent trois méthodes de sélection :
#   - selection_elitisme.
#   - selection_tournoi.
#   - selection_roulette.
#

def selection_elitisme(T, popu):
    popu = sorted(popu, key=lambda x: x.Cost)  # Tri des individus de Population selon leur score
    popu = popu[:T]  # on ne garde que les individus avec le plus faible score
    return popu


def selection_tournoi(T, popu):
    newpop = []
    indices = [i for i in range(len(popu))]  # indices des Individus
    for i in range(T):
        A = random.choice(indices)
        B = random.choice([j for j in indices if j != A])  # on prend 2 indices différents car 2 adversaires différents
        if popu[A].Cost < popu[B].Cost:
            newpop.append(popu[A])
            indices.remove(A)  # A est sélectionné mais B peut continuer à participer à des tournois
        else:
            newpop.append(popu[B])
            indices.remove(B)
    return newpop


# On associe à chaque individu une probabilité d'être tiré au sort en fonction de son score
# Tel quel pas très adapté à notre problème tant les proba sont faibles
# Il faudrait faire l'étalooner sur la différence de score entre le Cost min et Cost max
# info : https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
def selection_roulette(T, popu):
    s = 0
    for e in popu:
        s += e.Cost
    proba = []
    for i in range(len(popu)):
        proba.append((1 / popu[i].Cost) / s)  # 1/popu[i] car on veut prendre le plus petit
    print(proba)
    newpop = []
    while len(newpop) != T:
        for i in range(len(popu)):
            chance = random.random()
            if chance > proba[i]:
                continue  # cet individu n'est pas sélectionné
            else:
                newpop.append(popu[i])
    return newpop


######################################################################
#
# Fonction qui execute l'algorithme colonie de fourmis sur une population.
#
# Elle est une version adaptée pour la version hybridée de l'algorthme évolutionnaire
# Elle est appelée lors de la sélection de la population afin de recommencer une itération.
# On peut ainsi éspérer une meilleure population avec une configuration possèdant
# un coût moindre qu'avant son appel.
#

def fourmisSurPopulation(Population, Cr, Ca):
    for indv in Population:
        listeRing, listeHorsRing, listeLienHorsRing = conversionAller(indv.RING, indv.PEER)
        mlisteRing, listeHorsRing, listeLienHorsRing, cout = colonieFourmi(20, 20, 1, 1, 1, 0.75,
                                                                           listeRing, listeHorsRing, listeLienHorsRing,
                                                                           Cr, Ca)
        indv.Cost = cout
        indv.RING = conversionRetour(mlisteRing)
    return Population


######################################################################
#
# Fonctions de mutation :
#
# Ces fonctions modifient les enfants pour tenter d'améliorer le coût.
#
# On distingue 3 fonctions différentes :
#   - mutation 1 : permutation triviale de deux points au sein du ring.
#   - mutation 2 : inversion du ring (on "casse" le ring en deux et change le sens d'une moitié).
#   - mutation 3 :  mutation par recuit simulé.
#

def mutation1(Pm, Enfant):
    for i in range(len(Enfant)):
        chance = random.random()
        if chance > Pm:
            continue  # il n'y a pas de mutation

        else:  # il y a mutation chez l'enfant
            # si Enfant est de taille 2, on ne permute pas car 1 toujours en 1ère place
            if len(Enfant[i]) < 3:
                continue
            else:
                # indice du somment à permuter (pas 0 et pas dernier)
                n = random.randint(1, len(Enfant[i]) - 2)
                Enfant[i][n], Enfant[i][n + 1] = Enfant[i][n + 1], Enfant[i][n]
    return Enfant


def mutation2(Pm, Enfant):
    for i in range(len(Enfant)):
        chance = random.random()
        if chance > Pm:
            continue  # il n'y a pas de mutation
        else:  # il y a mutation chez l'enfant
            # si Enfant est de taille 2, on ne permute pas car 1 toujours en 1ère place
            if len(Enfant[i]) < 4:
                continue
            else:
                temp = list(Enfant[i])
                taille = 1
                while taille % 2 != 0:
                    taille = random.randint(2, len(temp) - 2)
                for j in range(int(taille / 2)):
                    temp.pop(0)
                    temp.pop(-1)
                temp.reverse()
                Enfant[i][int(taille / 2):len(Enfant[i]) - int(taille / 2)] = temp
    return Enfant


def mutation3(Pm, Enfant, Cr, Ca):
    for i in range(len(Enfant)):
        chance = random.random()
        if chance > Pm:
            continue  # il n'y a pas de mutation
        else:  # il y a mutation chez l'enfant
            if len(Enfant[i]) < 2:
                continue
            else:
                Enfant[i] = recuit2(Cr, Ca, Enfant[i])
    return Enfant


######################################################################
#
# Les deux fonctions suivantes sont des adaptations du Recuit Simulé
# implémenté plus haut, de manière à ce qu'ils s'insèrent dans une
# version hybridée de l'algorithme évolutionnaire (via mutation3).
#

# Prérecuit appelé dans recuit2()
def preRecuit2(Ca, ring):
    nbr = len(Ca[0])
    star = list(range(1, nbr + 1))
    link = []

    for point in ring:
        star.remove(point)
    for point in star:
        minimum = min([j for i, j in enumerate(Ca[point - 1]) if i + 1 in ring])
        minPos = Ca[point - 1].index(minimum) + 1
        link.append(minPos)
    return ring, star, link


# Recuit simulé adapté à l'algo évolutionnaire
def recuit2(Cr, Ca, ring):
    nbrItr = 20

    t = 3
    tf = 0.1
    N = 0.9

    # fonction qui va générer le star et le link en fonction du ring passé en paramètre
    ring, star, link = preRecuit2(Ca, ring)
    currentScore = getScore(Cr, Ca, ring, star, link)

    while t > tf:
        for i in range(nbrItr):
            newRing, newStar, newLink = createMovement(ring, star, link, Ca)
            newScore = getScore(Cr, Ca, newRing, newStar, newLink)
            if newScore < currentScore:
                currentScore = newScore
                ring = newRing
                star = newStar
                link = newLink
            else:
                if (newScore - currentScore) / t < -20:
                    P = 0
                else:
                    P = math.exp((currentScore - newScore) / t)
                if P >= random.random():
                    currentScore = newScore
                    ring = newRing
                    star = newStar
                    link = newLink

        # print(ring, star, link, currentScore, t)
        if t > tf:
            t = t * N
    return ring


######################################################################
#
# Execution de l'algorithme évolutionnaire.
#
# La fonction renvoie une population de d'INDIVIDUS,
# càd les configurations du problème avec leurs coûts.
#
# A appeler dans le main (dernière section).
#

def evolutionnaire(N, Cr, Ca, t_max):
    # paramètres à modifier
    T = 10  # Taille de la population
    G = 10  # Nombre maximal de génération
    Pc = 0.9  # Probabilité de croisement
    Pm = 0.8  # Probabilité de mutation

    # on peut choisir d'ajouter mannuellement des individus de grande taille
    L = int(N * 1)  # Taille de RING min pour les individus de grande taille
    if L >= N:
        L = N - 1  # pour les fct initiate
    NL = int(T * 0.5)  # Nombre d'individus de GT à ajouter


    # On va faire plusieurs échantillons de population dont on va sélectionner le meilleur individu
    best_indv = []

    m = 0  # compte le nombre d'échantillons de populations défférentes avec lequelles on travaille
    t_init = time.time()  # initialisation du temps de calcul
    while time.time() - t_init < t_max:
        m += 1

        # Initialisation
        Population = []
        best = []  # Tableau du meilleur individu pour chaque génération
        for i in range(T):
            RING, STAR = initiate_GT(N, L)
            c, PEER = evaluate(RING, STAR, Cr, Ca)
            Population.append(Individu(RING, STAR, PEER, c))

        for g in range(G):  # G générations se succèdent
            if time.time() - t_init > t_max:  # si on dépasse le temps imparti, on sort de la boucle
                break
            print("\n" + str(m) + " - Generation : " + str(g))

            # Sélection des couples
            Couple = []
            pop = [i for i in range(0, T)]  # liste des indices des individus
            for i in range(int(T / 2)):
                A = random.choice(pop)
                pop.remove(A)
                B = random.choice(pop)
                pop.remove(B)
                Couple.append([Population[A], Population[B]])

            # Croisement
            Enfant = []
            for i in range(int(T / 2)):
                chance = random.random()  # chance in [0,1] car pas sûr de croiser
                if chance > Pc:
                    # print("Pas croisement" + "\n")
                    continue  # il n'y a pas de reproduction

                else:  # il y a reproduction (et donc croisement des caractéristiques)
                    p1 = Couple[i][0].RING
                    p2 = Couple[i][1].RING
                    if len(p1) == 1 or len(p2) == 1:  # si l'indidividu est de taille 1, on ne croise pas
                        continue  # équivalent à continue si on était dans la loop
                    else:
                        e1, e2 = croisement_1pt(p1, p2)
                        #e1, e2 = croisement_2pt(p1, p2)
                        #e1, e2 = croisement_uniforme(p1, p2)
                        Enfant.append(e1)
                        Enfant.append(e2)

            # Mutation
            #Enfant = mutation1(Pm, Enfant)  # mutation par permutation
            #Enfant = mutation2(Pm, Enfant)         # mutation par inversion
            Enfant = mutation3(Pm, Enfant, Cr, Ca)  # mutation par recuit simulé

            # Construction des individus Enfants
            for i in range(len(Enfant)):
                STAR = []
                for j in range(2, N + 1):
                    if j not in Enfant[i]:
                        STAR.append(j)
                c, PEER = evaluate(Enfant[i], STAR, Cr, Ca)
                Population.append(Individu(Enfant[i], STAR, PEER, c))  # parents + enfants > T -> sélection à faire

            # Sélection d'individus
            if len(Population) != T:  # si aucun croisement n'a eu lieu à cause de Pc, il n'y a pas de sélection
                Population = selection_elitisme(T, Population)  # Selection par élitisme.
                # Population = selection_roulette(T, Population) # Sélection par roulette.
                # Population = selection_tournoi(T, Population) # Sélection par tournoi.

            # Meilleur individu de la population g
            print("best = " + str(Population[0].Cost))
            best.append(Population[0].Cost)

            # Ajout d'individus de grande taille si le RING optimal est très rempli
            # selon le besoin, commenter/décommenter cette partie :
            """
            best.append(Population[0].Cost)
            if g > 10:  # on fait minimum 10 itérations
                if (best[g-2]/best[g]) < 1.01:  # moins de 1% d'amélioration entre 3 générations
                    for l in range(NL):  # on rajoute NL individus de taille L min
                        RING, STAR = initiate_GT(N, L)
                        c, PEER = evaluate(RING, STAR, Cr, Ca)
                        Population.append(Individu(RING, STAR, PEER, c))
            #print(len(Population))
            #"""

            # Break si on est bloqué sur un minimum
            # Donc que la valeur ne change pas pdt plusieurs générations d'affilée
            if g > 16:
                if best[g - 14] == best[g]:
                    best_indv.append(Population[0])  # on sauve le nvx meilleur
                    break  # on passe à l'échantillon suivant
            if g == G:
                best_indv.append(Population[0])  # on n'a pas atteint un min local mais pas de assez de generations ou temps écoulé

    return best_indv


######################################################################
#                               MAIN                                 #
######################################################################
#
# Script faisant appel aux différents algorithmes implémentés.
#

if __name__ == '__main__':

    ring = []
    horsRing = []
    cout = 0

    # Nom du dataset à lire dans le sous-dossier 'Datasets'.
    file = "data3"

    # Extraction des données
    N, Ca, Cr = dataExtract(file)

    # Choix de l'algorithme à executer
    # Ring, Star, Link = recuit(Cr, Ca)
    a = time.time()
    popu = evolutionnaire(N, Cr, Ca, 30)
    popu = sorted(popu, key=lambda x: x.Cost)
    for i in range(len(popu)):
        print(popu[i].Cost)
    print("Temps = " + str(time.time() - a))
    # mlisteRing, listeHorsRing, listeLienHorsRing, mcout = CDF(50, 50, 20, 1, 1, 1, 0.75)

    # Sélection de la meilleure configuration parmi la population
    # >>>>>>>>>>> A FAIRE <<<<<<<<<<<<

    # Ecriture de la solution dans le sous-dossier 'Outputs'.
    writeOutput(file, ring, horsRing, cout)