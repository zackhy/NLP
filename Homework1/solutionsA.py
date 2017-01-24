import math
import nltk
import time
from collections import Counter

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    # Initialize counter
    c1, c2, c3 = Counter(), Counter(), Counter()
    c = 0

    for sentence in training_corpus:
        sentence = (START_SYMBOL + " ")*2 + sentence + " " + STOP_SYMBOL
        tokens = sentence.strip().split()
        # Add the number of (START_SYMBOL,) to unigram and (START_SYMBOL, START_SYMBOL) to bigram
        # in order to calculate bigram possibilities and trigram possibilities
        c1[(START_SYMBOL,)] += 1
        c2[(START_SYMBOL, START_SYMBOL)] += 1
        c += 1

        # Count the number of each unigram, bigram and trigram
        for position in range(len(tokens)):
            # Unigram should not include any START_SYMBOL
            if(position > 1):
                c1[(tokens[position],)] += 1
            # Bigram should include only one START_SYMBOL
            if(position > 0 and position < len(tokens) - 1):
                c2[(tokens[position], tokens[position + 1])] += 1
            # Trigram should include two START_SYMBOLs
            if(position < len(tokens) - 2):
                c3[(tokens[position], tokens[position + 1], tokens[position + 2])] += 1

    # Since we added the number of START_SYMBOL to unigram before, we should get rid of it here
    unigram_sum = sum(c1.values()) - c
    # Calculate possibilities for unigram, bigram and trigram
    unigram_p = {item: (math.log(c1[item], 2) - math.log(unigram_sum, 2)) for item in set(c1.elements())}
    bigram_p = {item: (math.log(c2[item], 2) - math.log(c1[(item[0],)], 2)) for item in set(c2.elements())}
    trigram_p = {item: (math.log(c3[item], 2) - math.log(c2[(item[0], item[1])], 2)) for item in set(c3.elements())}

    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []

    # when import unigram
    if(n == 1):
        for sentence in corpus:
            sentence_score = 0
            sentence = sentence + " " + STOP_SYMBOL
            tokens = sentence.strip().split()

            # Calculate sentence scores
            for words in tokens:
                try:
                    sentence_score += ngram_p[(words,)]
                # Set sentence score to -1000 when any unigram in sentence doesn't exist in corpus
                except:
                    sentence_score = MINUS_INFINITY_SENTENCE_LOG_PROB

            scores.append(sentence_score)

    # when import bigram
    if(n == 2):
        for sentence in corpus:
            sentence_score = 0
            sentence = (START_SYMBOL + " ") * 2 + sentence + " " + STOP_SYMBOL
            tokens = sentence.split()

            for position in range(len(tokens)):
                if (position < len(tokens) - 1):
                    try:
                        sentence_score += ngram_p[(tokens[position], tokens[position + 1])]
                    except:
                        sentence_score = MINUS_INFINITY_SENTENCE_LOG_PROB

            scores.append(sentence_score)

    # when import trigram
    if(n == 3):
        for sentence in corpus:
            sentence_score = 0
            sentence = (START_SYMBOL + " ")*2 + sentence + " " + STOP_SYMBOL
            tokens = sentence.split()

            for position in range(len(tokens)):
                if (position < len(tokens) - 2):
                    try:
                        sentence_score += ngram_p[(tokens[position], tokens[position + 1], tokens[position + 2])]
                    except:
                        sentence_score = MINUS_INFINITY_SENTENCE_LOG_PROB

            scores.append(sentence_score)

    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []

    for sentence in corpus:
        sentence_score = 0
        sentence = (START_SYMBOL + " ") * 2 + sentence + " " + STOP_SYMBOL
        tokens = sentence.strip().split()

        # Implement linear interpolation among the three n-gram models
        for word1, word2, word3 in zip(tokens[0::1], tokens[1::1], tokens[2::1]):
            if((word3,) in unigrams and (word2, word3) in bigrams and (word1, word2, word3) in trigrams):
                uni_score = 2**unigrams[(word3,)]
                bi_score = 2**bigrams[(word2, word3)]
                tri_score = 2**trigrams[(word1, word2, word3)]
                sentence_score += math.log((uni_score + bi_score + tri_score), 2) + math.log(1, 2) - math.log(3, 2)
            # Set sentence score to -1000 when any unigram in sentence doesn't exist in corpus
            else:
                sentence_score = MINUS_INFINITY_SENTENCE_LOG_PROB
                break

        scores.append(sentence_score)

    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
