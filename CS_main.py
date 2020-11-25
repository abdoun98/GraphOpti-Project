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
    j = random.randrange(len(ring))
    while i==j:
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

def permOutOfRing(ring, star, link):
    #print("ping permOutOfRing")
    i = random.randrange(len(ring))
    elem = ring[i]
   # print(elem)
    del ring[i]

    for i, j in enumerate(link):
        if elem == j:
            link[i] = ring[random.randrange(len(ring))]

    star.append(elem)
    j = random.randrange(len(ring))
    link.append(ring[j])
    return ring, star, link
def permIntoRing(ring, star, link):
    #print("ping permIntoRing")
    i = random.randrange(len(star))
    elem = star[i]
    del star[i]
    del link[i]
    ring.append(elem)
    return ring, star, link

def createMovement(ring, star, link):
    select = random.randrange(4)
    if select == 0:
        if len(ring) <= 2:
            createMovement(ring, star, link)
        else:
            ring = permRing(ring)
    elif select == 1:
        if len(star) <= 2:
            createMovement(ring, star, link)
        else:
            link = permStar(ring, link)
    elif select == 2:
        if len(ring) <= 1:
            createMovement(ring, star, link)
        else:
            ring, star, link = permOutOfRing(ring, star, link)
    else:
        if len(star) <= 0:
            createMovement(ring,star,link)
        else:
            ring, star, link = permIntoRing(ring, star, link)

    return ring, star, link

def randomSolution(nbr):
    ringRndTreshold = 0.5
    listOfPoint = list(range(1, nbr+1))

    random.shuffle(listOfPoint)
    ring = []
    while len(ring) ==0:
        for i, elem in enumerate(listOfPoint):
            if random.random() <= ringRndTreshold:
                ring.append(elem)
                del listOfPoint[i]
    star = listOfPoint
    link = []
    for i in star:
        link.append(random.choice(ring))
    return ring, star, link

def recuit(Cr, Ca):
    nbrItr = 10

    size = len(Cr[0])
    ring, star, link = randomSolution(size)
    t = 100
    tf = 0.01
    N = 0.9
    currentScore = getScore(Cr, Ca, ring, star, link)

    while t > tf:
        for i in range(nbrItr):
            newRing, newStar, newLink = createMovement(ring, star, link)
            newScore = getScore(Cr, Ca, newRing, newStar, newLink)
            if newScore > currentScore:
                currentScore = newScore
                ring = newRing
                star = newStar
                link = newLink
            else:
                P = math.exp((newScore-currentScore)/t)
                if P >=random.random():
                    currentScore = newScore
                    ring = newRing
                    star = newStar
                    link = newLink
            print(ring, star, link, currentScore, t)
        if t > tf:
            t = t * N
    return ring, star, link


if __name__ == '__main__':
    Cr = []  # cout du ring
    Ca = []  # cout des liens vers ring

    with open("Datasets/test.txt") as f:
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
    print(getScore(Cr,Ca,ring,star, link))
