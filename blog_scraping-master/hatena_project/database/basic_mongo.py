from bson import ObjectId
from pymongo import MongoClient, response
from datetime import datetime
from extractcontent3 import ExtractContent

from master_key import mongo_key
# 同じディレクトリ にmaster_key.pyを作成し、そこにmongo_keyを追加する


class Mongo(object):
    def __init__(self):
        self.client = MongoClient(mongo_key)
        self.db = self.client['test']
        self.collection = self.db['hateb']

    def add_one(self):
        """データ挿入"""
        post = {
            'url': 'ハリネズミ',
            'title': 'ハリネズミ可愛い~',
            'html': datetime.now()
        }
        return self.collection.insert_one(post)

    def get_one(self):
        return self.collection.find_one()

    def get_from_oid(self, oid):
        return self.db.test.find_one({'_id': ObjectId(oid)})

    def delete(self):
        """マッチした最初のデータを削除"""
        rest = self.db.test.delete_one({"title": "ハムスター"})
        return rest

    def content_update(self, title, content):
        rest = self.collection.update_one({"title": title}, {"$set": {"content": content}})
        return rest

    def get_content(self, html):
        extractor = ExtractContent()
        extractor.analyse(html)
        text, title = extractor.as_text()
        return text

    def pad(self):
        """
        contentカラムで取れていない物（空欄）を埋める
        """
        find = self.collection.find(filter={'content': ''})
        for doc in find:
            content = self.get_content(doc['html'])
            self.content_update(doc['title'], content)

    def count_pad(self):
        """
        contentカラムの空欄の数を表示
        """
        find = self.collection.find(filter={'content': ''})
        print(find.count())


def main():
    # Mongo().pad()
    mon = Mongo()
    mon.count_pad()
    # Mongo().count_pad()


if __name__ == '__main__':
    main()