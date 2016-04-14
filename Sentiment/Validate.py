import sys
import os
import csv
import re
import argparse
from SentimentEngine import SentimentEngine
from tabulate import tabulate

class AccuracyMeasures:
    def __init__(self, name):
        self.truePositive = 0
        self.trueNegative = 0
        self.falsePositive = 0
        self.falseNegative = 0
        self.itemCount = 0
        self.truePositiveFile = open(name + '-truePositive', 'w')
        self.trueNegativeFile = open(name + '-trueNegative', 'w')
        self.falsePositiveFile = open(name + '-falsePositive', 'w')
        self.falseNegativeFile = open(name + '-falseNegative', 'w')
        self.invalidFile = open(name + '-invalid', 'w')
        self.skipFile = open(name + '-skipped', 'w')
        self.accuracyFile = open(name + '-accuracyMeasures', 'w')

def labeledSentiment():
    os.chdir('validation-results')

    accuracyMeasure = AccuracyMeasures('labeledSentiment')

    os.chdir('..')

    os.chdir('labeledSentiment')

    for filename in os.listdir('.'):
        if '.txt' in filename and not 'readme' in filename:
            f = open(filename, 'r');

            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            
            for line in reader:
                if line[1]:
                    se = SentimentEngine(line[0], 'simple')
                    sentimentSum = sum([sentence.getAggregatePolarizedSentenceSentiment() for sentence in se.getSentences()])
                    sentiment = 0
                    sentiment = 1 if sentimentSum > 0 else (0 if sentimentSum < 0 else -1)
                    if sentiment == -1:
                        # print("Skipping:", line[0])
                        accuracyMeasure.skipFile.write(line[0] + '\n')
                    else:
                        accuracyMeasure.itemCount += 1
                        # print(line[0], line[1], sentiment)

                        if int(line[1]) == 0 and sentiment == 0:
                            accuracyMeasure.trueNegative += 1
                            accuracyMeasure.trueNegativeFile.write(line[0] + '\n')
                        if int(line[1]) == 1 and sentiment == 0:
                            accuracyMeasure.falseNegative += 1
                            accuracyMeasure.falseNegativeFile.write(line[0] + '\n')
                        if int(line[1]) == 0 and sentiment == 1:
                            accuracyMeasure.falsePositive += 1
                            accuracyMeasure.falsePositiveFile.write(line[0] + '\n')
                        elif int(line[1]) == 1 and sentiment == 1:
                            accuracyMeasure.truePositive += 1
                            accuracyMeasure.truePositiveFile.write(line[0] + '\n')
                else:
                    accuracyMeasure.invalidFile.write(line[0] + '\n')
            f.close()


    accuracyMeasure.accuracyFile.write((tabulate([['Actual Positive', str(accuracyMeasure.truePositive), str(accuracyMeasure.falseNegative)], ['Actual Negative', str(accuracyMeasure.falsePositive), str(accuracyMeasure.trueNegative)]], headers=['', 'Classified Positive', 'Classified Negative'])) + '\n')

    precision = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falsePositive)
    recall = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falseNegative)

    accuracyMeasure.accuracyFile.write('numItems: ' + str(accuracyMeasure.itemCount) + '\n')
    accuracyMeasure.accuracyFile.write('Precision: ' + str(precision) + '\n')
    accuracyMeasure.accuracyFile.write('Recall: ' + str(recall) + '\n')
    accuracyMeasure.accuracyFile.write('PF: ' + str(accuracyMeasure.falsePositive/ float(accuracyMeasure.falsePositive + accuracyMeasure.trueNegative)) + '\n')
    accuracyMeasure.accuracyFile.write('F-Measure: ' + str(2.0 / ((1.0 / precision) + (1.0 / recall))) + '\n')

    accuracyMeasure.truePositiveFile.close()
    accuracyMeasure.trueNegativeFile.close()
    accuracyMeasure.falsePositiveFile.close()
    accuracyMeasure.falseNegativeFile.close()
    accuracyMeasure.skipFile.close()
    accuracyMeasure.invalidFile.close()

    os.chdir('..')

