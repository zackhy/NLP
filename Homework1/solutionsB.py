import sys
import nltk
import math
import time
from collections import Counter

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    for sentence in brown_train:
        tokens = sentence.strip().split()
        list1 = []
        list2 = []

        # Split words and tags by the last '/' using string.rfind()
        for words in tokens:
            position = words.rfind('/')
            list1.append(words[0:position])
            list2.append(words[position+1:])

        # Add START_SYMBOL and STOP_SYMBOL
        list1 = [START_SYMBOL, START_SYMBOL] + list1 + [STOP_SYMBOL]
        list2 = [START_SYMBOL, START_SYMBOL] + list2 + [STOP_SYMBOL]

        brown_words.append(list1)
        brown_tags.append(list2)
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    # Initialize Counter
    c1, c2 = Counter(), Counter()

    for sentence in brown_tags:
        # Count the number of bigram ('*', '*')
        c1[(START_SYMBOL, START_SYMBOL)] += 1
        # Count the number of bigrams and trigrams
        for position in range(len(sentence)):
            if (position > 0 and position < len(sentence) - 1):
                c1[(sentence[position], sentence[position + 1])] += 1
            if (position < len(sentence) - 2):
                c2[(sentence[position], sentence[position + 1], sentence[position + 2])] += 1

    # Calculate trigram probabilities
    q_values = {item: (math.log(c2[item], 2) - math.log(c1[(item[0], item[1])], 2)) for item in set(c2.elements())}

    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = []
    c = Counter()
    # Count the number of each word
    for sentence in brown_words:
        for words in sentence:
            c[words] += 1

    for key in c.keys():
        if c[key] > 5:
            known_words.append(key)
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []

    for sentence in brown_words:
        sentence_replace = []
        # Replace rare words with RARE_SYMBOL
        for words in sentence:
            if words in known_words:
                sentence_replace.append(words)
            else:
                sentence_replace.append(RARE_SYMBOL)
        brown_words_rare.append(sentence_replace)
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    taglist = []
    # Initialize counter
    c_tag, c_word_tag = Counter(), Counter()

    # Count the number of each tag and each (word, tag)
    for sentence, tags in zip(brown_words_rare, brown_tags):
        for word, tag in zip(sentence, tags):
            c_tag[tag] += 1
            c_word_tag[(word, tag)] += 1

    # Calculate emission probabilities
    e_values = {item: math.log(c_word_tag[item], 2) - math.log(c_tag[item[1]], 2) for item in c_word_tag}
    for tag in c_tag.keys():
        taglist.append(tag)
    
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []

    # Initialize pi and backpointers
    pi = {}
    bp = {}
    pi[1, START_SYMBOL, START_SYMBOL] = 0

    # Replace rare words with RARE_SYMBOL
    for sentence in brown_dev_words:
        sentence_replace = []
        sentence = [START_SYMBOL, START_SYMBOL] + sentence + [STOP_SYMBOL]
        for word in sentence:
            if word in known_words:
                sentence_replace.append(word)
            else:
                sentence_replace.append(RARE_SYMBOL)

        # Implement viterbi algorithm
        for k in range(2, len(sentence) - 1):
            # Calculate pi and backpointers using triple nested loop
            for u in taglist:
                for v in taglist:
                    word_tup = (sentence_replace[k], v)
                    max_prob = LOG_PROB_OF_ZERO
                    pointer = taglist[0]
                    for w in taglist:
                        last_tup = (k - 1, w, u)
                        tags_tup = (w, u, v)
                        if tags_tup in q_values and word_tup in e_values and last_tup in pi:
                            flag = q_values[tags_tup] + e_values[word_tup] + pi[last_tup]
                            if flag >= max_prob:
                                max_prob = flag
                                pointer = w

                    pi[k, u, v] = max_prob
                    bp[k, u, v] = pointer

        # Determine last two tags according to STOP_SYMBOL
        final_tup = (taglist[0], taglist[0])
        for u in taglist:
            for v in taglist:
                last_tup = (len(sentence) - 2, u, v)
                tags_tup = (u, v, STOP_SYMBOL)
                max_prob = LOG_PROB_OF_ZERO
                if last_tup in pi and tags_tup in q_values:
                    flag = pi[last_tup] + q_values[tags_tup]
                    if flag >= max_prob:
                        max_prob = flag
                        final_tup = (u, v)

        # Initialize tag_seq to store tag sequence in reverse order
        tag_seq = [None] * (len(sentence) - 3)
        tag_seq[0] = final_tup[1]
        tag_seq[1] = final_tup[0]

        # Determine highest scoring tag sequence using backpointers
        for k in range(len(sentence) - 5):
            tag_seq[k + 2] = bp[len(sentence) - 2 - k, tag_seq[k+1], tag_seq[k]]

        # Attach words with tags in 'WORD/TAG' format
        tagged_sent = ''
        for k in range(len(sentence) - 3):
            tagged_sent += sentence[k + 2] + '/' + tag_seq[-1 - k] + ' '

        tagged_sent += '\n'
        tagged.append(tagged_sent)

    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []

    # Set up default tagger
    default_tagger = nltk.DefaultTagger('NOUN')
    # Set up N-gram tagger
    bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    # Tag sentence and assign tagged sentence to tagged
    for sentence in brown_dev_words:
        tagged_list = trigram_tagger.tag(sentence)
        tagged_sentence = ''
        for item in tagged_list:
            tagged_sentence += item[0] + '/' + item[1] + ' '
        tagged_sentence += '\n'
        tagged.append(tagged_sentence)
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
