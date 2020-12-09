from natto import MeCab
import logging

'''
引数の文字列に対して形態素解析を行う.
名詞, 動詞, 形容詞, 形容動詞のみを抽出し, 単語のリストとして返す.
'''
def parseText(text, sysdic='/usr/local/lib/mecab/dic/mecab-ipadic-neologd'):
    text = text.split("\n") #改行で分割して配列にする
    while '' in text: #空行は削除
        text.remove('')
    
    parser = MeCab("-d " + sysdic)
    lst = []
    
    for sentence in text:
        logging.debug(sentence)
        nodes = parser.parse(sentence, as_nodes=True)

        for node in nodes:
            features = node.feature.split(',')
            parts = features[0]
            if parts == '名詞':
                lst.append(node.surface)
            if parts in {'動詞', '形容詞', '形容動詞'}:
                lst.append(features[6])

    return lst
