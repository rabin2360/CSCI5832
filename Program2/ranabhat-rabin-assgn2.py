#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
import math
#import re

def main():

    #check the input parameters to ensure that training and test files are entered
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

#probabilities of unigrams and bigrams
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

                unigramArray = line.strip()
                unigramArray = unigramArray.split()

                bigramArray = line.strip()
                bigramArray = bigramArray.split()
                
                unigramProbabilityModel(unigramArray, unigramProbDict)
                bigramProbabilityModel(bigramLineDict, bigramProbDict, unigramProbDict, firstKey)            
                bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey)

#unigram probabilities
def unigramProb(unigramDict, wordCount):
    unigramProbabilityDict = dict()

    for key, value in unigramDict.items():
        unigramProbabilityDict[key] = value/wordCount;
    
    return unigramProbabilityDict

#probabilities of bigram combinations
def bigramProb(bigramDict, unigramDict):
    bigramProbabilityDict = dict()
#    print(unigramDict)
    
    for key, value in bigramDict.items():
        key1 = key[1]
        bigramKeyValue = bigramDict[key]
        bigramProbabilityDict[key] = bigramKeyValue /(unigramDict.get(key1))

    return bigramProbabilityDict

#uses the unigram probabilties to determine probability for the sentence using unigrams
def unigramProbabilityModel(unigramLineArray, unigramProbDict):

    unigramProbability = 0
    hasZero = False
        
    for i in range(len(unigramLineArray)):
        if unigramProbDict.get(unigramLineArray[i]) == None:
            hasZero = True
            break
        else:
            #print('key: ',unigramLineArray[i],' value',unigramProbDict.get(unigramLineArray[i]), 'log ',math.log10(unigramProbDict.get(unigramLineArray[i])))      
            unigramProbability = unigramProbability + math.log10(unigramProbDict.get(unigramLineArray[i]))
            
#    print("Count ", count)
    if hasZero == False:
        print("Unigrams: logprob(S) = ", unigramProbability)
    else:
        print("Unigrams: logprob(S) = undefined")
            
#uses the bigram probabilites to determine probability for the sentence. Bigrams used
def bigramProbabilityModel(bigramLineDict, bigramProbDict, unigramProbDict, firstKey):
    #print('bigram Line Dict: ', bigramLineDict)
    #print('bigram Prob Dict: ', bigramProbDict)
    #print('uingram Dict: ', unigramProbDict)

    #getting the first value in the line
    probability = 0
    bigramProbValue = 0
    hasZero = False
    count = 0
    
    #checking if the key is in unigram
    if unigramProbDict.get(firstKey) == None:
        probability = 0
        hasZero = True
    else:
        probability = math.log10(unigramProbDict.get(firstKey))
        #print("unigramKey", firstKey," prob value: ",unigramProbDict.get(firstKey), " value:",math.log10(unigramProbDict.get(firstKey)))
        count += 1
        for key, value in bigramLineDict.items():
            
                bigramKey = key
                #print("bigram key", key)
                #checking if the key is in the bigram, otherwise bail!
                if bigramProbDict.get(key) == None:
                    hasZero = True
                    break
                else:
                    bigramProbValue = bigramProbDict.get(key)
                    probability = probability + value*math.log10(bigramProbValue)
                    count += 1
                    #print("bigramKey", key,": ",bigramProbValue, "-->", math.log10(bigramProbValue), "count: ", value)
    
    if hasZero == False:
        probability = probability
        print('Bigrams: logprob(S) = ',probability)
    else:
        print('Bigrams: logprob(S) = undefined')



def bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey):

    probability = 0
    tokenCount = 0
    
    #account for the first element
    if unigramDict.get(firstKey) == None:
        unigramDict[firstKey] = 1

    for key, value in unigramDict.items():
        tokenCount += unigramDict.get(key)

    #Need to smooth unigrams over?
    probability = math.log10(unigramDict.get(firstKey) / tokenCount)
        
    #account for the rest of it
    for key, value in bigramLineDict.items():
        if bigramDict.get(key) == None:
            bigramDict[key] = 1
        else:
            bigramDict[key] += 1

        #key value for bigram
        bigramCount = bigramDict[key]

        #demonimator - not sure about this part
        countOfPrecedingWord = unigramDict.get(key[1]) + len(unigramDict)

        probability = probability + math.log10(bigramCount/countOfPrecedingWord)


#    probability = math.exp(probability)
    print('Smoothed Bigrams: logprob(S) = ',probability)
    print()
    
    
#counting the occurences of bigrams in the tranining corpus 
def countBiGrams(line, bigramDict):
    wordArray = line.split()

    for i in range(len(wordArray)):
        if i < len(wordArray)-1:
            alias = (wordArray[i+1], wordArray[i])

            if bigramDict.get(alias) != None:
                bigramDict[alias] += 1
            else:
                bigramDict[alias] = 1

    return bigramDict

#counting the occurences of unigrams in the traning corpus
def countUniGrams(line, wordDict):
    #read the words separated by the white space
    for word in line.split():
        
        #if not in the dictionary, add key otherwise increment count
        if wordDict.get(word) != None:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
            
    return wordDict

#makes the main method the default method
if __name__=="__main__":
    main()
