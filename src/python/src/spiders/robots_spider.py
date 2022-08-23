# -*- coding: utf-8 -*-
import re
import traceback

from scrapy.spiders import Spider
from rmq.utils import get_import_full_name

from pipelines import SitemapDBPipeline
from items import SitemapItem


class RobotsSpider(Spider):
    name = 'robots'
    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(SitemapDBPipeline): 310},
    }

    allowed_domains = ['www.bi-bi.com.ua']
    start_urls = ['https://bi-bi.com.ua/robots.txt']

    def parse(self, response):
        try:
            sitemaps = re.findall(r'Sitemap:\s(.*?.xml)', response.text)
            if sitemaps:
                for sitemap in sitemaps:
                    yield SitemapItem({"url": sitemap})
            else:
                raise Exception("Failed to find sitemaps")
        except Exception as e:
            self.logger.error(e)
            self.logger.warning(traceback.format_exc())