def proCons():
    os.chdir('validation-results')

    accuracyMeasure = AccuracyMeasures('pro-cons')

    os.chdir('..')

    os.chdir('pro-cons')
    consFile = open('IntegratedCons.txt', 'r', encoding = "ISO-8859-1")
    cons = re.findall(r'<Cons>(.*?)</Cons>', consFile.read())

    prosFile  = open('IntegratedPros.txt', 'r', encoding = "ISO-8859-1")
    pros = re.findall(r'<Pros>(.*?)</Pros>', prosFile.read())

    for con in cons:
        se = SentimentEngine(con, 'simple')
        sentimentSum = sum([sentence.getAggregatePolarizedSentenceSentiment() for sentence in se.getSentences()])
        sentiment = 0
        sentiment = 1 if sentimentSum > 0 else (0 if sentimentSum < 0 else -1)
        if sentiment == -1:
            # print("Skipping:", con)
            accuracyMeasure.skipFile.write(con + '\n')
        else:
            accuracyMeasure.itemCount += 1

            if sentiment == 0:
                accuracyMeasure.trueNegative += 1
                accuracyMeasure.trueNegativeFile.write(con + '\n')
            elif sentiment == 1:
                accuracyMeasure.falsePositive += 1
                accuracyMeasure.falsePositiveFile.write(con + '\n')

    for pro in pros:
        se = SentimentEngine(pro, 'simple')
        sentimentSum = sum([sentence.getAggregatePolarizedSentenceSentiment() for sentence in se.getSentences()])
        sentiment = 0
        sentiment = 1 if sentimentSum > 0 else (0 if sentimentSum < 0 else -1)
        if sentiment == -1:
            # print("Skipping:", pro)
            accuracyMeasure.skipFile.write(pro + '\n')
        else:
            accuracyMeasure.itemCount += 1

            if sentiment == 0:
                accuracyMeasure.falseNegative += 1
                accuracyMeasure.falseNegativeFile.write(pro + '\n')
            elif sentiment == 1:
                accuracyMeasure.truePositive += 1
                accuracyMeasure.truePositiveFile.write(pro + '\n')

    accuracyMeasure.accuracyFile.write((tabulate([['Actual Positive', str(accuracyMeasure.truePositive), str(accuracyMeasure.falseNegative)], ['Actual Negative', str(accuracyMeasure.falsePositive), str(accuracyMeasure.trueNegative)]], headers=['', 'Classified Positive', 'Classified Negative'])) + '\n')

    precision = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falsePositive)
    recall = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falseNegative)

    accuracyMeasure.accuracyFile.write('numItems: ' + str(accuracyMeasure.itemCount) + '\n')
    accuracyMeasure.accuracyFile.write('Precision: ' + str(precision) + '\n')
    accuracyMeasure.accuracyFile.write('Recall: ' + str(recall) + '\n')
    accuracyMeasure.accuracyFile.write('PF: ' + str(accuracyMeasure.falsePositive/ float(accuracyMeasure.falsePositive + accuracyMeasure.trueNegative)) + '\n')
    accuracyMeasure.accuracyFile.write('F-Measure: ' + str(2.0 / ((1.0 / precision) + (1.0 / recall))) + '\n')

    accuracyMeasure.truePositiveFile.close()
    accuracyMeasure.trueNegativeFile.close()
    accuracyMeasure.falsePositiveFile.close()
    accuracyMeasure.falseNegativeFile.close()
    accuracyMeasure.skipFile.close()
    accuracyMeasure.invalidFile.close()

    prosFile.close()
    consFile.close()
    
    os.chdir('..')

