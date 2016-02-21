import csv
import pickle

def setupNegativeWordList():
    negativeWordsList = []

    with open('./sentiment-data/negative-words.txt', "r", encoding = "ISO-8859-1") as negativeWordsFile:
        for line in negativeWordsFile.readlines():

            # Ignore comment lines and empty lines
            if line[0] != ';' and line.strip():
                negativeWordsList.append(line.strip())

    return negativeWordsList

def setupPositiveWordList():
    positiveWordsList = []

    with open('./sentiment-data/positive-words.txt', 'r') as positiveWordsFile:
        for line in positiveWordsFile:
            
            # Ignore comment lines and empty lines
            if line[0] != ';' and line.strip():
                positiveWordsList.append(line.strip())

    return positiveWordsList

class ANEWWord:
    def __init__(self, word, valence, valenceMeanSd, dominance, 
                 dominanceMeanSd, arousal, arousalMeanSd, frequency):
        self.word = str(word)
        self.valence = float(valence)
        self.valenceMeanSd = float(valenceMeanSd)
        self.dominance = float(dominance)
        self.dominanceMeanSd = float(dominanceMeanSd)
        self.arousal = float(arousal)
        self.arousalMeanSd = float(arousalMeanSd)
        self.frequency = int(frequency)

    def __str__(self):
        return "word: {}\nvalence: {}\nvalenceMeanSd: {}\ndominance: {}\ndominanceMeanSd: {}\narousal: {}\narousalMeanSd: {}\nfrequency: {}".format(str(self.word),
               str(self.valence),
               str(self.valenceMeanSd),
               str(self.dominance),
               str(self.dominanceMeanSd),
               str(self.arousal),
               str(self.arousalMeanSd),
               str(self.frequency))

    def __repr__(self):
        return self.__str__()

def setupANEWWordList():
    anewWordList = {}

    with open('./sentiment-data/anew.csv', 'r') as anewWordListCsv:
        csvreader = csv.reader(anewWordListCsv, delimiter=",", quotechar='"')

        # Skip the header line
        next(csvreader)

        for line in csvreader:
            anewWordList[line[0]] = ANEWWord(line[0], line[1], line[2], line[3], 
                                         line[4], line[5], line[6], line[7])

        return anewWordList

class SentiWord:
    def __init__(self, pos, ID, positiveValue, negativeValue, word, definition, num):
        self.pos = pos
        self.ID = ID
        self.positiveValue = positiveValue
        self.negativeValue = negativeValue
        self.word = word
        self.definition = definition
        self.num = num

def setupSentiWordNetList():
    sentiWordNetList = {}

    with open('./sentiment-data/sentiment-word-list.csv', 'r') as sentiWordListCsv:
        csvreader = csv.reader(sentiWordListCsv, delimiter="\t", quotechar='"')

        for line in csvreader:
            if not line[0] or line[0].startswith('#'):
                continue
            for word in line[4].split(' '):
                num = word.split('#', 1)[1]
                word = word.split('#', 1)[0]
                word = word.replace('_', ' ')
                sentiWordNetList[(line[0], word, num)] = SentiWord(line[0], line[1], line[2], line[3], word, line[5], num)

        return sentiWordNetList
