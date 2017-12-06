from gensim import models
import nltk
import pandas as pd

wvec = models.Word2Vec
import os
MODEL_NAME = 'w2vmodel'

if os.path.exists(MODEL_NAME):
    model = wvec.load(MODEL_NAME)
else:
    # os.chdir('TrippyMain/AI')
    df_all = pd.read_pickle('../Warehouse/UdpRevFin.pkl')
    all_text = '. '.join(list(df_all['Text']))
    pk = nltk.PunktSentenceTokenizer()
    sentences = [nltk.word_tokenize(i) for i in pk.tokenize(all_text)]
    model = wv(sentences, min_count=5, size=500, workers=3)
    model.save(MODEL_NAME)


def sim(a, b):
    return model.wv.similarity(a, b)
