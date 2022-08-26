# -*- coding: utf-8 -*-
from rmq.items import RMQItem
from scrapy import Field


class ProductDetailItem(RMQItem):
    id = Field()
    url = Field()
    external_id = Field()
    brand = Field()
    model = Field()
    category = Field()
    subcategory = Field()
    name = Field()
    first_image = Field()
    images = Field()
    price = Field()
    parameters = Field()
    description = Field()
    original_number = Field()
    substitute_number = Field()
    condition = Field()
    amount = Field()
    manufacturer = Field()
