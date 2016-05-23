import java.io.*;
import java.util.List;
import java.util.Scanner;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.shiftreduce.ShiftReduceParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.Tree;

public class ShiftReduce {

  public static void main(String[] args) throws Exception {
    String modelPath = "edu/stanford/nlp/models/srparser/englishSR.ser.gz";
    String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

    for (int argIndex = 0; argIndex < args.length; ) {
      switch (args[argIndex]) {
        case "-tagger":
          taggerPath = args[argIndex + 1];
          argIndex += 2;
          break;
        case "-model":
          modelPath = args[argIndex + 1];
          argIndex += 2;
          break;
        default:
          throw new RuntimeException("Unknown argument " + args[argIndex]);
      }
    }

    MaxentTagger tagger = new MaxentTagger(taggerPath);
    ShiftReduceParser model = ShiftReduceParser.loadModel(modelPath);
    BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));

    while (true) {
      String input = bufferRead.readLine();
      if (":exit".equals(input)) {
        System.exit(0);
      }

      StringBuilder text = new StringBuilder();

      do {
        text.append(input);
        input = bufferRead.readLine();
      } while (!(":parse".equals(input)));

      DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text.toString()));

      for (List<HasWord> sentence : tokenizer) {
        List<TaggedWord> tagged = tagger.tagSentence(sentence);
        Tree tree = model.apply(tagged);
        System.out.println(tree);
      }

      System.out.println("** Success **");
    }
  }
}
