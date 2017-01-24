from nltk.corpus import comtrans
import A
import B

if __name__ == '__main__':
    aligned_sents = comtrans.aligned_sents()[:350]
    A.main(aligned_sents)
    B.main(aligned_sents)
