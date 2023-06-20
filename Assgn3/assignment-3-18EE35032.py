import os
import re
import sys
import math
import random
from pyspark import SparkConf, SparkContext

def preprocessing(line,sw):
    line = set([word.lower() for word in re.split('[^a-zA-Z]',line) if word.lower() not in sw and word])
    # if len(line)==0:
    #     print("Set is empty")
    # print(line)
    # line = set([word.lower() for word in line if not any(c.isdigit() for c in word)])
    # line = [word for word in line if word not in sw and word]
    # print(line)
    return line

# for finding P(w1)
def psi_fun(line):
    return [(word,1) for word in line]

# for finding P(w1,query-word)
def pmi_fun(line,qw):
    if qw in line:
        return [(word, 1) for word in line]
    return [(word, 0) for word in line]

# formula for PMI scores
def formula(w,N,psi_qw):
    epsilon = 1e-10
    res = math.log2(epsilon+w[1][0]*N/(w[1][1]*psi_qw))
    # assert isinstance(res,float)
    # assert isinstance(w[0],str)
    return (w[0],(res,w[1][0]))

def comp(x):
    return x[1][0],x[0]

if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("Test")
    sc = SparkContext(conf=conf)

    file_loc = sys.argv[1] # location of file
    qw = sys.argv[2] # query-word
    k = int(sys.argv[3]) # no of top K words
    sw_loc = sys.argv[4] # location of stopword file

    with open(sw_loc, "r") as f:
        sw = f.readlines()
    # sw = f.readlines()
    # print("Stopwords", sw[0:10])
    sw=[word.replace("\n","") for word in sw]
    # print("Stopwords", sw[0:10])
    lines = sc.textFile(file_loc)
    # print(lines.collect())
    lines_p = lines.map(lambda line: preprocessing(line,sw))
    N =  lines_p.map(lambda line:1 if len(line)>0 else 0).reduce(lambda x,y:x+y)
    # print("printing n",N)
    psi =  lines_p.flatMap(lambda line : psi_fun(line)).reduceByKey(lambda x,y:x+y)
    # print("printing psi",psi)
    if len(psi.lookup(qw))==0 :
        print("-------------------------Query words itself not found in any document. Please enter any other query word---------------------------")

    # print("printing psi_qwklsdddddddddddddddddddddddddddddddddddddddddddd",psi_qw)

    else:
        # print(psi_qw)
        # print("lkdslkslkdslkdlskdklsdlksdlskdlskdlsdlkslk")
        psi_qw = psi.lookup(qw)[0]
        pmi =  lines_p.flatMap(lambda line : pmi_fun(line,qw)).reduceByKey(lambda x,y:x+y)
        # print(pmi)
        positive_pmi = pmi.join(psi).map(lambda w: formula(w,N,psi_qw))
        positive_pmi = positive_pmi.filter(lambda x: x[1][1]!=0)
        negative_pmi = positive_pmi.map(lambda x: (x[0],(-1*x[1][0],x[1][1])))
        # print(pos_pmi.collect())
        positive_words = positive_pmi.top(k,key = comp)
        print("---------------------------Top",k,"positively associated words---------------------------")
        for i in range(k):
            print(positive_words[i][0],"      ",positive_words[i][1][0])
        negative_words = negative_pmi.top(k,key = comp)
        print("---------------------------Top", k, "negatively associated words---------------------------")
        for i in range(k):
            print(negative_words[i][0], "      ", -1*negative_words[i][1][0])

        # neg_pmi =

    # print("These are the lines "+lines.collect()[0])
    # print(sys.argv,sw)

