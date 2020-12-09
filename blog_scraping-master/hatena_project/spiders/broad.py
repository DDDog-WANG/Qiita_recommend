import scrapy

from ..items import Page
from ..utils import get_content


class BroadSpider(scrapy.Spider):
    name = 'broad'
    #  はてなブックマークの新着エントリページ
    start_urls = ['http://b.hatena.ne.jp/entrylist/all']

    def parse(self, response):
        """
        個別のwebページのリンクをたどる
        :param response:
        """
        for url in response.css('.entrylist-contents-title > a::attr("href")').getall():
            #  parser_pageをコールバック関数として指定する
            yield scrapy.Request(url, callback=self.parse_page)

        #  page=の値が1桁の場合次の二十軒のリンクをたどる
        url_more = response.css('.entrylist-readmore > a::attr("href")').re_first(r'.*\?page=\d{1}$')
        if url_more:
            yield response.follow(url_more)

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, title=title, html=response.text,
                   content=content)
