#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 3 - Viterbi

import sys
import math
import csv

def likelihoodProbs():
    print("I am likelihood probs evaluator\n")

def transitionProbs():
    print("I am transition probs evaluator\n")

def parseInputFile(inputFileName):
    #contains the combination of (words, tag) to determine likelihood probs
    likelihoodCount = dict()
    #contains the combination of (tagN-1, tagN) to determine observation probs
    observationCount = dict()

    #needed values for likelihood and observations probs
    tagsDict = dict()
    tagsList = []
    
    with open(inputFileName) as input:
        content = [line.rstrip() for line in open(inputFileName)]
        #ignore blank lines
        content = list(line for line in content if line)

        #determines the likelihood count
        #also determines the count of unique tags in the corpus
        lineValues = csv.reader(content, delimiter='\t')
        for word,tag in lineValues:
            #tags list - preserves the order, needed for transition probs
            tagsList.append(tag)
            
            #tags count
            if tagsDict.get(tag) == None:
                tagsDict[tag] = 1
            else:
                tagsDict[tag] += 1
            
            alias = (word, tag)
            #likelihood dictionary count
            if  likelihoodCount.get(alias) == None:
               likelihoodCount[alias] = 1
            else:
               likelihoodCount[alias] += 1

    #iterate to only N-1 elements in the list
    #get the bigrams for tags, it works as the count for observation probs
    for i in range(0,len(tagsList)-1):
        alias = (tagsList[i], tagsList[i+1])

        if observationCount.get(alias) == None:
            observationCount[alias] = 1
        else:
            observationCount[alias] += 1
        
        #print(alias)

    #############DEBUGGING##########################   
    #print(tagsList)

    #for key, value in observationCount.items():
    #    print (key, value)
    
    #for key, value in likelihoodCount.items():
    #    print (key, value)
    
    #printing the list - testing purposes
    #for p in content:
    #    print(p)
    #############END###############################
    
def main():
    #check input vector to see what the user is supplying
    if (len(sys.argv) != 2):
        print("Not enough arguments- argument format <python file><inputfile>\n")
        sys.exit()
        
    parseInputFile(sys.argv[1])
    #read the file and create two dictionaries - tags and words (bigrams)

#makes the main method the default method
if __name__=="__main__":
    main()
