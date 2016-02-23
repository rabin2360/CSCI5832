#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
import math

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
    
    #reading the training corpus
    with open(sys.argv[1]) as file:
        for line in file:
            #ignoring '\n' only lines 
            if len(line) > 1:
                #convert the line read from the training corpus to lower case
                line = line.lower()
                #counting the words in the training corpus
                wordCount += len(line.split())
                #getting rid of the \n from the input line and creating unigram and bigram dictionaries for the training corpus
                unigramDict = countUniGrams(line.strip(), unigramDict)
                bigramDict = countBiGrams(line.strip(), bigramDict)
                
    #determining probabilities of unigrams and bigrams and inserting them to the unigramProbDict and bigramProbDict respectively
    unigramProbDict = unigramProb(unigramDict, wordCount)
    bigramProbDict = bigramProb(bigramDict, unigramDict)

    #reading the test corpus            
    with open(sys.argv[2]) as file:
        for line in file:
            #resetting the bigram and unigram dictionary for each new test sentence read
            bigramLineDict = dict()
            unigramLineDict = dict()
            
            if len(line) > 1:
                #stripping the read test sentence of new line character
                print("S = ", line.strip())
                #converting the read test sentence to lower case
                line = line.lower()

                #getting the first word of the test sentence read
                firstKey = line.split(None, 1)[0]

                #creating the bigram dictionary for the test sentence read
                bigramLineDict = countBiGrams(line.strip(), bigramLineDict)

                #splitting the test sentence into array of words
                unigramArray = line.strip()
                unigramArray = unigramArray.split()

                #determining the unigram model, bigram model (with or without smoothing)
                unigramProbabilityModel(unigramArray, unigramProbDict)
                bigramProbabilityModel(bigramLineDict, bigramProbDict, unigramProbDict, firstKey)            
                bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey)

#the function determines the unigram probabilities of the training corpus
def unigramProb(unigramDict, wordCount):
    #declaring the unigram probability dictionary
    unigramProbabilityDict = dict()

    #iterating through the unigram dictionary and determining probability
    #probability formula: (Count of the word in the vocabulary)/(Count of total words in the training corpus)
    for key, value in unigramDict.items():
        unigramProbabilityDict[key] = value/wordCount;
    
    return unigramProbabilityDict

#the function determines the probabilities of bigram combinations in the training corpus
def bigramProb(bigramDict, unigramDict):
    #declaring the bigram probability dictionary
    bigramProbabilityDict = dict()

    #iterating through the bigram dictionray and determining the probability of each bigram combination
    #bigram probability formula = (Count of the bigram in the training corpus)/(Count of the preceding word in the bigram present in the tranining corpus)
    for key, value in bigramDict.items():
        key1 = key[1]
        bigramKeyValue = bigramDict[key]
        bigramProbabilityDict[key] = bigramKeyValue /(unigramDict.get(key1))

    return bigramProbabilityDict

#uses the unigram probabilties to determine probability for the sentence using unigrams
def unigramProbabilityModel(unigramLineArray, unigramProbDict):

    unigramProbability = 0
    hasZero = False

    #iterates through the array of words and determines the probability of the test sentence
    for i in range(len(unigramLineArray)):
        #if the word in the test sentence is not in the unigram probability dictionary, break out of the loop with condition for hasZero set to true
        if unigramProbDict.get(unigramLineArray[i]) == None:
            hasZero = True
            break
        else:
            #add the log probabilities for the test sentence together
            unigramProbability = unigramProbability + math.log10(unigramProbDict.get(unigramLineArray[i]))
            
    #if all the words in the test sentence are in the unigram probability dictionary, print the probability, otherwise, print undefined
    if hasZero == False:
        print("Unigrams: logprob(S) = ", unigramProbability)
    else:
        print("Unigrams: logprob(S) = undefined")
            
#uses the bigram probabilites to determine the bigram probability (without smootihng) for the sentence
def bigramProbabilityModel(bigramLineDict, bigramProbDict, unigramProbDict, firstKey):

    #probability of the sentence
    probability = 0
    #bigram probability for bigrams in the test sentence
    bigramProbValue = 0
    hasZero = False
    
    #checking to see if the first word in the test sentence is in the unigram probability dictionary. If the word is not present, the hasZero condition is set to true and no further probability determination of bigrams are made
    if unigramProbDict.get(firstKey) == None:
        probability = 0
        hasZero = True
    else:
        probability = math.log10(unigramProbDict.get(firstKey))
        #iterate over the bigram dictionary for the line
        for key, value in bigramLineDict.items():            
                bigramKey = key

                #checking if the key is in the bigram probability dictionary, otherwise bail!
                if bigramProbDict.get(key) == None:
                    hasZero = True
                    break
                else:
                    #getting the probability value for the bigram
                    bigramProbValue = bigramProbDict.get(key)
                    #adding up the probability. The value for the test sentence bigram dictionary is important because if there is a bigram that is repeated in the test sentence, the value will help account for the repeating bigrams in the sentence
                    probability = probability + value*math.log10(bigramProbValue)

    #if all the bigrams for the test sentence are present in the bigram probability dictionary, print the probability, otherwise print undefined
    if hasZero == False:
        probability = probability
        print('Bigrams: logprob(S) = ',probability)
    else:
        print('Bigrams: logprob(S) = undefined')

#uses the bigram probabilites to determine the bigram probability (with smootihng) for the sentence
def bigramSmoothingProbability(bigramLineDict, bigramDict, unigramDict, firstKey):

    probability = 0
    totalWords = 0
    
    #checking to see if the first word in the test sentence is in the unigram probability dictionary. If the word is not present, the word is added to the dictionary and 1 is added as word count
    if unigramDict.get(firstKey) == None:
        unigramDict[firstKey] = 1

    #counting the total words in the training corpus
    for key, value in unigramDict.items():
        totalWords += unigramDict.get(key)

    #Determining the probability of the first word in the test sentence
    probability = math.log10(unigramDict.get(firstKey) / totalWords)
        
    #determining the probability of bigrams in the test sentence, if a bigram is not present in the bigram dictionary, 1 is added in place of 0, if a bigram is present, then 1 is added regardless
    for key, value in bigramLineDict.items():
        if bigramDict.get(key) == None:
            bigramDict[key] = 1
        else:
            bigramDict[key] += 1

        #getting the bigram count for the bigram key
        bigramCount = bigramDict[key]

        #determining the count of the preceding word and then adding the size of the vocabulary of the training corpus for smoothing
        countOfPrecedingWord = unigramDict.get(key[1]) + len(unigramDict)

        #determining the bigram probability with smoothing
        #probability = (count of the bigram in the test sentence/count of the preceding word)
        probability = probability + math.log10(bigramCount/countOfPrecedingWord)

    #printing the bigram with smoothing
    print('Smoothed Bigrams: logprob(S) = ',probability)
    print()
    
    
#counting the occurences of bigrams in the tranining corpus 
def countBiGrams(line, bigramDict):
    wordArray = line.split()

    #split words into an array, make a bigram key such that a sentence, "This is a test" will produce keys like "(is, this), (a, is)".
    #the bigram keys look odd but I tried following the book where examples list P(w in nth position | w in n-1 position)
    for i in range(len(wordArray)):
        if i < len(wordArray)-1:
            alias = (wordArray[i+1], wordArray[i])

            #if the bigram is not in the dictionary, add the key and initiate the count to 1 otherwise increment the count by 1
            if bigramDict.get(alias) != None:
                bigramDict[alias] += 1
            else:
                bigramDict[alias] = 1

    return bigramDict

#counting the occurences of unigrams in the training corpus
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
