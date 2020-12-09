# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class HatenaProjectItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class Page(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()

    def __repr__(self):
        """
        ログが出力時に長くなりすぎないようにcontentを省略する
        :return:
        """
        p = Page(self)  # pageを複製
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'

        return super(Page, p).__repr__()  # 複製したPageの文字列を返す
