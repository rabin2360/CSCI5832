#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 3 - Viterbi

import sys
import math
import csv
import re

tagsList = []
wordsList = []


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
    #printDict(probabilityDict)
    ######################END#####################

    return probabilityDict

#if element is not present in the dictionary, initiates the count to 1,
#otherwise, the count is incremented
def count(dictionary, key):

    if dictionary.get(key) == None:
        dictionary[key] = 1
    else:
        dictionary[key] += 1
            
    return dictionary

def parseInputFile(trainingCorpusList):
    #contains the combination of (words, tag) to determine likelihood probs
    observationCount = dict()
    #contains the combination of (tagN-1, tagN) to determine observation probs
    transitionCount = dict()

    #dictionaries for transition and observation
    observationProbs = dict()
    transitionProbs = dict()
    
    #needed values for transition and observations probs
    tagsDict = dict()
    #storing the tags and words sequences as in the input file
    global tagsList
    global wordsList

    #constants needed to determine the probability
    CONST_OBSERVATION_KEY_LOCATION = 0
    CONST_TRANSITION_KEY_LOCATION = 1
    
    #determines the observation count
    #also determines the count of unique tags in the corpus
    for i in range(0, len(trainingCorpusList)):
        lineValues = trainingCorpusList[i].split("\t")
        
        #for word,tag in lineValues:
        #tags list - preserves the order, needed for transition probs
        tagsList.append(lineValues[1])
        wordsList.append(lineValues[0])

        #counting the tags
        tagsDict = count(tagsDict, lineValues[1])

        #observation likelihood count
        alias = (lineValues[0], lineValues[1])
        observationCount = count(observationCount, alias)

    #iterate to only N-1 elements in the list
    #get the bigrams for tags, it works as the count for transition probs
    for i in range(0,len(tagsList)-1):
        alias = (tagsList[i], tagsList[i+1])
        
        #transition count
        transitionCount = count(transitionCount, alias)

    #Probabilities - transition and likelihood
    observationProbs = calculateProbability(observationCount, tagsDict, CONST_TRANSITION_KEY_LOCATION)
    transitionProbs = calculateProbability(transitionCount, tagsDict, CONST_OBSERVATION_KEY_LOCATION)

    #############DEBUGGING##########################   
    #print(tagsList)
    #printDict(observationCount)
    #printDict(likelihoodCount)
    
    #printing the list - testing purposes
    #for p in content:
    #    print(p)
    #############END###############################

    return observationProbs, transitionProbs, transitionCount, observationCount

def printDict(dict):
    for key, value in dict.items():
        print (key, value)
    
def main():
    #check input vector to see what the user is supplying
    if (len(sys.argv) != 2):
        print("Not enough arguments- argument format <python file><inputfile>\n")
        sys.exit()

    totalSentences = 0
    temp = 0
    count = 0
    
    trainingCorpus = []
    testCorpus = []
    content = []
    
    #80-20 split
    with open(sys.argv[1]) as input:
        content = [line.rstrip() for line in open(sys.argv[1])]
        #ignore blank lines
        content = list(line for line in content if line)

        #count the periods in the corpus
        for line in input:
            #finding period in the input read
            temp = len(re.findall('\.', line))
            totalSentences = temp + totalSentences
            #content = input.readlines()

    splitLimit = (math.floor(0.8*totalSentences)/2)

    if(splitLimit%2 != 0):
        splitLimit +=1
    
    #print("count", totalSentences)
    #print("0.8 percent", splitLimit)
    #print(content)

    contentDivider = 0

    #dividing the input between training and test corpus
    for i in range(0,len(content)):
        temp = len(re.findall('\.', content[i]))
        contentDivider = contentDivider + temp
        
        if(contentDivider <=  splitLimit):
            trainingCorpus.append(content[i])
        else:
            testCorpus.append(content[i]) 


    #fixing some of the kinks in the divide
    trainingCorpus.append(testCorpus[0])
    testCorpus = testCorpus[1:]
    
    #print("training corpus:")
    #print(trainingCorpus)

    #print("test corpus:")
    #print(testCorpus)
    
    #training 
    observationProbsMatrix = dict()
    transitionProbsMatrix = dict()
    transitionCount = dict()
    observationCount = dict()
    observationProbsMatrix, transitionProbsMatrix, transitionCount, observationCount = parseInputFile(trainingCorpus)
    #read the file and create two dictionaries - tags and words (bigrams)

    #printDict(observationProbsMatrix)
    #printDict(transitionProbsMatrix)
    #printDict(observationCount)
    
    #test
    testSentences = returnList(testCorpus, 0)
    #print(testSentences)

    #determines new words
    #for i in range(0, len(testSentences)):
    #    if(newWord(observationCount, testSentences[i])):
    #       print("new word",testSentences[i])
           #need to do something with words that are not part of the training corpus
    #transition smoothing
    #if(tagSequence(transitionCount, ("JJ", "."))):
    #    print ("has it")
    #else:
    #    print("Nope")
    
    #sending the input sentences one at a time to send it to viterbi
    testSentence = []
        
    for i in range(0, len(testSentences)):
        if(testSentences[i] == "."):
            Viterbi(testSentence, observationProbsMatrix, transitionProbsMatrix)
            testSentence = []
        else:
            testSentence.append(testSentences[i])

                
def Viterbi(sentence, observationProbsMatrix, transitionProbsMatrix):
    bestPath = []

    #print(sentence)
    #print("\n")

    #...........put viterbi code here

    
    return bestPath
    
#determines if the tag sequence is in the transition probability key list. Returns TRUE if in the list or false otherwise
def tagSequence(tagsListDict, inputTagSet):
    hasTagSequence = False

    for key, value in tagsListDict.items():
        if(key[0] == inputTagSet[0] and key[1] == inputTagSet[1]):
            hasTagSequence = True
            break

    return hasTagSequence

#takes the tab delimited list input and returns the values that are mandated by the index location
def returnList(inputList, index):
    returnList = []
    
    for i in range(0, len(inputList)):
        lineValues = inputList[i].split("\t")
        returnList.append(lineValues[index])

    return returnList

#identifies if a word in the test corpus is a new one
def newWord(wordsListDict, inputWord):
    hasNewWord = True

    for key, value in wordsListDict.items():
        if (key[0] == inputWord):
            hasNewWord = False
            break
        
    return hasNewWord

#makes the main method the default method
if __name__=="__main__":
    main()
