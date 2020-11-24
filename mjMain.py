import math
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

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


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def permuteRing(listeRing, i):
    listeRing[i], listeRing[i - 1] = listeRing[i - 1], listeRing[i]

def entreRing(listeRing,listeHorsRing,listeLienHorsRing,i,j):
    listeRing=listeRing[:j]+[listeHorsRing[i]]+listeRing[j:]
    listeHorsRing=listeHorsRing[:i]+listeHorsRing[i+1:]
    listeLienHorsRing=listeLienHorsRing[:i]+listeLienHorsRing[i+1:]
    attributSommetRing(listeRing,listeHorsRing,listeLienHorsRing)

def attributSommetRing(listeRing,listeHorsRing,listeLienHorsRing):
    for i in len(listeHorsRing):
        m=math.inf
        s=-1
        for j in len(listeRing):
            if m>Ca[i][j]:
                m=Ca[i][j]
                s=j
        listeLienHorsRing[i]=s