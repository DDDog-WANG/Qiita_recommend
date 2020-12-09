import scrapy

from .broad import BroadSpider
from ..items import Page
from ..utils import get_content


class FunSpider(BroadSpider):
    name = 'fun'
    start_urls = ['http://b.hatena.ne.jp/entrylist/fun']

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, category="fun", title=title, html=response.text,
                   content=content)