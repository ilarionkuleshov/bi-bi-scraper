# -*- coding: utf-8 -*-
from rmq.items import RMQItem
from scrapy import Field


class SerpPageItem(RMQItem):
    url = Field()
    brand = Field()
    model = Field()
    category = Field()
    subcategory = Field()
