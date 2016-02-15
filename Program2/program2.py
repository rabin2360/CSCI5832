#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 2 - N-grams modeling

import sys
import re

def main():
   
    if len(sys.argv) > 1:
        readInputFile()

    else:
        print("Please enter the file name\n")
        print("format <filename.py><trainingFilename><testFile>")


def readInputFile():
    fileContent = ""

    with open(sys.argv[1]) as f:
        for line in f:
            if len(line) > 1:
                countUniGrams(line.strip())


def countUniGrams(line):
    count = 0
    print("line: ",line)

    #read the words separated by the white space
    for word in line.split():
        print(word)
        count = count + 1

    print("word counts: ", count)

#makes the main method the default method
if __name__=="__main__":
    main()
