#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
#import re

def main():
   
    if len(sys.argv) > 1:
        readInputFile()

    else:
        print("Please enter the file name\n")
        print("format <filename.py><trainingFilename><testFile>")


def readInputFile():
    fileContent = ""

    with open(sys.argv[1]) as file:
        for line in file:
            if len(line) > 1:
                #getting rid of the \n from the input line
                countUniGrams(line.strip())
                #count bi-grams
                countBiGrams(line.strip())
                
def countBiGrams(line):
    #print('counting bi-grams', line)
    bigramDict = dict()
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
    
    print('bigram', bigramDict)
    
    
def countUniGrams(line):
    count = 0
    #print("line: ",line)
    wordDict = dict()
    
    #read the words separated by the white space
    for word in line.split():
        word = word.lower()
        #print(word)

        #if not in the dictionary, add key otherwise increment count
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
            
        count = count + 1

    #print("word counts: ", count)
    #print("dict: ", wordDict)

#makes the main method the default method
if __name__=="__main__":
    main()
