import scrapy

from .broad import BroadSpider
from ..items import Page
from ..utils import get_content


class SocialSpider(BroadSpider):
    name = 'social'
    start_urls = ['http://b.hatena.ne.jp/entrylist/social']

    def parse_page(self, response):
        title, content = get_content(response.text)
        yield Page(url=response.url, category="social", title=title, html=response.text,
                   content=content)