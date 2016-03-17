import sys
import pickle
import argparse

class CustomSentimentDictionary:
    """
    params:
        fileformat (int): 
           1. word, value
           2. word, positive value, negative value
           3. word, meaning, value
           4. See eriq's

        inputfile (string): 
           name of the file with the specified file format
    """
    def __init__(self, fileformat, inputfile):
        self.fileformat = fileformat
        self.dictionary = {}

        try: 
            if (fileformat == 1):
                with open(inputfile, 'r') as dictionary:
                    line = dictionary.readline()
                    line = line.split(',')
                    self.dictionary[line[0]] = line

            elif (fileformat == 2):
                with open(inputfile, 'r') as dictionary:
                    line = dictionary.readline()
                    line = line.split(',')
                    self.dictionary[line[0]] = line
        except IOError:
            print("Failed to open inputfile " + inputfile)
            sys.exit(1)

def ParseArguments():
    parser = argparse.ArgumentParser()

    # Arguments
    parser.add_argument('--fileformat', '-f', action='store', type=int, required=True,
            dest='fileformat', help='Format of dictionary:\n\t1. Word, Value\n\t' + 
            '2. Word, Positive, Negative')

    parser.add_argument('--input', '-i', action='store', required=True,
            dest='inputfile', help='file to read and convert into a custom' +
            ' dictionary')

    results, unknown = parser.parse_known_args()

    return results, unknown


def main():
    results, unknown = ParseArguments()

    customDictionary = CustomSentimentDictionary(results.fileformat, results.inputfile)

    pickleFile = open('pickle/CustomDictionary', 'wb')

    pickle.dump(customDictionary, pickleFile)

    pickleFile.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
