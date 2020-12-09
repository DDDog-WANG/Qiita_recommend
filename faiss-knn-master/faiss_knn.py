import numpy as np
import pandas as pd
import time
import glob
import faiss
import sys

from database import get_article_features

vec_path = 'data/vec2.csv'

print('Loading csv...')
df_vec = pd.read_csv(vec_path)

dic = {}
for i, id in enumerate(df_vec['article_id']):
    dic[id] = i


def parseVector(string):
    lst = string.strip('[]').replace(' ', '').split(',')
    v = [float(i) for i in lst]
    return v

print('Creating NumPy array...')

vec = [parseVector(s) for s in df_vec['vector']]
df_vec = df_vec.drop('vector', axis=1)

dim = len(vec[0])   # ベクトルの次元(dimension)

arr_b = np.array(vec).astype('float32')
del(vec)

print('Building index...')
index = faiss.IndexFlatL2(dim)
index.add(arr_b)

def search_knn(id_list, count):
    s = time.time()
    nq = len(id_list)
    arr_q = np.empty((nq, dim)).astype('float32')
    for i, id in enumerate(id_list):
        arr_q[i] = arr_b[dic[id]]

    D_all, I_all = index.search(arr_q, count)

    res = {}
    for D, I, qid in zip(D_all, I_all, id_list):
        inner_res = {}
        for d, i in zip(D, I):
            id = df_vec['article_id'][i]
            feature = get_article_features(id)
            feature['distance'] = float(d)
            feature['topic_id'] = int(np.argmax(arr_b[i]))
            feature['created_at'] = str(feature['created_at'])
            inner_res[id] = feature      
        res[qid] = inner_res

    e = time.time()
    print("search time: {}".format(e-s))
    
    return res
