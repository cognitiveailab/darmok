
import random
import copy
from collections import deque
import os


# 
#   File I/O
#
def loadSpreadsheetTSV(filename:str):
    out = []
    print ("* loadSpreadsheetTSV(): Loading... " + str(filename))

    f = open(filename, 'r')    
    for line in f.readlines():        
        fields = line.split("\t")

        utterance = fields[0].strip()
        location = fields[1].strip()    # Discard
        meaning = fields[2].strip()
        examples = [x.strip() for x in fields[3:13]]

        record = {}
        record['utterance'] = utterance        
        record['meaning'] = meaning
        record['examples'] = examples
        
        out.append(record)

    
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
def mkCrossvalidationFolds(dataIn, foldIdx):
    sizeTrain = 8
    sizeDev = 1
    sizeTest = 1

    trainOut = []
    devOut = []
    testOut = []

    # Shift array
    print("FoldIdx: " + str(foldIdx))
    dataInShifted = []
    for record in dataIn:
        recordCopy = copy.deepcopy(record)

        shifted = deque(recordCopy['examples'])
        shifted.rotate(foldIdx)
        recordCopy['examples'] = list(shifted)

        print("Length: " + str(len(recordCopy['examples'])))

        dataInShifted.append(recordCopy)


    for record in dataInShifted:
        # Train
        recTrain = copy.deepcopy(record)
        recTrain['examples'] = recTrain['examples'][0:sizeTrain]
        trainOut.append(recTrain)

        recDev = copy.deepcopy(record)
        recDev['examples'] = recDev['examples'][sizeTrain:sizeTrain+sizeDev]
        devOut.append(recDev)

        recTest = copy.deepcopy(record)        
        recTest['examples'] = recTest['examples'][sizeTrain+sizeDev:sizeTrain+sizeDev+sizeTest]
        testOut.append(recTest)

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

path = "july13/"
filenameInputTSV = "july13/Tamarian Language - Utterances.tsv"

data = loadSpreadsheetTSV(filenameInputTSV)

for record in data:
    print(record)
    print("")

print("Generating crossvalidation folds...")
print("")

for foldIdx in range(0, 10):
    print ("Generating folds with index: " + str(foldIdx))
    foldPath = path + "/fold" + str(foldIdx) + "/"
    try: 
        os.mkdir(foldPath)
    except: 
        pass

    foldTrain, foldDev, foldTest = mkCrossvalidationFolds(data, foldIdx)

    lines = exportToJsonLines(foldPath + "train.json", foldTrain)
    lines = exportToJsonLines(foldPath + "dev.json", foldDev)
    lines = exportToJsonLines(foldPath + "test.json", foldTest)

    print("")




