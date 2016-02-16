#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
#import re

def main():
   
    if len(sys.argv) > 2:
        readInputFile()

    else:
        print("Please enter the file name\n")
        print("format <filename.py><trainingFilename><testFile>")


def readInputFile():
    fileContent = ""
    unigramDict = dict()
    bigramDict = dict()
    
    #reading the training file
    with open(sys.argv[1]) as file:
        for line in file:
            if len(line) > 1:
                #getting rid of the \n from the input line
                unigramDict = countUniGrams(line.strip(), unigramDict)

#    print('Unigram dict \n')

#    for key, value in sorted(unigramDict.items()):
#        print(key, value)
    
    #reading the test file            
    with open(sys.argv[2]) as file:
        for line in file:
            bigramDict = countBiGrams(line.strip(), bigramDict)

#    print('Bigram dict \n', bigramDict)

    calculateProbabilities(bigramDict, unigramDict)
    
def calculateProbabilities(bigramDict, unigramDict):
    print('calculating the bigram probability')
    
def countBiGrams(line, bigramDict):
    #print('counting bi-grams', line)

    line = line.lower()

    for word1 in line.split():
        for word2 in line.split():
            alias = (word1, word2)
            bigramDict[alias] = 0


    wordPrevious = None
    for wordCurrent in line.split():
        #print('wordPrevious', wordPrevious, 'wordCurrent', wordCurrent)
        
        bigramValue = (wordPrevious, wordCurrent)

        if bigramValue in bigramDict:
            bigramDict[bigramValue] += 1
        else:
            bigramDict[bigramValue] = 0

        wordPrevious = wordCurrent
    
    #print('bigram', bigramDict)
    return bigramDict
    
def countUniGrams(line, wordDict):
    count = 0
    
    #read the words separated by the white space
    for word in line.split():
        word = word.lower()
    
        #if not in the dictionary, add key otherwise increment count
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
            
        count = count + 1

    #print("word counts: ", count)
    #print("dict: ", wordDict)

    return wordDict

#makes the main method the default method
if __name__=="__main__":
    main()
