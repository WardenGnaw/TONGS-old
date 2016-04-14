import nltk
from nltk.tokenize import TweetTokenizer
import SetupSentimentData
from nltk.corpus import sentiwordnet as swn
from nltk.wsd import lesk

# Speed up tagging
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()

# Set up word lists to use for sentiment analysis.
negativeWordsList = SetupSentimentData.setupNegativeWordList()
positiveWordsList = SetupSentimentData.setupPositiveWordList() 
anewWordList = SetupSentimentData.setupANEWWordList() 
negationWords = ["no", "not", "doesn't", "neither", "don't", "wasn't", "couldn't", "haven't"]


class InvalidDictionaryException(Exception):
    pass

def convertPOSTagToSimplePOS(pos):
    if pos == "NN":
        return 'n'
    elif pos == "VB":
        return 'v'
    elif pos == "JJ":
        return 'a'
    elif pos == "RB":
        return 'r'
    else:
        return None


class SentimentSentence:
    def __init__(self, sentence, wordlist):
        self.rawSentence = sentence
        self.tokens = TweetTokenizer().tokenize(sentence)
        self.wordlist = wordlist

        # Setup basic polarity
        self.polarity = 1

        # Naive version of detection of a negated sentence.
        for token in self.tokens:
            if token in negationWords:
                self.polarity = -1
                break

        self.pos = [pos[1] for pos in nltk.tag._pos_tag(self.tokens, None, tagger)]
        self.wordsSentiment = [self.getWordSentiment(word, wordlist) for word in self.tokens]
        if wordlist == "sentiwordnet":
            self.wordsSentimentTuple = [self.getWordSentimentTuple(self.tokens[i], self.pos[i], wordlist) for i in range(0, len(self.tokens))]
        if self.wordsSentiment:
            self.sentimentWordCount = sum(sentiment != 0 for sentiment in self.wordsSentiment)
            self.aggregateSentenceSentiment = sum(self.wordsSentiment)
            self.aggregateSentenceSentimentNormalized = sum(self.wordsSentiment)/float(1 if self.sentimentWordCount == 0 else self.sentimentWordCount)
            self.absSentenceSentiment = max([abs(i) for i in self.wordsSentiment])
            self.maxSentenceSentiment = max(self.wordsSentiment)
            self.minSentenceSentiment = min(self.wordsSentiment)
        else:
            self.sentimentWordCount = 0
            self.aggregateSentenceSentiment = 0
            self.aggregateSentenceSentimentNormalized = 0
            self.absSentenceSentiment = 0
            self.maxSentenceSentiment = 0
            self.minSentenceSentiment = 0

        self.polarizedWordSentiment = [self.getWordSentiment(word, wordlist) * self.polarity for word in self.tokens]
        if self.polarizedWordSentiment:
            self.aggregatePolarizedSentenceSentiment = sum(self.polarizedWordSentiment)
            self.aggregatePolarizedSentenceSentimentNormalized = sum(self.polarizedWordSentiment)/float(1 if self.sentimentWordCount == 0 else self.sentimentWordCount)
        else:
            self.aggregatePolarizedSentenceSentiment = 0
            self.aggregatePolarizedSentenceSentimentNormalized = 0


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

    def getWordSentimentTuple(self, word, pos, wordlist):
        if wordlist != "sentiwordnet":
            raise InvalidDictionaryException("Invalid dictionary " + wordlist + \
                    "please use sentiwordnet")
        else:
            simplePOS = convertPOSTagToSimplePOS(pos)
            if pos:
                wordSense = lesk(self.tokens, word, simplePOS)
                if wordSense: 
                   sentiSynsetWord = swn.senti_synset(wordSense.name())
                   if sentiSynsetWord:
                       return (sentiSynsetWord.pos_score(), 
                               sentiSynsetWord.neg_score(),
                               sentiSynsetWord.obj_score())

        return (0, 0, 0)

    def getRawSentence(self):
        return self.rawSentence

    def getTokens(self):
        return self.tokens

    def getPartsOfSpeech(self):
        return self.pos

    def getPolarity(self):
        return self.polarity

    def getWordsSentiment(self):
        if self.wordlist == "sentiwordnet":
            return self.wordsSentimentTuple
        else:
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
