# analyzeResults.py
#   This reads in the output from the crossvalidation folds, combines it, and then computes summary scores (BLEU, percent correct)

import os
import json


# 
#   File I/O
#


# Load data in JSONL format
def loadFileJSONL(filename:str):
    out = []

    print(" * loadFileJSONL (" + filename + ")")
    f = open(filename, 'r')
    for line in f.readlines():
        # Parse JSON
        print(line)
        oneLine = json.loads(line)
        out.append(oneLine)

    print(" * loadFileJSONL: Loaded " + str(len(out)) + " lines.")
    return out


def exportJSONL(filenameOut:str, arrayOut):
    print("Writing " + filenameOut)
    with open(filenameOut, 'w') as f:
        for line in arrayOut:
            lineStr = json.dumps(line)
            f.write(lineStr + "\n")

    print ("Wrote " + str(len(arrayOut)) + " lines.")
        


#
#   Main
#

pathInput = "/home/peter/github/darmok/models/out-base-"
resultsFilename = "generated_eval.jsonl"             # Dev
#resultsFilename = "generated_predictions.jsonl"      # Test

numFolds = 10

# Load all generated samples into one combined array
combined = []
for foldIdx in range(0, numFolds):
    results = loadFileJSONL(pathInput + "fold" + str(foldIdx) + "/" + resultsFilename)
    for sample in results:
        combined.append(sample)


# Compute overall score
numCorrect = 0
scoreBleu = 0
totalSamples = 0
for sample in combined:
    source = sample['source']
    target = sample['target']
    generated = sample['predict']
    bleu = float(sample['score'])

    # correctness
    if (target.strip() == generated.strip()):
        numCorrect += 1
        sample["correct"] = 1           # Also add correctness scores to sample
    else:
        sample["correct"] = 0

    # bleu
    scoreBleu += bleu

    totalSamples += 1

# Averages
scoreBleu = scoreBleu / totalSamples
avgCorrect = numCorrect / totalSamples

# Output combined JSONL file
filenameOutCombined = pathInput + "-combined-" + resultsFilename
exportJSONL(filenameOutCombined, combined)


# Performance summary
print("-----------------------")
print("  Performance Summary")
print("-----------------------")
print(" Input Path: " + str(pathInput))
print(" Filename: " + str(resultsFilename))
print(" Number of crossvalidation folds: " + str(numFolds))
print("")

print(" average BLEU: " + str(scoreBleu))
print(" average correct: " + str(avgCorrect))


print("-----------------------")

print("")






