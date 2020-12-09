# LDA_ou
# 読み込むコード
from gensim import corpora, models

corpus = corpora.MmCorpus("cop.mm")

lda = models.ldamodel.LdaModel.load("lda.model")

d = corpora.Dictionary.load_from_text("dict.txt")

doc_index = similarities.docsim.MatrixSimilarity.load("sim")
