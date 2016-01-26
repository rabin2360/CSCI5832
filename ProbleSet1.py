#!/bin/env/python3

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
    wordCount = len(re.findall('[a-zA-Z0-9\-\.\',\"\)\(]+', fileContent))
    print('Word(s):',wordCount)
    
    #count sentence

    #count paragraphs
    paragraphCount = len(re.findall('[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*', fileContent))
    print('Paragraph(s):',paragraphCount)

    #print(s)
    
#makes the main method the default method
if __name__=="__main__":
    main()
