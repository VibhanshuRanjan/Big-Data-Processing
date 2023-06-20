import os
import re
import sys
import random



def find_Set(v, pset):
    # path compression
    if v == pset[v]:
        return v
    pset[v]=find_Set(pset[v], pset)
    return pset[v]
    # if pset[v] != v:
    #     pset[v] = find_Set(pset[v], pset)
    # return pset[v]


def find_Union(v1, v2, pset, rank):
    v1s = find_Set(v1, pset)
    v2s = find_Set(v2, pset)
    # Connect a lower rank tree to the high rank tree's root (Union by Rank)
    if v1s != v2s:
        if rank[v1s] < rank[v2s]:
            t=v1s
            v1s=v2s
            v2s=t
        pset[v2s] = v1s
        # Make one the root and raise its rank by one if the rankings are equal.
        if rank[v1s] == rank[v2s]:
            rank[v1s] = rank[v1s]+1


def kMC(Gedges,l,vxs):
    Vt = max(vxs) + 1
    Va = len(vxs)
    #print(Vt,Va)
    pset = []  # parents for union-find
    rank = []  # rank of each subset
    for v in range(Vt):
        #print(v)
        pset.append(v)
        rank.append(0)
    vx = Va #total no of vertices
    while vx > 2:
        i = (random.randint(0,10*l))%l
        #find sets of two corners of current edge
        p1 = find_Set(Gedges[i][0],pset)
        p2 = find_Set(Gedges[i][1],pset)
        if p1 == p2:
            continue
        else:
            # print("Edge to remove " + str(graph[i][0]) + "-" + str(graph[i][1]))
            vx -= 1
            find_Union(p1, p2, pset, rank)
    ces_edges = []
    for i in range(l):
        v1s = find_Set(Gedges[i][0],pset)
        v2s = find_Set(Gedges[i][1],pset)
        if v1s != v2s:
            ces_edges.append(i)
    ces = len(ces_edges)
    print("No. of cut found by Kargers minCut algorithm is", ces)
    print("Communities that we get after removing the mincut edges: First column is node value and second column is community id(1 or 2)")
    t = find_Set(list(vxs)[0],pset)
    for i in vxs:
        print(f"{i} 1" if find_Set(i,pset) == t else f"{i} 2")




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
        # print(l)
        # print(E)
        # print(graph[0])
        # r = random.random()
        kMC(Gedges,l,vxs)


