
if __name__ == '__main__':
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

    RING = []
    STAR = []
    costr = 0
    costa = 0
    #élément du RING
    A = N-10 #nbre d'élément dans le RING
    for i in range(A):
        RING.append(i+1)

    #coût du RING
    for i in range(A-1):
        costr += Cr[RING[i]-1][RING[i+1]-1]
        #print(str(i) + " " + str(Cr[RING[i]-1][RING[i+1]-1]))

    #element dans STAR
    for i in range(1,N+1):
        #print(i)
        if i in RING:
            continue
        else:
            STAR.append(i)


    #coût de STAR
    PEER = []
    for e in STAR:
        cmin = Cr[e-1][0]
        i_min = 0
        for i in range(N):
            if Cr[e-1][i] == 0:
                continue
            elif Cr[e-1][i] < cmin:
                cmin = Cr[e-1][i]
                i_min  = i+1
        PEER.append([e,i_min])
        costa += cmin

    cost = costr + costa



    print("end")

