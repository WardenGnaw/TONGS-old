import sys
import nltk
import argparse
import SentimentEngine
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

   return parser.parse_known_args()

def main():
   results, unknown = ParseArguments()
   
   print("Welcome to the CLI for the SentimentEngine")
   while True:
      try:
         input = raw_input('> ')
         se = SentimentEngine.SentimentEngine(input)
         print se.getAggregiateSentenceSentiment()
      except EOFError:
         print("\nGoodbye")
         break

   return 0

if __name__ == "__main__":
   sys.exit(main())
