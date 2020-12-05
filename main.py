# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
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

    with open("outputC", 'w') as f:
        for x in Ca:
            f.write(str(x) + "\n")

    print("asa")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/



