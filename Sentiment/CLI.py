import sys
import nltk
import argparse
from SentimentEngine import SentimentEngine
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
   
   if results.wordlist != "simple" and results.wordlist != "anew":
       print("Dictionary must be simple or anew")
       parser.print_help()
       sys.exit(1)

   return results, unknown


def promptUserInterface(sentence):
     print(sentence.rawSentence)
     while True:
         print("What would you like to do?:\n", \
               "\t1. All Information\n", \
               "\t2. getAggregiateSentenceSentiment\n", \
               "\t3. getAbsSentenceSentiment\n", \
               "\t4. getMaxSentenceSentiment\n", \
               "\t5. getMinSentenceSentiment\n", \
               "\t6. Exit\n")
         while True:
             inputLine = input('> ')
             try:
                 inputValue = int(inputLine)
                 if inputValue == 1 or inputValue == 2:
                     print("\tAggregiate Sentence Sentiment:", sentence.getAggregiateSentenceSentiment())
                 if inputValue == 1 or inputValue == 3:
                     print("\tAbs Sentence Sentiment:", sentence.getAbsSentenceSentiment())
                 if inputValue == 1 or inputValue == 4:
                     print("\tMax Sentence Sentiment:", sentence.getMaxSentenceSentiment())
                 if inputValue == 1 or inputValue == 5:
                     print("\tMin Sentence Sentiment:", sentence.getMinSentenceSentiment())
                 if 1 <= inputValue <= 5:
                     print()
                     break
                 if inputValue == 6:
                     return
                 raise ValueError
             except ValueError:
                 print("Please pick a number between 1 and 6")

def main():
   results, unknown = ParseArguments()
   
   print("Welcome to the CLI for the SentimentEngine")
   while True:
      try:
         print("Please type the sentence you want to grab sentiment from.")
         inputLine = input('> ')
         se = SentimentEngine(inputLine, results.wordlist)
         for sentence in se.getSentences():
             promptUserInterface(sentence)

      except EOFError:
         print("\nGoodbye")
         break

   return 0

if __name__ == "__main__":
   sys.exit(main())
