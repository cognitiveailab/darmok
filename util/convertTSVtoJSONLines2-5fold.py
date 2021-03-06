# Creates crossvalidation folds for the Tamarian language

import random
import copy
from collections import deque
import os
import math

# 
#   File I/O
#
def loadSpreadsheetTSV(filename:str):
    out = []
    print ("* loadSpreadsheetTSV(): Loading... " + str(filename))

    f = open(filename, 'r')    
    lineIdx = 0
    for line in f.readlines():        
        if (lineIdx > 0):                   # Skip TSV header
            fields = line.split("\t")

            utterance = fields[0].strip()
            location = fields[1].strip()    # Discard
            meaning = fields[2].strip()
            done = fields[3].strip()        # Discard
            examples = [x.strip() for x in fields[4:14]]
            examples = [x for x in examples if len(x) > 0]

            record = {}
            record['utterance'] = utterance        
            record['meaning'] = meaning
            record['examples'] = examples
            
            out.append(record)

        lineIdx += 1

    
    print("* loadSpreadsheetTSV(): Read " + str(len(out)) + " records.")

    # Return
    return out


# Write an array of lines to a file
def writeLines(filenameOut:str, linesOut):
    print("Writing " + filenameOut)
    with open(filenameOut, 'w') as f:
        for line in linesOut:
            f.write("%s\n" % line)


# Make crossvalidation folds (8/1/1)
def mkCrossvalidationFolds(dataIn, numFolds, foldIdx):    
    propTrain = (1/numFolds) * 3
    propDev = (1/numFolds) * 1
    propTest = (1/numFolds) * 1

    trainOut = []
    devOut = []
    testOut = []

    # Shift array
    print("FoldIdx: " + str(foldIdx))
    dataInShifted = []
    for record in dataIn:
        totalExamples = len(record['examples'])
        numToShift = math.floor((1/numFolds) * totalExamples)
        #print("totalExamples: " + str(totalExamples) + "  numToShift: " + str(numToShift) )
        recordCopy = copy.deepcopy(record)

        shifted = deque(recordCopy['examples'])
        shifted.rotate(numToShift * foldIdx)
        recordCopy['examples'] = list(shifted)

        #print("Length: " + str(len(recordCopy['examples'])))

        dataInShifted.append(recordCopy)


    for record in dataInShifted:
        totalExamples = len(record['examples'])
        sizeTrain = math.floor(totalExamples * propTrain)
        sizeDev = math.floor(totalExamples * propDev)
        sizeTest = math.floor(totalExamples * propTest)

        #print("totalExamples: " + str(totalExamples))
        #print("sizeTrain: " + str(sizeTrain))
        #print("sizeDev: " + str(sizeDev))
        #print("sizeTest: " + str(sizeTest))

        recDev = copy.deepcopy(record)
        #recDev['examples'] = recDev['examples'][sizeTrain:sizeTrain+sizeDev]
        recDev['examples'] = recDev['examples'][0:sizeDev]
        devOut.append(recDev)

        recTest = copy.deepcopy(record)        
        #recTest['examples'] = recTest['examples'][sizeTrain+sizeDev:sizeTrain+sizeDev+sizeTest]
        recTest['examples'] = recTest['examples'][sizeDev:sizeDev+sizeTest]
        testOut.append(recTest)

        # Train
        recTrain = copy.deepcopy(record)
        recTrain['examples'] = recTrain['examples'][sizeDev+sizeTest:sizeDev+sizeTest+sizeTrain]      # Everything left, after train/dev
        trainOut.append(recTrain)

    # Return
    return trainOut, devOut, testOut


# Export records to json-lines format
def exportToJsonLines(filenameOut:str, dataOut):
    outLines = []

    for record in dataOut:
        utterance = record['utterance']
        meaning = record['meaning']
        examples = record['examples']

        for example in examples:
            outStr = "{ \"translation\": { \"en\": \"" + example + "\", \"tam\": \"" + utterance + "\" } }"
            outLines.append(outStr)


    # Shuffle before returning
    random.shuffle(outLines)

    # Write to file
    writeLines(filenameOut, outLines)

    # Return
    return outLines





#
#   Main Program
#

path = "july16-50/"
filenameInputTSV = "july16-50/TamarianLanguage50.tsv"

data = loadSpreadsheetTSV(filenameInputTSV)

for record in data:
    print(record)
    print("")

print("Generating crossvalidation folds...")
print("")

numFolds = 5
for foldIdx in range(0, numFolds):
    print ("Generating folds with index: " + str(foldIdx))
    foldPath = path + "/fold" + str(foldIdx) + "/"
    try: 
        os.mkdir(foldPath)
    except: 
        pass

    foldTrain, foldDev, foldTest = mkCrossvalidationFolds(data, numFolds, foldIdx)

    lines = exportToJsonLines(foldPath + "train.json", foldTrain)
    lines = exportToJsonLines(foldPath + "dev.json", foldDev)
    lines = exportToJsonLines(foldPath + "test.json", foldTest)

    print("")




