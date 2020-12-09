#coding: UTF-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
from collections import defaultdict

from parse import parseText
from normalization import normalize
from stopwords import remove_stopwords

# https://qiita.com/YIPG/items/476c814ea6d548e070e5

def clustering(dic):

    df = pd.read_csv('./data/hateb.csv')
    td = []

    with open("./data/stop.txt", "r") as f:
        stop_list = [v.rstrip() for v in f.readlines() if v != '\n']

    # 1文書ずつ、単語に分割してリストに入れていく[([単語1,単語2,単語3],文書id),...]こんなイメージ
    # words：文書に含まれる単語のリスト（単語の重複あり）
    # tags：文書の識別子（リストで指定．1つの文書に複数のタグを付与できる）
    for i in range(len(df)):
        wordlist = parseText(text=str(df['content'][i]), sysdic=dic)
        # 単語の文字種の統一、つづりや表記揺れの吸収
        normalizedlist = [normalize(word) for word in wordlist]
        # ストップワードの除去
        stopremovedlist = remove_stopwords(normalizedlist, stop_list)
        td.append(TaggedDocument(words=stopremovedlist, tags=[i]))

    #モデル作成
    model = Doc2Vec(documents=td, dm = 1, vector_size=300, window=8, min_count=10, workers=4)

    #ベクトルをリストに格納
    vectors_list=[model.docvecs[n] for n in range(len(model.docvecs))]

    #ドキュメント番号のリスト
    doc_nums=range(len(model.docvecs))

    #クラスタリング設定
    #クラスター数を変えたい場合はn_clustersを変えてください
    n_clusters = 8
    kmeans_model = KMeans(n_clusters=n_clusters, verbose=1, random_state=1, n_jobs=-1)

    #クラスタリング実行
    kmeans_model.fit(vectors_list)

    #クラスタリングデータにラベル付け
    labels=kmeans_model.labels_

    #ラベルとドキュメント番号の辞書づくり
    cluster_to_docs = defaultdict(list)
    for cluster_id, doc_num in zip(labels, doc_nums):
        cluster_to_docs[cluster_id].append(doc_num)

    #クラスター出力
    for docs in cluster_to_docs.values():
        print(docs)


    # DataFrameにcluster_idのカラムを追加
    df['cluster_id'] = labels

    df.to_csv('data/hateb_cluster.csv')
