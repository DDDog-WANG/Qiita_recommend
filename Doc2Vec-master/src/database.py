import os
import pandas as pd
from pymongo import MongoClient

from stopwords import maybe_download


if not os.path.exists('./data'):
    os.mkdir('./data')

url = open('dbserver', 'r').read()

# MongoDBに接続し, テキストデータを取得
client = MongoClient(url)
collection = client['test']['hateb']

df = pd.DataFrame.from_dict(list(collection.find())).astype(object)
pd.DataFrame.to_csv(df, './data/hateb.csv')

# ストップワード一覧を取得
maybe_download("./data/stop.txt")
