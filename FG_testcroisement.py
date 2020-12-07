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
    # nombre d'éléments à switch entre STAR et RING, donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(0, N - 1)
    for i in range(nbr):
        # numéro du sommet à switch
        n = random.randint(0, N - i - 2)  # 0 -> (N-2) car correspond à l'indice du sommet et non à sa valeur
        RING.append(STAR[n])
        STAR.remove(STAR[n])
    return RING, STAR


#Initialise des individus de grande taille
#L'algo evolutionnaire ne trouve pas de bonne valeur quand le RING est grand, d'où cette fct
def initiate_GT(N, L):
    RING = [1]
    # STAR contient initialement tous les sommets nommés: 2 -> N
    STAR = np.array(np.linspace(2, N + 1, (N - 1), endpoint=False),
                    dtype='int').tolist()  # linspace(START, STOP (on ne prend pas cette valeur), nrbe éléments)
    # print(STAR)
    # nombre d'éléments à switch entre STAR et RING, donc bien de 0 -> N-1 (le ring doit contenir min 1 elem)
    nbr = random.randint(L, N - 1)
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
        cmin = Ca[e - 1][0]  # par défaut, pointe vers 1 qui est de toute façon dans le RING
        r_min = RING[0]  # pareil
        for r in RING:
            if Ca[e - 1][r - 1] < cmin:
                cmin = Ca[e - 1][r - 1]
                r_min = r
        PEER.append([e, r_min])
        c += cmin
        # print("update cout hr ({}) : {}".format(i, c))
    return c, PEER


##############
# Croisement #
##############
# Pas ouf, à ne pas utiliser
def croisement_base(p1, p2):
    enfants = []
    e1 = [1]
    e2 = [1]  # chaque solution doit commencer par 1
    # enfant 1
    e1.append(p2[-1])  # on choisit le dernier elem p2 à introduire dans e1
    for j in range(2, len(p1)):  # on construit e1 avec les éléments de p1
        if e1[1] == p1[j]:  # l'élément switch ne peut pas se retrouver 2 fois dans e1
            continue
        else:
            e1.append(p1[j])
    enfants.append(e1)
    # enfant 2
    e2.append(p1[-1])
    for j in range(2, len(p2)):
        if e2[1] == p2[j]:
            continue
        else:
            e2.append(p2[j])
    enfants.append(e2)
    # print("p1 : " + str(p1) + "\n" + "p2 : " + str(p2) + "\n" + "e1 : " + str(e1) + "\n" + "e2 : " + str(e2) + "\n")
    return enfants


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
    # on coupe avant à la fin du plus petit parent pour être sûr d'avoir un mélange génétique (sinon pas d'intérêt de croiser)
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


#############
# Sélection #
#############
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
        proba.append((1/popu[i].Cost)/s)  # 1/popu[i] car on veut prendre le plus petit
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
    T = 800  # Taille de la population
    G = 100  # Nombre maximal de génération
    # Pc = random.uniform(0.5, 0.9)  # Probabilité de croisement
    # Pm = random.uniform(0.05, 0.1)  # Probabilité de mutation
    Pc = 0.8
    Pm = 0.8
    L = int(N * 1)  # Taille de RING min pour les individus de grande taille
    if L == N:
        L -= 1  # pour les fct initiate
    NL = int(T * 0.5)  # Nombre d'individus de GT à ajouter
    best = []  # Tableau du meilleur individu pour chaque génération

    # Initialisation
    Population = []
    for i in range(T):
        RING, STAR = initiaterandom(N)
        c, PEER = evaluate(RING, STAR, Cr, Ca)
        Population.append(Individu(RING, STAR, PEER, c))

    for g in range(G):  # G générations se succèdent
        print("\n" + "Generation : " + str(g))

        # Sélection des couples
        Couple = []
        pop = [i for i in range(0, T)]  # liste des indices des individus
        for i in range(int(T/2)):
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
                #print("Pas croisement" + "\n")
                continue  # il n'y a pas de reproduction

            else:  # il y a reproduction (et donc croisement des caractéristiques)
                p1 = Couple[i][0].RING
                p2 = Couple[i][1].RING
                if len(p1) == 1 or len(p2) == 1:  # si l'indidividu est de taille 1, on ne croise pas
                    continue  # équivalent à continue si on était dans la loop
                else:
                    e1, e2 = croisement_1pt(p1, p2)
                    Enfant.append(e1)
                    Enfant.append(e2)

        # Permutation
        for i in range(len(Enfant)):
            chance = random.random()
            if chance > Pm:
                continue  # il n'y a pas de mutation
            else:  # il y a mutation chez l'enfant
                if len(Enfant[i]) < 3:  # si Enfant est de taille 2, on ne permute pas car 1 toujours en 1ère place
                    continue
                else:
                    n = random.randint(1, len(Enfant[i]) - 2)  # indice du somment à permuter (pas 0 et pas dernier)
                    Enfant[i][n], Enfant[i][n + 1] = Enfant[i][n + 1], Enfant[i][n]

        # Construction des individus Enfants
        for i in range(len(Enfant)):
            STAR = []
            for j in range(2, N + 1):
                if j not in Enfant[i]:
                    STAR.append(j)
            c, PEER = evaluate(Enfant[i], STAR, Cr, Ca)
            Population.append(Individu(Enfant[i], STAR, PEER, c))  # parents + enfants > T -> sélection à faire

        # Sélection d'individus
        if len(Population) == T:  # si aucun croisement n'a eu lieu à cause de Pc, il n'y a pas de sélection
            continue
        else:
            Population = selection_elitisme(T, Population)
        print("best = " + str(Population[0].Cost))


        # Ajout d'individus de grande taille
        # selon le besoin, commenter/décommenter cette partie :
        #"""
        best.append(Population[0].Cost)
        if g > 10:  # on fait minimum 10 itérations
            if (best[g-2]/best[g]) < 1.01:  # moins de 1% d'amélioration entre 3 générations
                for l in range(NL):  # on rajoute NL individus de taille L min
                    RING, STAR = initiate_GT(N, L)
                    c, PEER = evaluate(RING, STAR, Cr, Ca)
                    Population.append(Individu(RING, STAR, PEER, c))
        #print(len(Population))
        #"""

    # Affichage
    """
    print("\n" + "Individus sélectionnés")
    for i in range(T):
        print("Individu " + str(i + 1) + "\n" + "RING : " + str(Population[i].RING) + "\n" + "STAR : " + str(
            Population[i].STAR) + "\n" + "PEER : "
              + str(Population[i].PEER) + "\n" + "Cost : " + str(Population[i].Cost) + "\n")
    # """

    return Population


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
    # listeRing, listeHorsRing = initiate(N)
    listeRing, listeHorsRing = initiaterandom(N)
    #listeRing, listeHorsRing = initiate_GT(N, 40)
    cost, listeLienHorsRing = evaluate(listeRing, listeHorsRing, Cr, Ca)

    population = evolutionnaire(N, Cr, Ca)
    #print(len(population))

    #####################
    # Affichage et test #
    #####################

    #print("RING : " + str(listeRing) + "\n" + "STAR : " + str(listeHorsRing) + "\n" + "PEER : " + str(listeLienHorsRing) + "\n" + "Cost : " + str(cost))

    """
    # Test des éléments
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
    # """
