# -*- coding: utf-8 -*-
from rmq.items import RMQItem
from scrapy import Field


class ProductDetailItem(RMQItem):
    url = Field()
    external_id = Field()
    brand = Field()
    model = Field()
    category = Field()
    name = Field()
    images = Field()
    price = Field()
    parameters = Field()
    description = Field()
