import os
import re
import sys
import random




if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Your input was wrong. Correct format: python <your-code.py> <input filename>")
    else:
        file = sys.argv[1] #location of file
        Gedges = [] # stores all the edges
        vxs = []
        f = open(file, "r")
        # f = f.readlines()
        for x in f:
            # print(x)
            if len(x.split())>1:
                a = int(x.split()[0])
                b = int(x.split()[1])
                vxs.append(a)
                vxs.append(b)
                Gedges.append([a,b])
        vxs = set(vxs)  # set of all vertices
        l = len(Gedges)
        print("hello")
        # print(l)
        # print(E)
        # print(graph[0])
        # r = random.random()
        # kMC(Gedges,l,vxs)


