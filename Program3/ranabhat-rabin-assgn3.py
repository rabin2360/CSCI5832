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
        #ignore the start tags
        if lineValues[0] != '<start>':
            #print(lineValues[1])
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
    if (len(sys.argv) != 3):
        print("Not enough arguments- argument format <python file><trainingfile><testFile>\n")
        sys.exit()

    totalSentences = 0
    temp = 0
    count = 0
    
    trainingCorpus = []
    testCorpus = []
    content = []
    masterList = []
    masterList.append("<start>\tST")

    #training corpus
    with open(sys.argv[1]) as input:
        content = [line.rstrip() for line in open(sys.argv[1])]
        
    #adding start tag whereve there is an empty line
    for i in range(0, len(content)):
        if(content[i] ==""):
            content[i] = "<start>\tST"
                        
    masterList.extend(content)

    #training 
    observationProbsMatrix = dict()
    transitionProbsMatrix = dict()
    transitionCount = dict()
    observationCount = dict()
    observationProbsMatrix, transitionProbsMatrix, transitionCount, observationCount = parseInputFile(masterList)

    #read the file and create two dictionaries - tags and words (bigrams)

    #(word, tag)
    #printDict(observationProbsMatrix)
    #printDict(transitionProbsMatrix)
    #printDict(observationCount)
    
    #test file

    masterList = []
    masterList.append("<start>\tST")

    #training corpus
    with open(sys.argv[2]) as input:
        content = [line.rstrip() for line in open(sys.argv[2])]
        
    #adding start tag whereve there is an empty line
    for i in range(0, len(content)):
        if(content[i] ==""):
            content[i] = "<start>\tST"
               
    masterList.extend(content)
    
    observationSeqs = returnList(masterList, 0)
    #print(observationSeqs)

    #sending the input sentences one at a time to send it to viterbi
    observationSeq = []

    #write to a file
    file = open("outputFile.txt", "w+")
    backtrace = []
    tagSeq =  []
    
    for i in range(0, len(observationSeqs)):
        if(observationSeqs[i] == "."):
            observationSeq.append(observationSeqs[i])
            backtrace, tagSeq = Viterbi(observationSeq, observationProbsMatrix, transitionProbsMatrix)

            for i in range(1, len(backtrace)):
                #get tags
                #print(backtrace[i][0],",",backtrace[i][1])

                word = observationSeq[backtrace[i][1]]
                tag = tagSeq[backtrace[i][0]]

                print(word,", ", tag)
                file.write(word+"\t"+tag+"\n")

            file.write("\n")
            
            #reset the current sentence buffer after sending the sentence to be viterbi evaluated
            observationSeq = []
        else:
            observationSeq.append(observationSeqs[i])

    file.close()
    
def Viterbi(sentence, observationProbsMatrix, transitionProbsMatrix):

    print()
    bestPath = []
    tagsDict = dict()

    #create dictionary of tags
    for i in range(0, len(tagsList)):
        tagsDict = count(tagsDict, tagsList[i])

    #tag Sequeunce
    tagSeq = []
    for tag, value in tagsDict.items():
        #print(tag)
        tagSeq.append(tag)

    #print(tagSeq)

    #[column][row]
    viterbiMatrix = [[0 for col in range(len(sentence))] for row in range(len(tagsDict))]

    #initialization array
    initializeArray = dict()

    #for all the tags in the tagsDict, calculate P(ST,tags)
    for key, value in tagsDict.items():
        alias = ("ST", key)

        #elements are in the transition matrix
        if transitionProbsMatrix.get(alias) != None:
            #print(alias, ":", transitionProbsMatrix.get(alias))
            initializeArray[alias] = transitionProbsMatrix.get(alias)
        else:
            initializeArray[alias] = 1/(len(tagsDict)*len(tagsDict))
            #print(alias, ": Not in the matrix", 1/len(tagsDict))

    #print(initializeArray)
    #print(len(sentence))
    #print(len(tagSeq))

    maxValue = 0
    
    #values for the first column in the Viterbi matrix
    for row in range(0, len(tagSeq)):

        #transition probability
        tag = tagSeq[row]
        alias = ("ST", tag)
        transitionProb = initializeArray.get(alias)
        #print(alias, ": ", transitionProb)

        #observation probability
        word = sentence[0]
        alias = (word, tag)
        #newWord = True

        #determine if the observation sequence is in the matrix
        #if not then estimate a probability
        #if it is in the matrix then get the probability
        if observationProbsMatrix.get(alias) == None:
            #print("None: ", alias)
            observationProb = 1/(len(tagsDict)*len(tagsDict))
        else:
            #print("ALIAS:",  alias)
            observationProb = observationProbsMatrix.get(alias)

        #print(observationProb)
        viterbiMatrix[row][0] = observationProb * transitionProb

        #keeping track of maxValue in the first column in the viterbi matrix
        if maxValue < viterbiMatrix[row][0]:
            maxValue = viterbiMatrix[row][0]

    transitionVal = 0

    #rest of the viterbi matrix

    #for each word
    for col in range(1, len(sentence)):

        #for all the tags
        for row in range(0, len(tagSeq)):
            
            #print(sentence[col], ", ", tagSeq[row])

            #transition probability
            transitionVal = 0
            maxValue = 0

            #observation probability
            alias = (sentence[col], tagSeq[row])
            #print(alias)

            if observationProbsMatrix.get(alias) != None:
                observationProb = observationProbsMatrix.get(alias)
            else:
                observationProb = 1/(len(tagsDict)*len(tagsDict))

            
            for previousRow in range(0, len(tagSeq)):
                alias = (tagSeq[previousRow], tagSeq[row])
                
                if transitionProbsMatrix.get(alias) != None:
                    #print(alias, ":", transitionProbsMatrix.get(alias))
                    transitionVal = transitionProbsMatrix.get(alias)
                else:
                    transitionVal = 1/(len(tagsDict)*len(tagsDict))
                    #print(alias, ": Not in the matrix", 1/len(tagsDict))

                value = viterbiMatrix[previousRow][col-1]
                value  = value * transitionVal * observationProb
                #print(value)
                if maxValue < value:
                    #print(maxValue)
                    maxValue = value
            
            viterbiMatrix[row][col] = maxValue

        #rest of the viterbi matrix
                
    #print(maxValue)
    #print(viterbiMatrix)
    
    backtrace = []
    for col in range(0, len(sentence)):
        maxInCol = 0
        indexes = (-1, -1)
        for row in range(0, len(tagSeq)):

            if maxInCol < viterbiMatrix[row][col]:
                maxInCol = viterbiMatrix[row][col]
                indexes = (row, col)

        backtrace.append(indexes)

    #print(backtrace)
        
    #for i in range(0, len(backtrace)):
        #get tags
        #print(backtrace[i][0],",",backtrace[i][1])

        #word = sentence[backtrace[i][1]]
        #tag = tagSeq[backtrace[i][0]]

        #print(word,", ", tag)
        
    
    return backtrace, tagSeq
    
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
