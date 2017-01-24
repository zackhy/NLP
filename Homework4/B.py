from __future__  import division
import nltk
import A
from collections import defaultdict
from nltk import AlignedSent
from nltk.align import Alignment

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        min_prob = 1.0e-12
        words_len = len(align_sent.words)
        mots_len = len(align_sent.mots)
        alignment = []

        for i, en_word in enumerate(align_sent.words):
            max_prob = max(self.t[en_word][None] * self.q[0][i+1][words_len][mots_len], min_prob)
            best_point = None
            for j, ge_word in enumerate(align_sent.mots):
                align_prob = self.t[en_word][ge_word] * self.q[j+1][i+1][words_len][mots_len]
                if align_prob >= max_prob:
                    max_prob = align_prob
                    best_point = j
            if (best_point is not None):
                alignment.append((i, best_point))

        return AlignedSent(align_sent.words, align_sent.mots, Alignment(alignment))

    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        min_prob = 1.0e-12
        t_ef = nltk.IBMModel1(aligned_sents, 6).probabilities
        rev_aligned_sents = []
        for sentence in aligned_sents:
            rev_aligned_sents.append(sentence.invert())
        t_fe = nltk.IBMModel1(rev_aligned_sents, 6).probabilities

        # Vocabulary
        en_vocab = set()
        ge_vocab = set()
        for sentence in aligned_sents:
            en_vocab.update(sentence.words)
            ge_vocab.update(sentence.mots)
        ge_vocab.add(None)
        en_vocab.add(None)

        q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))
        rev_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))

        # Initialization
        for sentence in aligned_sents:
            en = [None] + sentence.words
            ge = [None] + sentence.mots
            l_e = len(en) - 1
            l_f = len(ge) - 1
            x = 1 / (l_f + 1)
            for i in xrange(0, l_f + 1):
                for j in xrange(1, l_e + 1):
                    q[i][j][l_e][l_f] = x
            y = 1 / (l_e + 1)
            for i in xrange(0, l_e + 1):
                for j in xrange(1, l_f + 1):
                    rev_q[i][j][l_f][l_e] = y

        # Implement EM algorithm
        for k in xrange(0, num_iters):
            ct_ef = defaultdict(lambda: defaultdict(lambda: min_prob))
            ct_fe = defaultdict(lambda: defaultdict(lambda: min_prob))
            total_f = defaultdict(lambda: min_prob)
            ct_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))
            total_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob)))
            rev_ct_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))
            rev_total_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob)))
            total_e = defaultdict(lambda: min_prob)
            denominator = defaultdict(lambda: min_prob)
            rev_denominator = defaultdict(lambda: min_prob)

            for sentence in aligned_sents:
                en = [None] + sentence.words
                ge = [None] + sentence.mots
                l_f = len(ge) - 1
                l_e = len(en) - 1

                # Normalization
                for j in xrange(1, l_e + 1):
                    en_word = en[j]
                    denominator[en_word] = 0
                    for i in xrange(0, l_f + 1):
                        denominator[en_word] += t_ef[en_word][ge[i]] * q[i][j][l_e][l_f]
                for j in xrange(1, l_f + 1):
                    ge_word = ge[j]
                    rev_denominator[ge_word] = 0
                    for i in xrange(0, l_e + 1):
                        rev_denominator[ge_word] += t_fe[ge_word][en[i]] * rev_q[i][j][l_f][l_e]

                # Collect counts
                for j in xrange(1, l_e + 1):
                    en_word = en[j]
                    for i in xrange(0, l_f + 1):
                        ge_word = ge[i]
                        c = t_ef[en_word][ge_word] * q[i][j][l_e][l_f] / denominator[en_word]
                        ct_ef[en_word][ge_word] += c
                        total_f[ge_word] += c
                        ct_q[i][j][l_e][l_f] += c
                        total_q[j][l_e][l_f] += c

                for j in xrange(1, l_f + 1):
                    ge_word = ge[j]
                    for i in xrange(l_e + 1):
                        en_word = en[i]
                        c = t_fe[ge_word][en_word] * rev_q[i][j][l_f][l_e] / rev_denominator[ge_word]
                        ct_fe[ge_word][en_word] += c
                        total_e[en_word] += c
                        rev_ct_q[i][j][l_f][l_e] += c
                        rev_total_q[j][l_f][l_e] += c

            for en in ct_ef:
                for ge in ct_ef[en]:
                    ct_ef[en][ge] = (ct_ef[en][ge] + ct_fe[ge][en]) * 0.5
                    ct_fe[ge][en] = ct_ef[en][ge]

            for sentence in aligned_sents:
                src = [None] + sentence.words
                tar = [None] + sentence.mots
                l_src = len(src) - 1
                l_tar = len(tar) - 1

                for j in xrange(1, l_src + 1):
                    for i in xrange(0, l_tar + 1):
                        ct_q[i][j][l_src][l_tar] = (ct_q[i][j][l_src][l_tar] + rev_ct_q[j][i][l_tar][l_src]) / 2
                        rev_ct_q[j][i][l_tar][l_src] = ct_q[i][j][l_src][l_tar]

            t_ef = defaultdict(lambda: defaultdict(lambda: min_prob))
            q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))
            t_fe = defaultdict(lambda: defaultdict(lambda: min_prob))
            rev_q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: min_prob))))

            for f in ge_vocab:
                for e in en_vocab:
                    t_ef[e][f] = ct_ef[e][f] / total_f[f]
            for e in en_vocab:
                for f in ge_vocab:
                    t_fe[f][e] = ct_fe[f][e] / total_e[e]

            for sentence in aligned_sents:
                en = [None] + sentence.words
                ge = [None] + sentence.mots
                l_f = len(ge) - 1
                l_e = len(en) - 1
                for i in xrange(0, l_f + 1):
                    for j in xrange(1, l_e + 1):
                        q[i][j][l_e][l_f] = ct_q[i][j][l_e][l_f] / total_q[j][l_e][l_f]

                for i in xrange(0, l_e + 1):
                    for j in xrange(1, l_f + 1):
                        rev_q[i][j][l_f][l_e] = rev_ct_q[i][j][l_f][l_e] / \
                                                        rev_total_q[j][l_f][l_e]
        return (t_ef, q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

