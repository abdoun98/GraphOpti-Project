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
    RING = []
    # STAR contient initialement tous les sommets nommés: 1 -> N
    STAR = np.array(np.linspace(1, N+1, N, endpoint=False), dtype='int').tolist()  # linspace(START, STOP (on ne prend pas cette valeur), nrbe éléments)
    #print(STAR)
    # nombre d'éléments à switch entre RING et STAR, donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(1, N)
    for i in range(nbr):
        # numéro du sommet à switch
        n = random.randint(0, N - i - 1)  # 0 -> (N-1) car correspond à l'indice du sommet et non à sa valeur
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
                cmin = Ca[e-1][i+1]
            elif Ca[e - 1][i] == 0:
                continue
            elif Ca[e - 1][i] < cmin:
                cmin = Ca[e - 1][i]
                i_min = i
        PEER.append([e, i_min + 1])
        c += cmin
    return c, PEER


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
        #print(N)

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

    #####################
    # Affichage et test #
    #####################

    print("RING : " + str(listeRing) + "\n" + "STAR : " + str(listeHorsRing) + "\n" + "PEER : " + str(listeLienHorsRing) + "\n" + "Cost : " + str(cost))

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
