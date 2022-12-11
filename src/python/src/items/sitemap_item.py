# -*- coding: utf-8 -*-
from scrapy import Field, Item


class SitemapItem(Item):
    url = Field()
