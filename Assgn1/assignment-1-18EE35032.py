import os
import re
import sys
#import timeit
from threading import Thread
#import numpy as np
#from nltk.tokenize import word_tokenize
  


def tokenize(file_loc):
    f = open(file_loc, 'rb')
    lines = [line.decode('utf-8', 'ignore') for line in f]
    words = []
    for l in lines:
        wd = re.split('[^a-zA-Z0-9]', l)
        wd = [word for word in wd if word]
        wd = [word.lower() for word in wd]
        #print(wd)
        #print(file_loc)
        words.extend(wd)
    return words


## function to add/update the count of n-gram of a particular class in class_dict dictionary
def find_ngram(class_dir,class_dict,class_name,file_name_list,start,end,ngram):
    for i in range(start,end):
        file_loc = os.path.join(class_dir,file_name_list[i])
        words = tokenize(file_loc)
        #print(words)
        for j in range(len(words)-ngram+1):#2 = 3-1
            str1 = " "
            list = []
            for k in range(ngram): #3 = n-gram
                list.append(words[j+k])
            #list.append(str(class_no))
            str1 = str1.join(list)
            if str1 in class_dict.keys():
                class_dict[str1][0]=class_dict[str1][0]+1
            else:
                class_dict[str1]=[1,class_name] 


#Use of multithreading
# function to find the salience score of ngram of a particular class
def class_ngram_fun(directory,class_name,class_dict,nthreads,k):
    class_dir = os.path.join(directory,class_name)   #location of class directory
    class_file_cnt = 0
    file_name_list = []    # list of filenames in a class
    for file_name in os.listdir(class_dir):
        class_file_cnt+=1
        file_name_list.append(file_name)

    # creating multiple threads and allocating a set of files in a class to each thread
    threads = [None]*min(nthreads,class_file_cnt) 
    size = int((class_file_cnt+len(threads)-1)/len(threads))
    for i in range(len(threads)):
        start = i*size
        if (i == (len(threads)-1)):
            end = class_file_cnt
        else:
            end = (i+1)*size
        threads[i] = Thread(target=find_ngram,args=(class_dir,class_dict,class_name,file_name_list,start,end,ngram)) 
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()
    
    # calculating salience score of ngram in a class
    for i in class_dict:
        class_dict[i][0]=float(class_dict[i][0]/class_file_cnt)

    #only top k ngram of each class can decide the final top k ngram for all classes
    # sorted_class_dict = dict(sorted(class_dict.items(), key=lambda x:x[1], reverse=True))
    # cnt = 0
    # class_dict_t={}
    # for i in sorted_class_dict:
    #     class_dict_t[i]=sorted_class_dict[i]
    #     cnt+=1
    #     if(cnt==k): #5 = k
    #         break
    # class_dict = class_dict_t
    # print(class_name)
    # print(class_dict)


    

# function to merge the salience score of ngrams from each class to ngram_dict dictionary
def all_ngram_fun(ngram_dict,class_dict):
    for i in class_dict:
        if (i in ngram_dict):
            if (class_dict[i][0]>ngram_dict[i][0]) :
                ngram_dict[i]=class_dict[i] 
        else:
            ngram_dict[i]=class_dict[i]


# function to print top k unique ngram
def print_fun(sorted_dict,k):
    cnt = 0
    print("Output in form of (ngram, class, salience score)\n")
    for i in sorted_dict:
        print("(",i,",",sorted_dict[i][1],",",round(sorted_dict[i][0],5),")")
        cnt+=1
        if(cnt==k):break





if __name__ == "__main__":
    
    
    #t0 = timeit.default_timer()
    #print(sys.argv)
    directory = sys.argv[1] #location of directory
    nthreads =  int(sys.argv[2]) #no of threads
    ngram = int(sys.argv[3]) # no of words 
    k = int(sys.argv[4]) # top k ngrams
    ngram_dict={}
    for class_name in os.listdir(directory):
        class_dict = {}
        class_ngram_fun(directory,class_name,class_dict,nthreads,k)
        all_ngram_fun(ngram_dict,class_dict) 

    # t1 = timeit.default_timer()
    # print(round(t1-t0,3))
    
    sorted_dict = dict(sorted(ngram_dict.items(), key=lambda x:x[1], reverse=True))# sorting dictionary based on salience score in descending order

    #printing top k unique ngram
    print_fun(sorted_dict,k)

