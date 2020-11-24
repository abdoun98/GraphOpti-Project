Cr = [] #cout du ring
Ca = [] #cout des liens vers ring

with open("Datasets/data1.txt") as f:
    data = f.readline()
    data = data.split()
    data = list(map(int, data))
    N = data[0] #Nombre de sommets du problème
    print(N)


    for i in range (N):
        sommet = f.readline()
        sommet = sommet.split()
        sommet = list(map(int,sommet))
        Cr.append(sommet)

    for j in range(N):
        sommet2 = f.readline()
        sommet2 = sommet2.split()
        sommet2 = list(map(int,sommet2))
        Ca.append(sommet2)

    print(Ca[1][2])
    print("fin d'extraction des donnees")