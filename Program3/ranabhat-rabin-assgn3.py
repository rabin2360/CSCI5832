#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 3 - Viterbi

import sys
import math
import csv

#calculates probability given the count dictionary, tag counts and the index of the key
def calculateProbability(countDict, tagCounts, keyIndex):
    #contains the probability for the tag-word association
    probabilityDict = dict()

    #computes the probability for likelihood of word-tag association
    for key, values in countDict.items():
        #tag key
        tagKey = key[keyIndex]
        probabilityDict[key] = countDict[key]/tagCounts[tagKey]

    ######################DEBUG####################
    for key, value in probabilityDict.items():
        print(key, value)
    ######################END#####################

    return probabilityDict

def count(dictionary, key):

    #tags count
    if dictionary.get(key) == None:
        dictionary[key] = 1
    else:
        dictionary[key] += 1
            
    return dictionary

def parseInputFile(inputFileName):
    #contains the combination of (words, tag) to determine likelihood probs
    likelihoodCount = dict()
    #contains the combination of (tagN-1, tagN) to determine observation probs
    observationCount = dict()

    #dictionaries for likelihood and observation
    likelihoodProbs = dict()
    observationProbs = dict()
    
    #needed values for likelihood and observations probs
    tagsDict = dict()
    #storing the tags and words sequences as in the input file
    tagsList = []
    wordsList = []

    #constants needed to determine the probability
    CONST_OBSERVATION_KEY_LOCATION = 0
    CONST_TRANSITION_KEY_LOCATION = 1
    
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
            wordsList.append(word)

            #counting the tags
            tagsDict = count(tagsDict, tag)

            #likelihood count
            alias = (word, tag)
            likelihoodCount = count(likelihoodCount, alias)

    #iterate to only N-1 elements in the list
    #get the bigrams for tags, it works as the count for observation probs
    for i in range(0,len(tagsList)-1):
        alias = (tagsList[i], tagsList[i+1])
        
        #observation count
        observationCount = count(observationCount, alias)

    #Probabilities - transition and likelihood
    likelihoodProbs = calculateProbability(likelihoodCount, tagsDict, CONST_TRANSITION_KEY_LOCATION)
    observationProbs = calculateProbability(observationCount, tagsDict, CONST_OBSERVATION_KEY_LOCATION)

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
