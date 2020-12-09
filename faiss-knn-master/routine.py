import pandas as pd
import datetime

from database import insert_article_data, get_article_tokens, insert_vector_data
from get_content import get_items
from vectorize import vectorize

vec_path = './data/test.csv'

end = datetime.date.today()
start = end - datetime.timedelta(days=1)

df = get_items(start, end)
insert_article_data(df)

df = df[['article_id', 'tokens']]
df = vectorize(df)
insert_vector_data(df)
df.to_csv(vec_path, mode='a', index=False)
