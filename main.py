# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

def dataExtract(file):
    Cr = []  # cout du ring
    Ca = []  # cout des liens vers ring

    with open("Datasets/" + file + ".txt") as f:
        data = f.readline()
        data = data.split()
        data = list(map(int, data))
        N = data[0]  # Nombre de sommets du problème
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
        print("fin d'extraction des donnees")

    return N, Ca, Cr

def writeOutput(file, listRing, listHorsRing, cout):
    with open("Outputs/output-" + file + ".txt", "w") as f:
        f.write("RING {}\n".format(len(listRing)))
        for elem in listRing:
            f.write("{} ".format(elem))
        f.write("\nSTAR")
        for elem in listHorsRing:
            f.write("\n{} {}".format(elem[0], elem[1]))
        f.write("\nCOST {}".format(cout))

if __name__ == '__main__':

    file = "data1"
    a = [1,4,5,2]
    b = [[7,4],[8,5],[9,5],[6,2],[3,2]]
    c = 9

    writeOutput(file, a, b, c)
    print("fin")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/



