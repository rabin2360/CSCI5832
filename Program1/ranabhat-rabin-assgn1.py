#!/bin/env/python3

#Author: Rabin Ranabhat
#Problem Set 1 - Counting words, paragraphs & sentences

import re
import sys

def main():
    fileContent = readInputFile()
    parseFileContents(fileContent)
    

def readInputFile():
    fileContent = ""
    #open the file
    inputFile = open(sys.argv[1], "r")
    fileContent = inputFile.read()
    inputFile.close()
    
    return fileContent

def parseFileContents(fileContent):
    #count words
    wordCount = len(re.findall('[a-zA-Z0-9\-\.,")(]+', fileContent))
    print('Word(s):',wordCount)
    
    #count sentence
    sentenceCount = len(re.findall('[a-zA-CE-LN-Z0-9\.][a-zA-Z0-9]["\.?!\')]+\s+[A-Z\"(]', fileContent))
    #the regex does not account for the very last sentence in the input text hence the sentenceCount is increment by 1
    print('Sentence(s):',sentenceCount+1)
                        
    #count paragraphs
    paragraphCount = len(re.findall('[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*', fileContent))
    print('Paragraph(s):',paragraphCount)

#makes the main method the default method
if __name__=="__main__":
    main()
