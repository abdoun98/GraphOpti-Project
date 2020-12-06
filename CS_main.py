import random
import math

def getScore(Cr, Ca, ring, star, link):
    score = 0
    for i, elem in enumerate(ring):
        cr = Cr[ring[i]-1][ring[(i+1)%len(ring)]-1]
        score += cr

    for i, elem in enumerate(star):
        ca = Ca[star[i]-1][link[i]-1]
        score += ca
    return score


def createExample():
    ring = [1, 4, 5, 2]
    star = [3, 6, 7, 8, 9]
    link = [2, 2, 4, 5, 5]
    return star, ring, link

def permRing(ring):
    #print("ping permRing")
    i = random.randrange(len(ring))
    while i == 0:
        i = random.randrange(len(ring))
    j = random.randrange(len(ring))
    while i==j or j==0:
        j = random.randrange(len(ring))
    tmp = ring[i]
    ring[i] = ring[j]
    ring[j] = tmp
    return ring

def permStar(ring, link): #Comme mael a bien dit: on peut améliorer ca car on peut toujours trouver un minimum
    #print("ping permStar")
    i = random.randrange(len(link))
    j = random.randrange(len(ring))
    link[i] = ring[j]
    return link



def permOutOfRing(ring, star, link, Ca):
    #print("ping permOutOfRing")
    i = random.randrange(len(ring))
    while i == 0:
        i = random.randrange(len(ring))
    elem = ring[i]
    # print(elem)
    del ring[i]

    for i, j in enumerate(link):
        if elem == j:
            minimum = min([j for i, j in enumerate(Ca[elem - 1]) if i + 1 in ring])
            minPos = Ca[elem - 1].index(minimum) + 1
            link[i] = minPos

    star.append(elem)
    #j = random.randrange(len(ring))
    minimum = min([j for i, j in enumerate(Ca[elem-1]) if i + 1 in ring])
    minPos = Ca[elem-1].index(minimum)+1
    link.append(minPos)

    return ring, star, link
def permIntoRing(ring, star, link):
    #print("ping permIntoRing")
    i = random.randrange(len(star))
    elem = star[i]
    del star[i]
    del link[i]
    ring.append(elem)
    return ring, star, link

def createMovement(ring, star, link, Ca):
    newRing = ring[:]
    newStar = star[:]
    newLink = link[:]
    select = random.randrange(3)
    if select == 0:
        if len(newRing) <= 2:
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing = permRing(newRing)
            '''
    elif select == 1:
        if len(star) <= 2:
            createMovement(ring, star, link)
        else:
            link = permStar(ring, link)
            '''
    elif select == 1:
        if len(newRing) <= 1:
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing, newStar, newLink = permOutOfRing(newRing, newStar, newLink, Ca)
    else:
        if len(newStar) <= 0:
            createMovement(newRing, newStar, newLink, Ca)
        else:
            newRing, newStar, newLink = permIntoRing(newRing, newStar, newLink)

    return newRing, newStar, newLink

def randomSolution(nbr, Ca):
    ringRndTreshold = 0.5
    listOfPoint = list(range(2, nbr+1))

    random.shuffle(listOfPoint)
    ring = [1]

    while len(ring) ==0:
        for i, elem in enumerate(listOfPoint):
            if random.random() <= ringRndTreshold:
                ring.append(elem)
                del listOfPoint[i]

    star = listOfPoint
    link = []
    for elem in star:
        #print(ring)
        #print(Ca[elem-1])
        #print([j for i, j in enumerate(Ca[elem-1]) if i + 1 in ring])
        minimum = min([j for i, j in enumerate(Ca[elem-1]) if i + 1 in ring])
        minPos = Ca[elem-1].index(minimum) + 1
        link.append(minPos)
    return ring, star, link

#Prérecuit appelé dans recuit2()
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

def recuit(Cr, Ca, beginRing = None, beginStar = None, beginLink = None):
    nbrItr = 100000

    size = len(Cr[0])
    if beginRing == None or beginStar == None or beginLink == None:
        ring, star, link = randomSolution(size, Ca)
    else:
        ring = beginRing[:]
        star = beginStar[:]
        link = beginLink[:]
    t = 1000000
    tf = 1
    N = 0.9
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
                if (newScore-currentScore)/t < -20:
                    P = 0
                else:
                    P = math.exp((currentScore-newScore)/t)
                if P >=random.random():
                    currentScore = newScore
                    ring = newRing
                    star = newStar
                    link = newLink

        print(ring, star, link, currentScore, t)
        if t > tf:
            t = t * N
    return ring, star, link

#Recuit simulé adapté à l'algo évolutionnaire
def recuit2(Cr, Ca, ring):
    nbrItr = 100

    t = 1000000
    tf = 1
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
                if (newScore-currentScore)/t < -20:
                    P = 0
                else:
                    P = math.exp((currentScore-newScore)/t)
                if P >=random.random():
                    currentScore = newScore
                    ring = newRing
                    star = newStar
                    link = newLink

        #print(ring, star, link, currentScore, t)
        if t > tf:
            t = t * N
    return ring

"""
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

    ring, star, link = recuit(Cr, Ca)
    print("---------------------")
    print("RING = {}".format(ring))
    print("STAR = {}".format(star))
    print("LINK =")
    for i, j in enumerate(link):
        print([star[i], j])
        
    #print("SCORE = {}".format(getScore(Cr,Ca,ring,star, link)))
"""