def reviewPolarity():
    os.chdir('validation-results')

    accuracyMeasure = AccuracyMeasures('review_polarity')

    os.chdir('..')

    os.chdir('review_polarity/txt_sentoken')

    os.chdir('neg')

    for filename in os.listdir('.'):
        if '.txt' in filename:
            f = open(filename, 'r')
            se = SentimentEngine(f.read(), 'simple')
            sentimentSum = sum([sentence.getAggregatePolarizedSentenceSentiment() for sentence in se.getSentences()])
            sentiment = 0
            sentiment = 1 if sentimentSum > 0 else (0 if sentimentSum < 0 else -1)
            if sentiment == -1:
                pass
                # print("Skipping:", con)
                # accuracyMeasure.skipFile.write(con + '\n')
            else:
                accuracyMeasure.itemCount += 1

                if sentiment == 0:
                    accuracyMeasure.trueNegative += 1
                    # accuracyMeasure.trueNegativeFile.write(con + '\n')
                elif sentiment == 1:
                    accuracyMeasure.falsePositive += 1
                    # accuracyMeasure.falsePositiveFile.write(con + '\n')
            f.close()

    os.chdir('..')

    os.chdir('pos')

    for filename in os.listdir('.'):
        if '.txt' in filename:
            f = open(filename, 'r')
            se = SentimentEngine(f.read(), 'simple')
            sentimentSum = sum([sentence.getAggregatePolarizedSentenceSentiment() for sentence in se.getSentences()])
            sentiment = 0
            sentiment = 1 if sentimentSum > 0 else (0 if sentimentSum < 0 else -1)
            if sentiment == -1:
                pass
                # print("Skipping:", pro)
                # accuracyMeasure.skipFile.write(pro + '\n')
            else:
                accuracyMeasure.itemCount += 1

                if sentiment == 0:
                    accuracyMeasure.falseNegative += 1
                    #accuracyMeasure.falseNegativeFile.write(pro + '\n')
                elif sentiment == 1:
                    accuracyMeasure.truePositive += 1
                    #accuracyMeasure.truePositiveFile.write(pro + '\n')

            f.close()

    os.chdir('..')

    accuracyMeasure.accuracyFile.write((tabulate([['Actual Positive', str(accuracyMeasure.truePositive), str(accuracyMeasure.falseNegative)], ['Actual Negative', str(accuracyMeasure.falsePositive), str(accuracyMeasure.trueNegative)]], headers=['', 'Classified Positive', 'Classified Negative'])) + '\n')

    precision = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falsePositive)
    recall = accuracyMeasure.truePositive / float(accuracyMeasure.truePositive + accuracyMeasure.falseNegative)

    accuracyMeasure.accuracyFile.write('numItems: ' + str(accuracyMeasure.itemCount) + '\n')
    accuracyMeasure.accuracyFile.write('Precision: ' + str(precision) + '\n')
    accuracyMeasure.accuracyFile.write('Recall: ' + str(recall) + '\n')
    accuracyMeasure.accuracyFile.write('PF: ' + str(accuracyMeasure.falsePositive/ float(accuracyMeasure.falsePositive + accuracyMeasure.trueNegative)) + '\n')
    accuracyMeasure.accuracyFile.write('F-Measure: ' + str(2.0 / ((1.0 / precision) + (1.0 / recall))) + '\n')

    accuracyMeasure.truePositiveFile.close()
    accuracyMeasure.trueNegativeFile.close()
    accuracyMeasure.falsePositiveFile.close()
    accuracyMeasure.falseNegativeFile.close()
    accuracyMeasure.skipFile.close()
    accuracyMeasure.invalidFile.close()


    os.chdir('../..')

def main():

    try:
        os.chdir('validation')
    except OSError:
        print("Failed to find validation folder")
        return -1

    for filename in os.listdir('.'):
        if os.path.isdir(filename):
            if filename == 'labeledSentiment':
                pass
                # labeledSentiment()
            elif filename == 'pro-cons':
                pass
                # proCons()
            elif filename == 'review_polarity':
                reviewPolarity()

    return 0

if __name__ == "__main__":
    sys.exit(main())
