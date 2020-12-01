import math
import random
import numpy as np


################
# RING et STAR #
################
# Initialisation barbare
def initiate(N):
    RING = []
    STAR = []
    # élément du RING
    A = N - 10  # nbre d'élément dans le RING
    for i in range(A):
        RING.append(i + 1)
    # element dans STAR
    for i in range(1, N + 1):
        # print(i)
        if i in RING:
            continue
        else:
            STAR.append(i)
    return RING, STAR


# Initialisation aléatoire
def initiaterandom(N):
    RING = [1]
    # STAR contient initialement tous les sommets nommés: 2 -> N
    STAR = np.array(np.linspace(2, N + 1, (N - 1), endpoint=False),
                    dtype='int').tolist()  # linspace(START, STOP (on ne prend pas cette valeur), nrbe éléments)
    # print(STAR)
    # nombre d'éléments à switch entre RING et STAR, donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(0, N - 1)
    for i in range(nbr):
        # numéro du sommet à switch
        n = random.randint(0, N - i - 2)  # 0 -> (N-2) car correspond à l'indice du sommet et non à sa valeur
        RING.append(STAR[n])
        STAR.remove(STAR[n])
    return RING, STAR


################
# cost et PEER #
################
# Retourne le coût total et les arcs optimaux (PEER) pour le STAR
def evaluate(RING, STAR, N, Cr, Ca):
    c = 0
    PEER = []  # Contient les arcs optimaux pour STAR
    # Coût du RING
    for i in range(len(RING) - 1):
        c += Cr[RING[i] - 1][RING[i + 1] - 1]
    # MAJ de PEER et du coût
    for e in STAR:
        cmin = Ca[e - 1][0]
        i_min = 0
        for i in range(N):
            if Ca[e - 1][i] == 0 and i == 0:  # dans le cas où 1 est dans le STAR
                cmin = Ca[e - 1][i + 1]
            elif Ca[e - 1][i] == 0:
                continue
            elif Ca[e - 1][i] < cmin:
                cmin = Ca[e - 1][i]
                i_min = i
        PEER.append([e, i_min + 1])
        c += cmin
    return c, PEER


##################
# Evolutionnaire #
##################
class Individu:
    def __init__(self, RING, STAR, PEER, Cost):
        self.RING = RING
        self.STAR = STAR
        self.PEER = PEER
        self.Cost = Cost


def evolutionnaire(N, Cr, Ca):
    T = 4  # Taille de la population
    G = 2  # Nombre maximal de génération
    Pc = random.uniform(0.5, 0.9)  # Probabilité de croisement
    Pm = random.uniform(0.05, 0.1)  # Probabilité de mutation

    # Initialisation
    Population = []
    for i in range(T):
        RING, STAR = initiaterandom(N)
        c, PEER = evaluate(RING, STAR, N, Cr, Ca)
        Population.append(Individu(RING, STAR, PEER, c))

    # Sélection
    Couple = []
    pop = [i for i in range(0, T)]
    for i in range(int(T/2)):
        A = random.choice(pop)
        pop.remove(A)
        B = random.choice(pop)
        pop.remove(B)
        Couple.append([Population[A], Population[B]])

    # Croisement
    for i in range(int(T/2)):
        p1 = Couple[i][0].RING
        p2 = Couple[i][1].RING
        e1 = [1]
        e2 = [1]
        if len(p1) == 1 or len(p2) == 1:  # si l'indidividu est de taille 1, on ne croise pas
            continue
        else:
            # enfant 1
            e1.append(p2[-1])  # on choisit un le dernier elem p2 à introduire dans e1
            for j in range(2, len(p1)):  # on construit e1 avec les éléments de p1
                if e1[1] == p1[j]:  # l'élément switch ne peut pas se retrouver 2 fois dans e1
                    continue
                else:
                    e1.append(p1[j])
            # enfant 2
            e2.append(p1[-1])
            for j in range(2, len(p2)):
                if e2[1] == p2[j]:
                    continue
                else:
                    e2.append(p2[j])
        print("p1 : " + str(p1) + "\n" + "p2 : " + str(p2) + "\n" + "e1 : " + str(e1) + "\n" + "e2 : " + str(e2) + "\n")


    # Affichage
    #for i in range(T):
    #    print("Individu " + str(i + 1) + "\n" + "RING : " + str(Population[i].RING) + "\n" + "STAR : " + str(Population[i].STAR) + "\n" + "PEER : "
    #          + str(Population[i].PEER) + "\n" + "Cost : " + str(Population[i].Cost) + "\n")

    return Population, Couple


########
# Main #
########
if __name__ == '__main__':

    #######################
    # Lecture des données #
    #######################
    with open("Datasets/data1.txt") as f:
        Cr = []  # cout du ring
        Ca = []  # cout des liens vers ring

        data = f.readline()
        data = data.split()
        data = list(map(int, data))
        N = data[0]  # Nombre de sommets du problème
        # print(N)

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

        # print("fin d'extraction des donnees")

    ##############
    # Résolution #
    ##############
    #listeRing, listeHorsRing = initiate(N)
    listeRing, listeHorsRing = initiaterandom(N)
    cost, listeLienHorsRing = evaluate(listeRing, listeHorsRing, N, Cr, Ca)

    pop, couple = evolutionnaire(N, Cr, Ca)
    print(pop)
    print(couple)


    #####################
    # Affichage et test #
    #####################

    #print("RING : " + str(listeRing) + "\n" + "STAR : " + str(listeHorsRing) + "\n" + "PEER : " + str(listeLienHorsRing) + "\n" + "Cost : " + str(cost))

    """
    #Test des éléments
    sum = 0
    sum1 = 0
    for i in range(1, 52):
        sum += i  # valeur à laquelle on doit arriver
    for a in listeRing:
        sum1 += a
    for b in listeHorsRing:
        sum1 += b
    print(sum, sum1)
    
    print("end")
    #"""
