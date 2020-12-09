import os
import sys
import time
import datetime
import requests
import json
import pandas as pd

from typing import Tuple
import lxml.html
import re
import MeCab

url = 'https://qiita.com/api/v2/items'

with open('private.json') as f:
    token = json.load(f)['qiita_access_token']
h = {'Authorization': 'Bearer ' + token}

sleep_sec = 1.0

# BMP外を''に置換するマップ
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')

def get_string(html_text):
    html = lxml.html.fromstring(html_text)
    remove_tags = ('.//style', './/script', './/noscript')
    for remove_tag in remove_tags:
        for tag in html.findall(remove_tag):
            tag.drop_tree()
            # ここでの削除は元の変数tに反映されます。
    
    codeframe_list = []
    lang_list = []
    # コードの削除
    for tag in html.findall(".//div[@class='code-frame']"):
        codeframe_list.append(tag.text_content())
        lang_list.append(tag.attrib["data-lang"])
        tag.drop_tree()

    atext_list = []
    ahref_list = []
    # href　リンクの削除
    for tag in html.cssselect('a'):
        if tag.text is not None:
            atext_list.append(tag.text)
        if tag.get('href') is not None:
            ahref_list.append(tag.get('href'))
        tag.drop_tree()
        
    code_list = []
    # 一行コードの削除    
    for cc in  html.cssselect('code'):
        if cc.text is not None:
            code_list.append(cc.text)
        cc.drop_tree()
    
    text = html.text_content().strip('\n')

    return  pd.Series(["".join(text.split('\n')), ",".join(codeframe_list), ",".join(lang_list), ",".join(code_list), ",".join(atext_list), ",".join(ahref_list)], index=['text', 'code-frame', 'lang', 'code', 'a-text', 'a-href'])

def wakati(html):
    i = get_string(html)
    mecab = MeCab.Tagger ('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    return mecab.parse (i['text'])

def get_simple_df(df):
    df['tags_str'] = df['tags'].apply(
        lambda tags: ','.join(tag['name'] for tag in tags if not tag['name'] == '\x00')
    )
    df['title'] = df['title'].str.replace('\r', '').apply(lambda x : x.translate(non_bmp_map))
    df['article_id'] = df['id']
    df['html'] = df['rendered_body'].apply(lambda x : x.translate(non_bmp_map))
    df['created_at'] = df['created_at'].apply(lambda x : x[:19].replace('T', ' '))
    df['updated_at'] = df['updated_at'].apply(lambda x : x[:19].replace('T', ' '))

    wakati_list = []

    for i in df['html']:
        try:
            wakati_list.append(wakati(i))
        except:
            wakati_list.append('')
    
    df['tokens'] = pd.Series(wakati_list)

    df = df[['title', 'article_id', 'created_at', 'updated_at','likes_count', 'comments_count', 'tags_str',
               'user_id', 'user_permanent_id', 'url', 'html', 'tokens']]
    return df

# Qiitaから [start, end) の範囲で記事を取得
def get_items(start, end):
    start = start - datetime.timedelta(days=1)
    print('Fetching articles...')
    p = {
        'per_page': 100,
        'query': 'created:>{} created:<{}'.format(start, end)
    }

    time.sleep(sleep_sec)
    r = requests.get(url, params=p, headers=h)
    total_count = int(r.headers['Total-Count'])

    if total_count == 0:
        return

    df_list = [get_simple_df(pd.io.json.json_normalize(r.json(), sep='_'))]    

    if total_count > 100:
        for i in range(2, (total_count - 1) // 100 + 2):
            p['page'] = i
            time.sleep(sleep_sec)
            r = requests.get(url, params=p, headers=h)
            df_list.append(get_simple_df(pd.io.json.json_normalize(r.json(), sep='_')))

    df_all = pd.concat(df_list, ignore_index=True)
    print('{} articles fetched.'.format(len(df_all)))
    return df_all
