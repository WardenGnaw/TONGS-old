import sys
import nltk
import SetupSentimentData
from nltk.tokenize import TweetTokenizer

# Set up word lists to use for sentiment analysis.
negativeWordsList = SetupSentimentData.setupNegativeWordList()
positiveWordsList = SetupSentimentData.setupPositiveWordList() 
anewWordList = SetupSentimentData.setupANEWWordList() 
sentiWordNetList = SetupSentimentData.setupSentiWordNetList()
negationWords = ["no", "not", "doesn't", "neither"]

class SentimentEngine:
    def __init__(self, sentence):
        self.rawSentence = sentence
        self.tokens = TweetTokenizer().tokenize(sentence)

        # Setup basic polarity
        self.polarity = []
        curPolarity = 1
        for token in self.tokens:
            if token in negationWords:
                curPolarity = curPolarity * -1
            self.polarity.append(curPolarity)

        self.pos = [pos[1] for pos in nltk.pos_tag(self.tokens)]
        self.wordsSentiment = [self.getWordSentiment(word) * self.getPolarity(word) for word in self.tokens]
        self.aggregiateSentenceSentiment = sum(self.wordsSentiment)
        self.absSentenceSentiment = max(abs(i) for i in self.wordsSentiment)
        self.maxSentenceSentiment = max(self.wordsSentiment)
        self.minSentenceSentiment = min(self.wordsSentiment)

    @staticmethod
    def getWordSentiment(word):
        word = word.lower()

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

    def getPolarity(self, word):
        return self.polarity[self.tokens.index(word)]
