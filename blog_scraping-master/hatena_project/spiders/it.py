import scrapy

from .broad import BroadSpider
from ..items import Page
from ..utils import get_content


class ItSpider(BroadSpider):
    name = 'it'
    start_urls = ['http://b.hatena.ne.jp/entrylist/it']

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, category="it", title=title, html=response.text,
                   content=content)