import sys
import nltk
from nltk.tokenize import sent_tokenize
from SentimentSentence import SentimentSentence

class SentimentEngine:
    def __init__(self, data, wordlist):
        self.tokenized_sentences = sent_tokenize(data)
        self.sentiment_sentences = []

        for sentence in self.tokenized_sentences:
            self.sentiment_sentences.append(SentimentSentence(sentence, wordlist))

    def getSentences(self):
        return self.sentiment_sentences
