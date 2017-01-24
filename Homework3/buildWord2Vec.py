import json
import numpy as np
import gensim
from gensim.models import Word2Vec

with open('hist_split.json') as f:
    data = f.read()
    train_data = json.loads(data)['train']
    sentences = []
    for item in train_data:
        sentence = []
        for word in item[0]:
            if word[0] == None:
                sentence.append(u"None")
            else:
                sentence.append(word[0])
        sentences.append(sentence)

model = gensim.models.Word2Vec(size=100, window=5, min_count=1)
model.build_vocab(sentences)
alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes

for epoch in range(passes):
    model.alpha, model.min_alpha = alpha, alpha
    model.train(sentences)

    print('completed pass %i at alpha %f' % (epoch + 1, alpha))
    alpha -= alpha_delta

    np.random.shuffle(sentences)

model.save('word2vec_file')
