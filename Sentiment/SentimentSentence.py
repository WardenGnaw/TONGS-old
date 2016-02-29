import nltk
from nltk.tokenize import TweetTokenizer
import SetupSentimentData

# Set up word lists to use for sentiment analysis.
negativeWordsList = SetupSentimentData.setupNegativeWordList()
positiveWordsList = SetupSentimentData.setupPositiveWordList() 
anewWordList = SetupSentimentData.setupANEWWordList() 
sentiWordNetList = SetupSentimentData.setupSentiWordNetList()
negationWords = ["no", "not", "doesn't", "neither"]

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
        self.aggregiateSentenceSentiment = sum(self.wordsSentiment)
        self.absSentenceSentiment = max([abs(i) for i in self.wordsSentiment])
        self.maxSentenceSentiment = max(self.wordsSentiment)
        self.minSentenceSentiment = min(self.wordsSentiment)
        self.polarizedWordSentiment = [self.getWordSentiment(word, wordlist) * self.polarity for word in self.tokens]
        self.aggregiatePolarizedSentenceSentiment = sum(self.polarizedWordSentiment)

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


    def getAggregiateSentenceSentiment(self):
        return self.aggregiateSentenceSentiment 

    def getAbsSentenceSentiment(self):
        return self.absSentenceSentiment

    def getMaxSentenceSentiment(self):
        return self.maxSentenceSentiment
    
    def getMinSentenceSentiment(self):
        return self.minSentenceSentiment
