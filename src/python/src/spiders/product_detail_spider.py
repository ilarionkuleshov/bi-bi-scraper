# -*- coding: utf-8 -*-
import json
import traceback

from scrapy import Request
from scrapy.utils.project import get_project_settings
from rmq.utils.decorators import rmq_callback

from spiders import BaseRMQSpider
from items import ProductDetailItem


class ProductDetailSpider(BaseRMQSpider):
    name = 'product_detail'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.task_queue_name = settings.get("PRODUCT_DETAIL_TASKS")
        self.result_queue_name = settings.get("PRODUCT_DETAIL_RESULTS")

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return Request(
            data["url"],
            meta={
                "detail_id": data["id"],
                "delivery_tag": _delivery_tag,
            },
            callback=self.parse,
            errback=self._errback,
            dont_filter=True,
        )

    @rmq_callback
    def parse(self, response):
        try:
            name = response.xpath("//h1[@itemprop='name']/span/text()").get()
            price = response.xpath("//span[@itemprop='price']/@content").get()
            if price is not None:
                try:
                    price = float(price)
                except:
                    price = None
            else:
                price = None

            images = response.xpath("//div[@id='imageBlock']//img[contains(@src, a.allegroimg.com)]/@src").getall()
            images = list(dict.fromkeys(images))
            if len(images):
                images = ";".join(images)
            else:
                images = None

            desc_selector = response.xpath("//div[@itemprop='description']")
            description = desc_selector.xpath("div[@id='divInnerDetails']/div[@id='descRus']/text()").get()

            parameters = desc_selector.xpath("div[@class='descriptionBlock']/span/text()").getall()
            original_number = None
            condition = None
            manufacturer = None
            if len(parameters):
                for parameter in parameters:
                    if "Номер  детали по каталогу: " in parameter:
                        try:
                            original_number = parameter.split(": ")[1].strip()
                        except:
                            original_number = None
                    elif "Состояние: " in parameter:
                        try:
                            condition = parameter.split(": ")[1].strip()
                        except:
                            condition = None
                    elif "Производитель деталей: " in parameter:
                        try:
                            manufacturer = parameter.split(": ")[1].strip()
                        except:
                            manufacturer = None
                parameters = "\n".join(parameters)
            else:
                parameters = None

            availability = response.xpath("//span[@itemprop='availability']/text()").get()
            if availability is not None and "Доступное количество: " in availability:
                try:
                    amount = int(availability.split(": ")[1].strip())
                except:
                    amount = None
            else:
                amount = None

            yield ProductDetailItem(
                {
                    "id": response.meta.get("detail_id"),
                    "name": name,
                    "images": images,
                    "price": price,
                    "parameters": parameters,
                    "description": description,
                    "original_number": original_number,
                    "condition": condition,
                    "amount": amount,
                    "manufacturer": manufacturer,
                }
            )
        except Exception as e:
            self._inject_exception_to_task(
                response.meta.get("delivery_tag"), e
            )
            self.logger.warning(traceback.format_exc())
