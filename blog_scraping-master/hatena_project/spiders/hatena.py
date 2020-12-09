import scrapy

from ..items import Page
from ..utils import get_content


class HatenaSpider(scrapy.Spider):
    name = 'hatena'
    #  はてなブックマークの新着エントリページ
    start_urls = ['https://blog.hatenablog.com/archive/category/%E3%83%96%E3%82%AF%E3%83%9E%E6%95%B0%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0']

    def parse(self, response):
        """
        個別のwebページのリンクをたどる
        :param response:
        """
        for url in response.css('section.archive-entry>div>h1>a::attr("href")').getall():
            #  parser_pageをコールバック関数として指定する
            yield scrapy.Request(url, callback=self.week_page)

    def week_page(self, response):
        for url in response.css('table>tr>td>a:nth-child(2)::attr("href")').getall():
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, title=title, html=response.text,
                   content=content)
