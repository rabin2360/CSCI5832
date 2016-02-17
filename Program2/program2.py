#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
import math
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
    bigramLineDict = dict()
    wordCount = 0
    
    #reading the training file
    with open(sys.argv[1]) as file:
        for line in file:
            if len(line) > 1:
                line = line.lower()
                wordCount += len(line.split())
                #getting rid of the \n from the input line
                unigramDict = countUniGrams(line.strip(), unigramDict)
                bigramDict = countBiGrams(line.strip(), bigramDict)
                
#    print('Bigram dict \n', bigramDict)
#    print('Unigram dict \n', unigramDict)
#    print('Word count \n', wordCount)

    unigramProbDict = unigramProb(unigramDict, wordCount)
    bigramProbDict = bigramProb(bigramDict, unigramDict)

#    print('Porbability\n')
#    print('Unigram probability: ',unigramProbDict)
#    print('Bigram probability: ', bigramProbDict)


#    for key, value in sorted(bigramProbDict.items()):
#        print(key, value)
    
    #reading the test file            
    with open(sys.argv[2]) as file:
        for line in file:
            bigramLineDict = dict()
            unigramLineDict = dict()
            if len(line) > 1:
                print("S = ", line.strip())
                line = line.lower()
                #getting the first word in the line
                firstKey = line.split(None, 1)[0]
                
                bigramLineDict = countBiGrams(line.strip(), bigramLineDict)
                unigramLineDict = countUniGrams(line.strip(), unigramLineDict)
                #print(bigramLineDict)
                unigramProbability(unigramLineDict, unigramProbDict)
                bigramProbability(bigramLineDict, bigramProbDict, unigramProbDict, firstKey)            

                bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey)
def unigramProb(unigramDict, wordCount):
    unigramProbabilityDict = dict()

    for key, value in unigramDict.items():
        unigramProbabilityDict[key] = value/wordCount;
    
    return unigramProbabilityDict

def bigramProb(bigramDict, unigramDict):
    bigramProbabilityDict = dict()
#    print(unigramDict)
    
    for key, value in bigramDict.items():
        key1 = key[1]
        bigramKeyValue = bigramDict[key]
        bigramProbabilityDict[key] = bigramKeyValue /(unigramDict.get(key1))

    return bigramProbabilityDict

def unigramProbability(unigramLineDict, unigramProbDict):

    unigramProbability = 1
    hasZero = False
    
    for key in unigramLineDict:
        if unigramProbDict.get(key) == None:
            hasZero = True
            break
        else:
            unigramProbability = unigramProbability + math.log10(unigramProbDict.get(key))

    if hasZero == False:
        print("Unigrams: logprob(S) = %.4f" %math.exp(unigramProbability))
    else:
        print("Unigrams: logprob(S) = undefined")
            
       
def bigramProbability(bigramLineDict, bigramProbDict, unigramProbDict, firstKey):
    #print('bigram Line Dict: ', bigramLineDict)
    #print('bigram Prob Dict: ', bigramProbDict)
    #print('uingram Dict: ', unigramProbDict)

    #getting the first value in the line
    probability = 1
    bigramProbValue = 0
    hasZero = False
    
    #checking if the key is in unigram
    if unigramProbDict.get(firstKey) == None:
        probability = 0
        hasZero = True
    else:
        probability = math.log10(unigramProbDict.get(firstKey))
    
        for key, value in bigramLineDict.items():
            
                bigramKey = key
                #print("bigram key", key)
                #checking if the key is in the bigram, otherwise bail!
                if bigramProbDict.get(key) == None:
                    hasZero = True
                    break
                else:
                    bigramProbValue = bigramProbDict.get(key)
                    probability = probability + math.log10(bigramProbValue)
                    #print("prob value: ",bigramProbValue, "bigramKey", bigramKey)

    
    if hasZero == False:
        probability = math.exp(probability)
        print('Bigrams: logprob(S) = %.4f' % probability)
    else:
        print('Bigrams: logprob(S) = undefined')
    #formatted printing
    

    #print('\n')
    #unigram language modeling without smoothing
           
    #bigram language modeling with smoothing


def bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey):

    bigramCount = len(bigramDict)
    probability = 1

    #account for the first element
    #-----need to work here ----------
    
    #account for the rest of it
    
    for key, value in bigramLineDict.items():
        if bigramDict.get(key) == None:
            bigramDict[key] = 1
        else:
            bigramDict[key] += 1

        #key value for bigram
        bigramKeyValue = bigramDict[key]

        #demonimator
        denominator = unigramDict.get(key[1]) + len(bigramDict)

        probability = probability + math.log10(bigramKeyValue/denominator)


    probability = math.exp(probability)
    print('Smoothed Bigrams: logprob(S) = %.4f' % probability)
    print()
    
    
        
def countBiGrams(line, bigramDict):
    #print('counting bi-grams', line)

    wordArray = line.split()

    for i in range(len(wordArray)):
        if i < len(wordArray)-1:
            alias = (wordArray[i+1], wordArray[i])

            if alias in bigramDict:
                bigramDict[alias] += 1
            else:
                bigramDict[alias] = 1

    return bigramDict
    
def countUniGrams(line, wordDict):
    count = 0
    
    #read the words separated by the white space
    for word in line.split():
        
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
