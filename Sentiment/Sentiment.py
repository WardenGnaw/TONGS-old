import sys
import nltk
import csv

def setupNegativeWordList():
    negativeWordsList = []

    with open('./sentiment-data/negative-words.txt', 'r') as negativeWordsFile:
        for line in negativeWordsFile:

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
    anewWordList = []

    with open('./sentiment-data/anew.csv', 'r') as anewWordListCsv:
        csvreader = csv.reader(anewWordListCsv, delimiter=",", quotechar='"')

        # Skip the header line
        csvreader.next()

        for line in csvreader:
            anewWordList.append(ANEWWord(line[0], line[1], line[2], line[3], 
                                         line[4], line[5], line[6], line[7]))

        return anewWordList

negativeWordsList = setupNegativeWordList()
positiveWordsList = setupNegativeWordList()
anewWordList = setupANEWWordList()

class SentimentEngine:
    def __init__(self, sentence):
        self.rawSentence = sentence
        self.tokens = nltk.word_tokenize(sentence)
        self.pos = [pos[1] for pos in nltk.pos_tag(self.tokens)]
        self.wordsSentiment = [self.getWordSentiment(word.lower()) for word in self.tokens]
        self.aggregiateSentenceSentiment = sum(self.wordsSentiment)
        self.absSentenceSentiment = max(abs(i) for i in self.wordsSentiment)
        self.maxSentenceSentiment = max(self.wordsSentiment)
        self.minSentenceSentiment = min(self.wordsSentiment)

    @staticmethod
    def getWordSentiment(word):
        if word in negativeWordsList:
            return -1
        if word in positiveWordsList:
            return 1
        return 0

    def getAggregiateSentenceSentiment(self):
        return self.aggregiateSentenceSentiment

    def getAbsSentenceSentiment(self):
        return self.absSentenceSentiment

    def getMaxSentenceSentiment(self):
        return self.maxSentenceSentiment
    
    def getMinSentenceSentiment(self):
        return self.minSentenceSentiment

    def getPolarity(word):
        return 0

def main():
    return 0

if __name__ == "__main__":
   sys.exit(main()) 
