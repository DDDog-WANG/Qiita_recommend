import scrapy

from .broad import BroadSpider
from ..items import Page
from ..utils import get_content


class KnowledgeSpider(BroadSpider):
    name = 'knowledge'
    start_urls = ['http://b.hatena.ne.jp/entrylist/knowledge']

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, category="knowledge", title=title, html=response.text,
                   content=content)