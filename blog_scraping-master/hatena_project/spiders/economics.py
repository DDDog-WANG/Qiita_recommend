import scrapy

from .broad import BroadSpider
from ..items import Page
from ..utils import get_content


class EconomicsSpider(BroadSpider):
    name = 'economics'
    start_urls = ['http://b.hatena.ne.jp/entrylist/economics']

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, category="economics", title=title, html=response.text,
                   content=content)