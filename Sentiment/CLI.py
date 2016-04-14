import sys
import nltk
import argparse
from SentimentEngine import SentimentEngine
import json
import re

"""
Setup and parse arguments.

Returns both known argument list and unknown arguments list
"""
def ParseArguments():
   parser = argparse.ArgumentParser()

   # Arguments
   parser.add_argument('--verbose', '-v', action='store_true', 
                       help='turn on verbose mode')
   parser.add_argument('--input', '-i', action='store', dest='inputFile', 
                       help='file to read from')
   parser.add_argument('--output', '-o', action='store', dest='outputFile', 
                       help='file to write to')
   parser.add_argument('--dictionary', '-d', action='store', dest='wordlist', 
                       default="simple",
                       help='Dictionary to use (simple or anew). Defaults to simple.')

   results, unknown = parser.parse_known_args()
   
   
   if results.wordlist != "simple" and results.wordlist != "anew" and \
    results.wordlist != "sentiwordnet":
       print("Dictionary must be simple, anew, or sentiwordnet")
       parser.print_help()
       sys.exit(1)

   return results, unknown


def printData(sentence, wordlist):
    print("Raw Sentence:", sentence.getRawSentence())
    print("Tokens:", sentence.getTokens())
    print("Parts of Speech:", sentence.getPartsOfSpeech())
    print("Polarity:", sentence.getPolarity())
    if wordlist != "sentiwordnet":
        print("Words Sentiment:", sentence.getWordsSentimentTuple())
    else:
        print("Words Sentiment:", sentence.getWordsSentiment())
    print("Sentiment Word Count:", sentence.getSentimentWordCount())
    print("Aggregate Sentence Sentiment:", sentence.getAggregateSentenceSentiment())
    print("Aggregate Sentence Sentimate Normalized:", sentence.getAggregateSentenceSentimentNormalized())
    print("Abs Sentence Sentiment:", sentence.getAbsSentenceSentiment())
    print("Max Sentence Sentiment:", sentence.getMaxSentenceSentiment())
    print("Min Sentence Sentiment:", sentence.getMinSentenceSentiment())
    print("Polarized Sentence Sentiment:", sentence.getPolarizedSentenceSentiment())
    print("Aggregate Polarized Sentence Sentiment:", sentence.getAggregatePolarizedSentenceSentiment())
    print("Aggregate Polarized Sentence Sentiment Normalized:", sentence.getAggregatePolarizedSentenceSentimentNormalized())

def main():
   results, unknown = ParseArguments()
   
   if results.inputFile:
       suffix = results.inputFile.split('.')[-1]
       if suffix == 'json':
           f = open(results.inputFile, 'r')
           data = json.load(f)
           for key in data.keys():
               regex = re.compile(r'[\n\r\t]')
               arr = regex.sub('', "".join(data[key]))
               se = SentimentEngine(arr, results.wordlist)
               rating = 0
               for sentence in se.getSentences():
                   rating = rating + sentence.getAggregatePolarizedSentenceSentiment()

               print(key, rating)



   else:
       print("Welcome to the CLI for the SentimentEngine")
       while True:
          try:
             print("Please type the sentence you want to grab sentiment from.")
             inputLine = input('> ')
             se = SentimentEngine(inputLine, results.wordlist)
             for sentence in se.getSentences():
                 printData(sentence, results.wordlist)

          except EOFError:
             print("\nGoodbye")
             break

   return 0

if __name__ == "__main__":
   sys.exit(main())
