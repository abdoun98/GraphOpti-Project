import random
import numpy as np

def data_extract(file):
    Cr = []  # cout du newRing
    Ca = []  # cout des liens vers newRing

    with open("Datasets/" + file + ".txt") as f:
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

        #print(Ca[1][2])
        print("fin d'extraction des donnees")

    return N, Ca, Cr

def cout_ring(ring, Cr):
    cout = 0
    print(cout)

    for i in range(0, len(ring) - 1):
        cout += Cr[ring[i]][ring[i+1]]
        print(cout)

    return cout

def cout_hors_ring(HR_liste, Ca):
    cout = 0

    for couple in HR_liste:
        cout += Ca[couple[0]][couple[1]]
        print(cout)

    return cout

def permutation(liste, a, b):

    temp = liste[a]
    liste[a] = liste[b]
    liste[b] = temp
    print("liste avec permutation :{}".format(liste))

    return liste

def remplacement(liste, a, N):

    liste[a] = random.randint(1, N)
    print("liste avec remplacement :{}".format(liste))

    return liste

def modification(liste, a, b, N):
    choix = random.randint(1, 2)

    if choix == 1:
        liste = permutation(liste, a, b)
    else:
        liste = remplacement(liste, a, N)

    return liste

if __name__ == '__main__':
    """
    #test
    N, Ca, Cr = data_extract("data1")

    sol = [random.randint(1, N) for i in range(0, 4)]
    cout_sol = cout_ring(sol, Cr)

    sol_bis = modification(sol, 1, 2, Cr)
    cout_sol_bis = cout_ring(sol_bis, Cr)

    print("sol :{}\ncout sol :{}\n".format(sol, cout_sol))
    print("sol bis :{}\ncout sol bis :{}\n".format(sol_bis, cout_sol_bis))
    print("fin")
    """

    taille_ring = 4
    history = []
    history_cout = []

    Tc = 100
    Tf = 0.01
    palier = 10
    coeff = 0.99

    N, Ca, Cr = data_extract("data1")

    sol = [random.randint(1, N) for i in range(0, taille_ring)]
    cout_sol = cout_ring(sol, Cr)
    history.append(sol)
    history_cout.append(cout_sol)

    while True:

        cpt = 1
        while True:
            sol_bis = modification(sol, random.randint(0, taille_ring) - 1, random.randint(0, taille_ring) - 1, N)
            cout_sol_bis = cout_ring(sol_bis, Cr)

            dE = cout_sol_bis - cout_sol

            if dE <= 0:
                sol = sol_bis
                cout_sol = cout_sol_bis
                history.append(sol)
                history_cout.append(cout_sol)

            elif dE > 0 and Tc != 0:
                P = np.exp(-dE/Tc)
                x = random.random()

                if x <= P:
                    sol = sol_bis
                    cout_sol = cout_sol_bis
                    history.append(sol)
                    history_cout.append(cout_sol)

            cpt += 1
            if cpt == palier:
                break

        Tc = coeff * Tc
        if Tc <= Tf:
            break
    print("sol :{}\n cout sol :{}\n".format(sol, cout_sol))
    print("fin")