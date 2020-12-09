# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class HatenaProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    """ItemをMongoDBに保存するpipeline"""

    def open_spider(self, spider):
        """
        spiderの開始時にmongodbに接続する
        :param spider:
        """
        self.client = MongoClient()
        self.db = self.client['scraping-book']
        self.collection = self.db['items']

    def close_spider(self, spider):
        """mongodbの終了時に接続切断"""
        self.client.close()

    def process_item(self, item, spider):
        """ itemをコレクションに追加"""
        self.collection.insert_one(dict(item))
        return item

