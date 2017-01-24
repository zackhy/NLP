import nltk
import time

# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm = nltk.IBMModel1(aligned_sents, 10)
    return ibm

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm = nltk.IBMModel2(aligned_sents, 10)
    return ibm

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    aer = 0.0
    for i in range(n):
        sentence = model.align(aligned_sents[i])
        aer += aligned_sents[i].alignment_error_rate(sentence)
    return aer/n

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    with open(file_name, "w") as file:
        for i in range(20):
            aligned_model = model.align(aligned_sents[i])
            words = str(aligned_model.words)
            mots = str(aligned_model.mots)
            align = str(aligned_model.alignment)

            file.write(words + '\n' + mots + '\n' + align + '\n\n')

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)

    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

# def main(aligned_sents):
#     for i in range(20):
#         start_time = time.clock()
#         ibm1 = nltk.IBMModel1(aligned_sents, i)
#         avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)
#         end_time = time.clock()
#         runtime = end_time - start_time
#         print ('The number of iterations:' + str(i))
#         print ('IBM Model 1')
#         print ('---------------------------')
#         print ('Average AER: {0:.3f}'.format(avg_aer))
#         print ('Time:' + str(runtime))
#         print ('\n')
#
#     for i in range(20):
#         start_time = time.clock()
#         ibm2 = nltk.IBMModel2(aligned_sents, i)
#         avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
#         end_time = time.clock()
#         runtime = end_time - start_time
#         print ('The number of iterations:' + str(i))
#         print ('IBM Model 2')
#         print ('---------------------------')
#         print ('Average AER: {0:.3f}'.format(avg_aer))
#         print ('Time:' + str(runtime))
#         print ('\n')


