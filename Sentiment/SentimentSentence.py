import nltk
from nltk.tokenize import TweetTokenizer
import SetupSentimentData

# Set up word lists to use for sentiment analysis.
negativeWordsList = SetupSentimentData.setupNegativeWordList()
positiveWordsList = SetupSentimentData.setupPositiveWordList() 
anewWordList = SetupSentimentData.setupANEWWordList() 
sentiWordNetList = SetupSentimentData.setupSentiWordNetList()
negationWords = ["no", "not", "doesn't", "neither", "don't"]

class SentimentSentence:
    def __init__(self, sentence, wordlist):
        self.rawSentence = sentence
        self.tokens = TweetTokenizer().tokenize(sentence)

        # Setup basic polarity
        self.polarity = 1

        for token in self.tokens:
            if token in negationWords:
                self.polarity = -1
                break

        self.pos = [pos[1] for pos in nltk.pos_tag(self.tokens)]
        self.wordsSentiment = [self.getWordSentiment(word, wordlist) for word in self.tokens]
        self.sentimentWordCount = sum(sentiment != 0 for sentiment in self.wordsSentiment)
        self.aggregateSentenceSentiment = sum(self.wordsSentiment)
        self.aggregateSentenceSentimentNormalized = sum(self.wordsSentiment)/float(1 if self.sentimentWordCount == 0 else self.sentimentWordCount)
        self.absSentenceSentiment = max([abs(i) for i in self.wordsSentiment])
        self.maxSentenceSentiment = max(self.wordsSentiment)
        self.minSentenceSentiment = min(self.wordsSentiment)
        self.polarizedWordSentiment = [self.getWordSentiment(word, wordlist) * self.polarity for word in self.tokens]
        self.aggregatePolarizedSentenceSentiment = sum(self.polarizedWordSentiment)
        self.aggregatePolarizedSentenceSentimentNormalized = sum(self.polarizedWordSentiment)/float(1 if self.sentimentWordCount == 0 else self.sentimentWordCount)

    @staticmethod
    def getWordSentiment(word, wordlist):
        word = word.lower()

        if wordlist == "simple":
            if word in negativeWordsList:
                return -1
            if word in positiveWordsList:
                return 1

        elif wordlist == "anew":
            if word in anewWordList:
                return anewWordList[word].valence

        # Word not found
        return 0

    def getRawSentence(self):
        return self.rawSentence

    def getTokens(self):
        return self.tokens

    def getPartsOfSpeech(self):
        return self.pos

    def getPolarity(self):
        return self.polarity

    def getWordsSentiment(self):
        return self.wordsSentiment

    def getSentimentWordCount(self):
        return self.sentimentWordCount

    def getAggregateSentenceSentiment(self):
        return self.aggregateSentenceSentiment

    def getAggregateSentenceSentimentNormalized(self):
        return self.aggregateSentenceSentimentNormalized

    def getAbsSentenceSentiment(self):
        return self.absSentenceSentiment

    def getMaxSentenceSentiment(self):
        return self.maxSentenceSentiment

    def getMinSentenceSentiment(self):
        return self.minSentenceSentiment

    def getPolarizedSentenceSentiment(self):
        return self.polarizedWordSentiment

    def getAggregatePolarizedSentenceSentiment(self):
        return self.aggregatePolarizedSentenceSentiment

    def getAggregatePolarizedSentenceSentimentNormalized(self):
        return self.aggregatePolarizedSentenceSentimentNormalized 
